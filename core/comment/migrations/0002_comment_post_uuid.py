# Generated by Django 4.0.1 on 2023-06-17 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post_uuid',
            field=models.UUIDField(default=0),
            preserve_default=False,
        ),
    ]
