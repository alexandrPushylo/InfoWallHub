# Generated by Django 4.1 on 2022-08-21 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presets', '0011_alter_preset_rating_alter_preset_sum_vote_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preset',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=999, null=True),
        ),
    ]
