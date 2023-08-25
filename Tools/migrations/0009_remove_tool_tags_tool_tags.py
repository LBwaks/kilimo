# Generated by Django 4.2.4 on 2023-08-25 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tools', '0008_tool_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='tags',
        ),
        migrations.AddField(
            model_name='tool',
            name='tags',
            field=models.ManyToManyField(to='Tools.tag', verbose_name='Tags'),
        ),
    ]
