# File: auctions/management/commands/populate_categories.py

from django.core.management.base import BaseCommand
from auctions.models import Category

class Command(BaseCommand):
    help = 'Populate the database with initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            'Electronics', 'Fashion', 'Home & Garden', 'Sports', 'Toys & Hobbies',
            'Art', 'Books', 'Music', 'Collectibles', 'Jewelry'
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created category "{category_name}"'))
