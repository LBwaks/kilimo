# Generated by Django 4.2.4 on 2023-08-21 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shamba', '0004_land_location_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landimages',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='lands', verbose_name='Land Images'),
        ),
    ]
