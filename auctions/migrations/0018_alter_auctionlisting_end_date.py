# Generated by Django 5.0.7 on 2024-08-09 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_auctionlisting_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 16, 12, 49, 51, 49841, tzinfo=datetime.timezone.utc)),
        ),
    ]