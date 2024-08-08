from django.contrib import admin
from .models import Bid, Comment, User, Profile
from django.contrib.auth.admin import UserAdmin
class BidAdmin(admin.ModelAdmin):
    BidAdmin = Bid
    list_display = ('id', 'listing', 'amount', 'user', 'date')

    def listing(self, obj):
        return obj.listing.title
    listing.short_description = 'Listing'

class CommentAdmin(admin.ModelAdmin):
    Comment
    list_display = ('id', 'listing', 'user', 'content', 'date')

    def listing(self, obj):
        return obj.listing.title
    listing.short_description = 'Listing'

admin.site.register(User, UserAdmin)

admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'total_auctions_won', 'total_auctions_created', 'rating']
    search_fields = ['user__username', 'location']