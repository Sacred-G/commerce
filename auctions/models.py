from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    facebook_id = models.CharField(max_length=50, blank=True, null=True)
    google_id = models.CharField(max_length=50, blank=True, null=True)
    twitter_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = CKEditor5Field(config_name='extends')
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    main_image = models.ImageField(
        upload_to='auction_images/', blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_listings")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    end_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=7))
    buy_it_now_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    payment_received = models.BooleanField(default=False)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')



        
    def set_winner(self):
        if not self.is_active and self.bids.exists():
            self.winner = self.bids.order_by('-amount').first().user
            self.save()

    def __str__(self):
        return self.title

    @property
    def additional_images(self):
        return self.images.all()  # Assuming you have a related_name="images" in AuctionImage


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid ${self.amount} on {self.auction.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} commented on {self.listing.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    is_system_message = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender or 'System'} to {self.recipient}: {self.subject}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics', blank=True, null=True)
    total_auctions_won = models.IntegerField(default=0)
    total_auctions_created = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)



class AuctionImage(models.Model):
    auction = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='auction_images/')

    def __str__(self):
        return f"Image for {self.auction.title}"


class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} viewed {self.listing.title}"


class Payment(models.Model):
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, null=True)  # Add null=True
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.listing.title if self.listing else 'Unknown listing'} by {self.buyer.username}"
    


class SocialShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20)  # e.g., 'facebook', 'twitter'
    shared_at = models.DateTimeField(auto_now_add=True)
    
    
