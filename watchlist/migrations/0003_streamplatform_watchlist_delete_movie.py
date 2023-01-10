# Generated by Django 4.1.4 on 2022-12-26 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0002_rename_movies_movie_alter_movie_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('about', models.CharField(max_length=200)),
                ('website', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'Stream Platforms',
            },
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=False)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'WatchList',
            },
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
