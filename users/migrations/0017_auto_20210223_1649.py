# Generated by Django 2.2.6 on 2021-02-23 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20210223_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_timestamp',
            field=models.IntegerField(default=1614099076, help_text='Время до повторной отправки письма', verbose_name='Переотправление письма'),
        ),
    ]
