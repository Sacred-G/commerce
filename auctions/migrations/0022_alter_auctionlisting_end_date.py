# Generated by Django 5.0.7 on 2024-08-11 03:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_remove_comment_date_comment_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 18, 3, 10, 2, 335969, tzinfo=datetime.timezone.utc)),
        ),
    ]