# Generated by Django 2.0.6 on 2018-10-21 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20181018_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='base_template',
            name='name',
        ),
    ]
