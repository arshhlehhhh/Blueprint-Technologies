# Generated by Django 3.1.1 on 2020-09-05 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distinctID', models.TextField()),
                ('articleData', models.TextField()),
                ('timestamp', models.DateField()),
            ],
        ),
    ]
