# Generated by Django 2.2.6 on 2021-01-21 09:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0021_sociallink'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sociallink',
            unique_together={('user', 'link_type')},
        ),
    ]
