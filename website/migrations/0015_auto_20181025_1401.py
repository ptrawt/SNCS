# Generated by Django 2.0.6 on 2018-10-25 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20181025_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='serial_port',
            field=models.CharField(max_length=20),
        ),
    ]
