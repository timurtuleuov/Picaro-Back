# Generated by Django 4.0.1 on 2023-06-09 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_post', '0006_rename_image_mapping_postimagemapping_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimagemapping',
            name='post_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='image_mappings', to='core_post.post'),
            preserve_default=False,
        ),
    ]
