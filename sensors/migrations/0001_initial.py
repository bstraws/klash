# Generated by Django 2.0.4 on 2018-05-04 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tempature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.IntegerField(verbose_name='tempature')),
                ('hum', models.IntegerField(verbose_name='humidity')),
            ],
        ),
    ]