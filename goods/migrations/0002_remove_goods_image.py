# Generated by Django 4.2.16 on 2024-12-10 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='image',
        ),
    ]