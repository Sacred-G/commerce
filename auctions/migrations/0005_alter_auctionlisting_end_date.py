# Generated by Django 5.0.7 on 2024-08-06 23:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_recentlyviewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 23, 48, 28, 595401, tzinfo=datetime.timezone.utc)),
        ),
    ]
