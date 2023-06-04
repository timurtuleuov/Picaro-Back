# Generated by Django 4.0.1 on 2023-06-04 09:11

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='username', unique=True),
        ),
    ]