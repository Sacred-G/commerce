from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment, Category, Watchlist, Message, AuctionImage, RecentlyViewed, Profile
from django.contrib.auth.admin import UserAdmin


class BidAdmin(admin.ModelAdmin):
    BidAdmin = Bid
    list_display = ('id', 'auction', 'amount', 'user', 'date')

    def auction(self, obj):
        return obj.auction.title
    auction.short_description = 'Auction'


class CommentAdmin(admin.ModelAdmin):
    Comment = Comment
    list_display = ('id', 'listing', 'user', 'content', 'created_at')

    def listing(self, obj):
        return obj.listing.title
    listing.short_description = 'Listing'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'total_auctions_won',
                    'total_auctions_created', 'rating']
    search_fields = ['user__username', 'location']

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'starting_bid', 'current_price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'description')
\
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'created_at', 'read')
    list_filter = ('read',)
    search_fields = ("user_username", "location",)

class AuctionImageAdmin(admin.ModelAdmin):
    list_display = ('auction', 'image')

class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'viewed_at')

admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(AuctionImage, AuctionImageAdmin)
admin.site.register(RecentlyViewed, RecentlyViewedAdmin)