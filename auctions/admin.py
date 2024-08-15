from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import AuctionListing, Bid, Comment, Watchlist, Message, Profile, AuctionImage, RecentlyViewed, Payment, Category

class UserAdmin(DefaultUserAdmin):
    # Define the fields to be displayed in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # Define the fields to be used for searching users
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Define filters to be applied in the admin interface
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    # Define the fields to be used in the user forms
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Define the fields to be used in the user creation and editing forms
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'current_price', 'category', 'created_by', 'created_at', 'is_active', 'end_date', 'buy_it_now_price', 'payment_received', 'winner')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_by', 'is_active', 'payment_received')
    readonly_fields = ('created_at',)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction', 'amount', 'date')
    list_filter = ('auction', 'user')
    readonly_fields = ('date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'content', 'date')
    list_filter = ('listing', 'user')
    readonly_fields = ('date',)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'created_at', 'read', 'is_system_message')
    list_filter = ('recipient', 'sender', 'read', 'is_system_message')
    readonly_fields = ('created_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date', 'phone_number', 'profile_picture', 'total_auctions_won', 'total_auctions_created', 'rating')

@admin.register(AuctionImage)
class AuctionImageAdmin(admin.ModelAdmin):
    list_display = ('auction', 'image')

@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'viewed_at')
    readonly_fields = ('viewed_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'amount', 'is_complete', 'created_at', 'updated_at')
    list_filter = ('listing', 'buyer', 'is_complete')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
