# Generated by Django 4.2.4 on 2023-08-25 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tools', '0005_tag_rename_created_date_category_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Tools.category', verbose_name='Category'),
            preserve_default=False,
        ),
    ]