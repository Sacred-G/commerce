# Generated by Django 5.0.7 on 2024-08-07 18:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auctionlisting_winner_alter_auctionlisting_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 14, 18, 2, 50, 429405, tzinfo=datetime.timezone.utc)),
        ),
    ]
