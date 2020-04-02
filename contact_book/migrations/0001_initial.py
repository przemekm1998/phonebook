# Generated by Django 3.0.5 on 2020-04-02 09:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('second_name', models.CharField(max_length=30)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('note', models.TextField()),
            ],
        ),
    ]