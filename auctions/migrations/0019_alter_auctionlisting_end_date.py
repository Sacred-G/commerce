# Generated by Django 5.0.7 on 2024-08-09 23:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_auctionlisting_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 23, 28, 7, 360261, tzinfo=datetime.timezone.utc)),
        ),
    ]