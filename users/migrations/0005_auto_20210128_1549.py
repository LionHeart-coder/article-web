# Generated by Django 2.2.6 on 2021-01-28 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210128_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='users/profile-default.jpg', null=True, upload_to='users/avatars', verbose_name='Аватар пользователя'),
        ),
    ]
