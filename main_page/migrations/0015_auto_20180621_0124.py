# Generated by Django 2.0.6 on 2018-06-20 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0014_auto_20180621_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='profile', width_field='width_field'),
        ),
    ]
