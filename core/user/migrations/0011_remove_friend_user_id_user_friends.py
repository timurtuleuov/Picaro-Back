# Generated by Django 4.0.1 on 2023-07-27 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_user', '0010_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='user_id',
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(to='core_user.Friend'),
        ),
    ]
