# Generated by Django 4.1 on 2022-08-21 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presets', '0006_preset_rating_alter_vote_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='preset',
            name='count_vote',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='preset',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=999, null=True),
        ),
    ]