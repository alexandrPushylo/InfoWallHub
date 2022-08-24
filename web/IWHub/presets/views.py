from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from presets.models import Preset, Vote
from presets.forms import UploadPresetForm  #, DetailPresetForm

import tarfile
import json


# Create your views here.
def detail_preset_view(request,pk):
    form = {}
    preset = Preset.objects.get(pk=pk)
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

        count_vote = len(Vote.objects.filter(preset=preset))    #count votes

        preset.rating = total_vote / count_vote
        preset.sum_vote = total_vote
        preset.save()
        vote.value = request.POST['vote']
        vote.save()

        return HttpResponseRedirect(f"/{pk}")
    return render(request, 'detail.html', form)


def upload_preset(request):
    FILE_IMAGE_NAME = "sys_wall.jpeg"
    FILE_CONFIG_NAME = "config.json"


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
        widget_set = config['widgets'].keys()
        widget_set = ', '.join(widget_set)
        preset.widget_set = widget_set
        preset.save()

        return HttpResponseRedirect('/')

    return render(request, 'create.html', {"form": UploadPresetForm})


class ListPresetsView(ListView): ## Adaptive
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



# class DetailPresetView(DetailView):
#     model = Preset
#     template_name = "detail.html"
#     context_object_name = "preset"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


class EditPresetView(UpdateView):
    model = Preset
    template_name = "edit.html"
    fields = 'title', 'description', 'private'
    success_url = '/'


class DeletePresetView(DeleteView):
    model = Preset
    template_name = "delete.html"
    success_url = '/private'


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')    ###Redirect to a success page.
        else:
            return HttpResponse('invalid login')

    return render(request, 'signin.html', {})


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
    template_name = "main.html"
    context_object_name = "presets"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Preset.objects.filter(
            Q(widget_set__icontains=query) |
            Q(title__icontains=query)
        )
        return object_list


def carousel_view(request):
    form = {}

    preset = Preset.objects.order_by('rating')

    return render(request, "start_page.html", form)


class CarouselView(ListView):
    model = Preset
    template_name = 'main.html'
    context_object_name = 'presets'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        reiting_list = Preset.objects.order_by('rating').reverse()[:3]
        context['presets'] = reiting_list
        context['start_page'] = True

        return context