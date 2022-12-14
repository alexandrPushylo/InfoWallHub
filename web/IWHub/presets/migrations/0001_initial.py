# Generated by Django 4.1 on 2022-08-20 11:37

from django.db import migrations, models
import presets.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=presets.models.user_directory_path, verbose_name='Превью')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(max_length=512, verbose_name='Описание')),
                ('author', models.CharField(max_length=255, verbose_name='Автор')),
                ('widget_set', models.CharField(blank=True, max_length=255, null=True, verbose_name='Набор виджетов')),
                ('private', models.BooleanField(default=True, verbose_name='Приватный')),
                ('uu_id', models.UUIDField(default=uuid.uuid4)),
                ('archive', models.FileField(upload_to=presets.models.user_directory_path)),
            ],
            options={
                'verbose_name': 'Пресет',
                'verbose_name_plural': 'Пресеты',
            },
        ),
    ]
