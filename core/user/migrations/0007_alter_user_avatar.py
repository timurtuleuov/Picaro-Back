# Generated by Django 4.0.1 on 2023-06-22 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar/default-avatar.png', upload_to='avatar/'),
        ),
    ]
