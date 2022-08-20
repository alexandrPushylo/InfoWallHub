from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.db.models import Q

from django.contrib.auth.models import User
from presets.models import Preset
from presets.forms import UploadPresetForm

import tarfile

# Create your views here.
def upload_preset(request):
    FILE_IMAGE_NAME = "sys_wall.jpeg"


    if request.method == 'POST':
        archive = request.FILES.get('archive')
        title = request.POST['title']
        description = request.POST['description']
        widget_set = request.POST['widget_set']
        # private = True if request.POST['private'] == 'on' else False
        private = True if request.POST.get('private') else False

        author = request.user

        preset = Preset(archive=archive, title=title, description=description,
                        widget_set=widget_set, private=private, author=author)
        preset.image = f"storage/presets/{preset.uu_id}/{FILE_IMAGE_NAME}"
        preset.save()

        with tarfile.open(f"storage\presets\{preset.uu_id}\{archive}", 'r') as tar:
            tar.extract(FILE_IMAGE_NAME, f"storage\presets\{preset.uu_id}")

        return HttpResponseRedirect('/')

    return render(request, 'create.html', {"form": UploadPresetForm})


class ListAllPresetsView(ListView): ###TEST
    model = Preset
    template_name = "main.html"
    context_object_name = "presets"


class ListPublicPresetsView(ListView):  ## Show public presets
    model = Preset
    template_name = "public.html"
    context_object_name = "presets"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        presets = Preset.objects.filter(private=False)
        context['presets'] = presets
        return context


class ListPrivatePresetsView(ListView): ## Show private presets
    model = Preset
    template_name = "main.html"
    context_object_name = "presets"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        presets = Preset.objects.filter(author=self.request.user)
        context['presets'] = presets
        return context

class ListPresetsView(ListView): ## Adaptive
    model = Preset
    template_name = "main.html"
    context_object_name = "presets"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            presets = Preset.objects.filter(private=False)
        else:
            presets = Preset.objects.filter(Q(author=self.request.user) | Q(private=False))
        context['presets'] = presets
        return context



class DetailPresetView(DetailView):
    model = Preset
    template_name = "detail.html"
    context_object_name = "preset"


class EditPresetView(UpdateView):
    model = Preset
    template_name = "edit.html"
    fields = 'title', 'description'
    success_url = '/'


class DeletePresetView(DeleteView):
    model = Preset
    template_name = "delete.html"
    success_url = '/'


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

