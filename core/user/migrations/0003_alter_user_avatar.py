# Generated by Django 4.0.1 on 2023-06-04 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0002_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to='E:/Программирование/DJANGO+REACT/Scripts/front/src/assets/avatar/'),
        ),
    ]