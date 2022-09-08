import os
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout, authenticate, login
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from presets.models import Preset, Vote
from presets.forms import UploadPresetForm

import shutil
import tarfile
import json
from random import randint


# Create your views here.
def detail_preset_view(request, uu_id):
    form = {}
    preset = Preset.objects.get(uu_id=uu_id)
    form['title'] = preset.title
    form['archive'] = preset.archive
    form['description'] = preset.description
    form['image'] = preset.image
    form['rating'] = preset.rating
    form['widget_set'] = preset.widget_set
    form['author'] = preset.author

    if request.method == 'POST':
        try:
            vote = Vote.objects.get(preset=preset, user=request.user)
            preset.sum_vote = int(preset.sum_vote) - int(vote.value)
        except ObjectDoesNotExist:
            vote = Vote.objects.create(preset=preset, user=request.user, value=request.POST['vote'])
        total_vote = int(preset.sum_vote) + int(request.POST['vote'])
        count_vote = len(Vote.objects.filter(preset=preset)) #TODO: count
        preset.rating = total_vote / count_vote
        preset.sum_vote = total_vote
        preset.save()
        vote.value = request.POST['vote']
        vote.save()
        return HttpResponseRedirect(f"/{uu_id}")
    return render(request, 'detail.html', form)


def upload_preset(request):
    FILE_IMAGE_NAME = "sys_wall.jpeg"   #TODO: module with constants
    FILE_CONFIG_NAME = "preset.json"

    if request.method == 'POST':
        archive = request.FILES.get('archive')
        title = request.POST['title']
        description = request.POST['description']
        private = True if request.POST.get('private') else False
        author = request.user
        preset = Preset(archive=archive, title=title, description=description,
                        private=private, author=author)
        preset.image = f"storage/presets/{preset.uu_id}/{FILE_IMAGE_NAME}"
        preset.save()

        with tarfile.open(f"storage/presets/{preset.uu_id}/{archive}", 'r') as tar:
            tar.extract(FILE_IMAGE_NAME, f"storage\presets\{preset.uu_id}")
            tar.extract(FILE_CONFIG_NAME, f"storage\presets\{preset.uu_id}")

        PATH_CONFIG_FILE = f"storage\presets\{preset.uu_id}\{FILE_CONFIG_NAME}"
        with open(PATH_CONFIG_FILE, 'r') as fp:
            config = json.load(fp)

        widget_set = config['widgets']
        preset.widget_set = widget_set
        preset.save()

        return HttpResponseRedirect('/private')
    return render(request, 'create.html', {"form": UploadPresetForm})


class ListPresetsView(ListView):
    model = Preset
    template_name = "main.html"
    context_object_name = "presets"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_anonymous:
            start_page = False
            presets = Preset.objects.filter(private=False)
            if self.request.get_full_path() == '/private':
                presets = Preset.objects.filter(author=self.request.user)
            elif self.request.get_full_path() == '/library':
                presets = Preset.objects.filter(Q(author=self.request.user) | Q(private=False))
            else:
                start_page = True
        else:
            presets = Preset.objects.filter(private=False)
            start_page = True

        context['presets'] = presets
        context['start_page'] = start_page
        return context


class EditPresetView(UpdateView):
    model = Preset
    template_name = "edit.html"
    fields = 'title', 'description', 'private'
    success_url = '/private'

    def get_object(self, queryset=None):
        uu_id = self.request.get_full_path().lstrip('/edit/')
        return Preset.objects.get(uu_id=uu_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preset = self.get_object()
        context['preset'] = preset
        return context


class DeletePresetView(DeleteView):
    model = Preset
    template_name = "delete.html"
    success_url = '/private'

    def get_object(self, queryset=None):
        uu_id = self.request.get_full_path().lstrip('/delete/')
        return Preset.objects.get(uu_id=uu_id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            from IWHub.settings import MEDIA_ROOT
            shutil.rmtree(f"{MEDIA_ROOT}{os.sep}presets{os.sep}{self.object.uu_id}",
                          ignore_errors=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def signin_view(request):
    out = {'err': False}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/private')
        else:
            out['err'] = True
    return render(request, 'signin.html', out)


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        new_user = User.objects.create_user(username=username, password=password,
                                            email=email, first_name=first_name, last_name=last_name,
                                            is_staff=False, is_superuser=False)
        new_user.save()
        login(request, new_user)
        return HttpResponseRedirect('/')
    return render(request, 'signup.html', {})


class SearchPresetsView(ListView):
    model = Preset
    template_name = "search_resault.html"
    context_object_name = "presets"

    def get_queryset(self):
        query = self.request.GET.get('q', "")
        criterion1 = Q(widget_set__icontains=query)
        criterion2 = Q(title__icontains=query)
        criterion3 = Q(author=self.request.user) | Q(private=False)
        object_list = Preset.objects.filter(criterion3 & (criterion1 | criterion2))
        return object_list

    def get_context_data(self, *, object_list=True, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q', "")
        sort = self.request.GET.get('sort')
        if sort == 'sort_author':
            sort_list = self.object_list.order_by('author')
        elif sort == 'sort_rating':
            sort_list = self.object_list.order_by('rating').reverse()
        else:
            sort_list = self.object_list.order_by('title')

        context['presets'] = sort_list
        return context


class CarouselView(ListView):
    model = Preset
    template_name = 'main.html'
    context_object_name = 'presets'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        reiting_list = Preset.objects.order_by('rating').reverse()
        len_list = len(reiting_list)//3
        n = randint(0, len_list)
        context['presets'] = reiting_list[n]
        context['start_page'] = True
        return context


def page_404_view(request):
    raise Http404(request)
