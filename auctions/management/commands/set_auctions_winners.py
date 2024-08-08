
from django.core.management.base import BaseCommand
from auctions.models import AuctionListing

class Command(BaseCommand):
    help = 'Sets winners for all closed auctions'

    def handle(self, *args, **options):
        closed_auctions = AuctionListing.objects.filter(is_active=False)
        for auction in closed_auctions:
            auction.set_winner()
        self.stdout.write(self.style.SUCCESS(f'Successfully set winners for {closed_auctions.count()} auctions'))
