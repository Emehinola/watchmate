# Generated by Django 4.1.4 on 2022-12-27 17:04

from django.db import migrations, models
import django.db.models.deletion
import watchlist.models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0004_watchlist_platform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveBigIntegerField(validators=[watchlist.models.minValue, watchlist.models.maxValue])),
                ('description', models.CharField(max_length=200, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='watchlist.watchlist')),
            ],
        ),
    ]
