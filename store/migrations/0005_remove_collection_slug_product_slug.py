# Generated by Django 4.1.7 on 2023-02-26 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_collection_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='slug',
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]
