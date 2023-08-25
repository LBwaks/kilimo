# Generated by Django 4.2.4 on 2023-08-25 05:56

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
                ('description', models.TextField(max_length=250)),
                ('is_published', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorys',
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
                ('price', models.CharField(max_length=50, verbose_name='Price')),
                ('period', models.CharField(choices=[('1 Hour', '1 Hour'), ('1 Day', '1 Day'), ('1 Week', '1 Week'), ('1 Month', '1 Month'), ('1 Season', '1 Season')], max_length=50, verbose_name='Period Per Price')),
                ('county', models.CharField(choices=[('Mombasa', 'Mombasa'), ('Kwale', 'Kwale'), ('Kilifi', 'Kilifi'), ('TanaRiver', 'Tana River'), ('Lamu', 'Lamu'), ('Taita-Taveta', 'Taita-Taveta'), ('Garissa', 'Garissa'), ('Wajir', 'Wajir'), ('Mandera', 'Mandera'), ('Marsabit', 'Marsabit'), ('Isiolo', 'Isiolo'), ('Meru', 'Meru'), ('Tharaka Nithi', 'Tharaka-Nithi'), ('Embu', 'Embu'), ('Kitui', 'Kitui'), ('Machakos', 'Machakos'), ('Makueni', 'Makueni'), ('Nyandarua', 'Nyandarua'), ('Nyeri', 'Nyeri'), ('Kirinyaga', 'Kirinyaga'), ('Muranga', "Murang'a"), ('Kiambu', 'Kiambu'), ('Turkana', 'Turkana'), ('WestPokot', ' West Pokot'), ('Samburu', 'Samburu'), ('TransNzoia', 'Trans Nzoia'), ('Uasin Gishu', 'Uasin Gishu'), ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'), ('Nandi ', 'Nandi'), ('Baringo', 'Baringo'), ('Laikipia', 'Laikipia'), ('Nakuru', 'Nakuru'), ('Narok', 'Narok'), ('Kajiado', 'Kajiado'), ('Kericho', 'Kericho'), ('Bomet', 'Bomet'), ('Kakamega', 'Kakamega'), ('Vihiga', 'Vihiga'), ('Bungoma', 'Bungoma'), ('Busia', 'Busia'), ('Siaya', 'Siaya'), ('Kisumu ', 'Kisumu'), ('HomaBay', 'Homa Bay'), ('Migori', 'Migori'), ('Kisii', 'Kisii'), ('Nyamira', 'Nyamira'), ('Nairobi', 'Nairobi')], max_length=50, verbose_name='County')),
                ('sub_county', models.CharField(choices=[('Sub 1', 'Sub 1'), ('Sub 2', 'Sub 2'), ('Sub 3', 'Sub 3'), ('Sub 4', 'Sub 4'), ('Sub 5', 'Sub 5')], max_length=50, verbose_name='Subcounty')),
                ('location', models.CharField(choices=[('Location 1', 'Location 1'), ('Location 2', 'Location 2'), ('Location 3', 'Location 3'), ('Location 4', 'Location 4'), ('Location 5', 'Location 5')], max_length=50, verbose_name='Location')),
                ('sub_location', models.CharField(choices=[('Sub_loc 1', 'Sub_loc 1'), ('Sub_loc 2', 'Sub_loc 2'), ('Sub_loc 3', 'Sub_loc 3'), ('Sub_loc 4', 'Sub_loc 4'), ('Sub_loc 5', 'Sub_loc 5')], max_length=50, verbose_name='Sublocation')),
                ('village', models.CharField(max_length=50, verbose_name='Village/Estate')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description About the tool')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tools.category', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Tool',
                'verbose_name_plural': 'Tools',
            },
        ),
        migrations.CreateModel(
            name='ToolImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tools', verbose_name='')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='')),
                ('tools', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tools.tool', verbose_name='')),
            ],
            options={
                'verbose_name': 'ToolImage',
                'verbose_name_plural': 'ToolImages',
            },
        ),
    ]