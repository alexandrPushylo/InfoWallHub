from django import forms
from presets.models import Preset


class UploadPresetForm(forms.ModelForm):
    class Meta:
        model = Preset
        fields = 'archive', 'title', 'description', 'private'
