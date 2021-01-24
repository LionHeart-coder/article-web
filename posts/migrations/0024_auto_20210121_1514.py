# Generated by Django 2.2.6 on 2021-01-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_auto_20210121_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='link_type',
            field=models.CharField(choices=[('youtube', 'Youtube'), ('twitter', 'Twitter'), ('vk', 'Вконтакте'), ('instagram', 'Instagram'), ('facebook', 'Facebook')], max_length=10, verbose_name='Тип ссылки'),
        ),
    ]
