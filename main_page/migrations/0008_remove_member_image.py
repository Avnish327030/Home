# Generated by Django 2.0.6 on 2018-06-20 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0007_member_manager_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='image',
        ),
    ]
