# Generated by Django 5.0.7 on 2024-08-12 22:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_alter_auctionlisting_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 19, 22, 44, 48, 503774, tzinfo=datetime.timezone.utc)),
        ),
    ]
