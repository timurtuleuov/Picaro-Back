# Generated by Django 4.0.1 on 2023-06-09 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_post', '0004_remove_postimagemapping_post_post_image_mapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_mapping',
        ),
        migrations.AddField(
            model_name='postimagemapping',
            name='image_mapping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core_post.post'),
        ),
    ]
