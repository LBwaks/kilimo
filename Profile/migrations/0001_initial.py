# Generated by Django 4.2.4 on 2023-09-05 05:59

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='Firstname')),
                ('lastname', models.CharField(max_length=50, verbose_name='Lastname')),
                ('slug', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('tell', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Phone Number')),
                ('county', models.CharField(choices=[('Mombasa', 'Mombasa'), ('Kwale', 'Kwale'), ('Kilifi', 'Kilifi'), ('TanaRiver', 'Tana River'), ('Lamu', 'Lamu'), ('Taita-Taveta', 'Taita-Taveta'), ('Garissa', 'Garissa'), ('Wajir', 'Wajir'), ('Mandera', 'Mandera'), ('Marsabit', 'Marsabit'), ('Isiolo', 'Isiolo'), ('Meru', 'Meru'), ('Tharaka Nithi', 'Tharaka-Nithi'), ('Embu', 'Embu'), ('Kitui', 'Kitui'), ('Machakos', 'Machakos'), ('Makueni', 'Makueni'), ('Nyandarua', 'Nyandarua'), ('Nyeri', 'Nyeri'), ('Kirinyaga', 'Kirinyaga'), ('Muranga', "Murang'a"), ('Kiambu', 'Kiambu'), ('Turkana', 'Turkana'), ('WestPokot', ' West Pokot'), ('Samburu', 'Samburu'), ('TransNzoia', 'Trans Nzoia'), ('Uasin Gishu', 'Uasin Gishu'), ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'), ('Nandi ', 'Nandi'), ('Baringo', 'Baringo'), ('Laikipia', 'Laikipia'), ('Nakuru', 'Nakuru'), ('Narok', 'Narok'), ('Kajiado', 'Kajiado'), ('Kericho', 'Kericho'), ('Bomet', 'Bomet'), ('Kakamega', 'Kakamega'), ('Vihiga', 'Vihiga'), ('Bungoma', 'Bungoma'), ('Busia', 'Busia'), ('Siaya', 'Siaya'), ('Kisumu ', 'Kisumu'), ('HomaBay', 'Homa Bay'), ('Migori', 'Migori'), ('Kisii', 'Kisii'), ('Nyamira', 'Nyamira'), ('Nairobi', 'Nairobi')], max_length=50, verbose_name='County')),
                ('sub_county', models.CharField(choices=[('Sub 1', 'Sub 1'), ('Sub 2', 'Sub 2'), ('Sub 3', 'Sub 3'), ('Sub 4', 'Sub 4'), ('Sub 5', 'Sub 5')], max_length=50, verbose_name='Sub County')),
                ('location', models.CharField(choices=[('Location 1', 'Location 1'), ('Location 2', 'Location 2'), ('Location 3', 'Location 3'), ('Location 4', 'Location 4'), ('Location 5', 'Location 5')], max_length=50, verbose_name='Location')),
                ('sub_location', models.CharField(choices=[('Sub_loc 1', 'Sub_loc 1'), ('Sub_loc 2', 'Sub_loc 2'), ('Sub_loc 3', 'Sub_loc 3'), ('Sub_loc 4', 'Sub_loc 4'), ('Sub_loc 5', 'Sub_loc 5')], max_length=50, verbose_name='Sub Location')),
                ('village', models.CharField(max_length=50, verbose_name='Village/Estates')),
                ('bio', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Bio')),
                ('interest', models.CharField(choices=[('Leasing Land', 'Leasing Land')], max_length=50, verbose_name='Interest')),
                ('other', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Explain Interest')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profiles', verbose_name='Profile')),
                ('status', models.CharField(default='Active', max_length=50, verbose_name='Status')),
                ('is_suspended', models.BooleanField(default=False, verbose_name='Suspended')),
                ('twitter', models.URLField(blank=True, null=True, verbose_name='Twitter')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('facebook', models.URLField(blank=True, null=True, verbose_name='Facebook')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]