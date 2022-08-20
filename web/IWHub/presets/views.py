from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.http import HttpResponseRedirect

from presets.models import Preset
from presets.forms import upload_preset

import tarfile

# Create your views here.
def upload_preset(request):
    FILE_IMAGE_NAME = "sys_wall.jpeg"

    if request.method == 'POST':
        archive = request.FILES.get('archive')
        title = request.POST['title']
        description = request.POST['description']
        widget_set = request.POST['widget_set']
        private = True if request.POST['private'] == 'on' else False
        author = request.user

        preset = Preset(archive=archive, title=title, description=description,
                        widget_set=widget_set, private=private, author=author)
        preset.image = f"static/presets/{preset.uu_id}/{FILE_IMAGE_NAME}"
        preset.save()

        with tarfile.open(f"static\presets\{preset.uu_id}\{archive}", 'r') as tar:
            tar.extract(FILE_IMAGE_NAME, f"static\presets\{preset.uu_id}")

        return HttpResponseRedirect('/')

    return render(request, 'create.html', {"form": upload_preset})





