from django.db import models
import uuid

from django.contrib.auth.models import User
# Create your models here.


def user_directory_path(instance, filename):
    return "static/presets/{0}/{1}".format(str(instance.uu_id), filename)


class Preset(models.Model):
    image = models.ImageField(upload_to=user_directory_path, verbose_name="Превью")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=512, verbose_name="Описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # author = models.CharField(max_length=255, verbose_name="Автор")
    widget_set = models.CharField(max_length=255, null=True, blank=True, verbose_name="Набор виджетов")
    private = models.BooleanField(default=True, verbose_name="Приватный")
    uu_id = models.UUIDField(default=uuid.uuid4)
    archive = models.FileField(upload_to=user_directory_path)
    # archive = models.FileField(upload_to='static/presets')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Пресет"
        verbose_name_plural = "Пресеты"
