from django import forms


class UploadPresetForm(forms.Form):
    archive = forms.FileField(label="Архив")
    title = forms.CharField(max_length=255, label="Название")
    description = forms.CharField(max_length=512, widget=forms.Textarea, label="Описание")
    widget_set = forms.CharField(max_length=255, label="Набор виджетов")
    private = forms.BooleanField(label="Приватный", initial=True, required=False,)


class DetailPresetForm(forms.Form):
    image = forms.ImageField(label="Превью")
    title = forms.CharField(max_length=255, label="Название")
    description = forms.CharField(max_length=512, widget=forms.Textarea, label="Описание")
    widget_set = forms.CharField(max_length=255, label="Набор виджетов")
    private = forms.BooleanField(label="Приватный", initial=True, required=False, )
    rating = forms.DecimalField(label="Рейтинг")
