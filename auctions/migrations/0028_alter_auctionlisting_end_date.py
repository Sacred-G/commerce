# Generated by Django 5.0.7 on 2024-08-12 20:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_alter_auctionlisting_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 19, 20, 53, 56, 771590, tzinfo=datetime.timezone.utc)),
        ),
    ]