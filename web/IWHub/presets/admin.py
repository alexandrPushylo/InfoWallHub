from django.contrib import admin
from .models import Preset, Vote, FileStorage
# Register your models here.
admin.site.register(Preset)
admin.site.register(Vote)
admin.site.register(FileStorage)
