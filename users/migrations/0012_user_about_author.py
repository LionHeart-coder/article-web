# Generated by Django 2.2.6 on 2021-02-04 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210128_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_author',
            field=models.TextField(default='without description', max_length=700),
            preserve_default=False,
        ),
    ]
