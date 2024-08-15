
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category_name>/", views.category, name="category"),
    path("auction/active", views.active_auctions_view, name="active_auctions_view"),
    path("listing/<int:listing_id>/", views.listing_detail, name="listing"),
    path("listing/<int:listing_id>/toggle-watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:listing_id>/place-bid/", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/close-auction/", views.close_auction, name="close_auction"),
    path("listing/<int:listing_id>/add-comment/", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/remove/", views.remove_listing, name="remove_listing"),
    path('listing/<int:listing_id>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:listing_id>/buy-it-now/', views.buy_it_now, name='buy_it_now'),
    path('listing/<int:listing_id>/payment/', views.payment, name='payment'),
    path('inbox/', views.inbox, name='inbox'),
    path('send-message/', views.send_message, name='send_message'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('profile/', views.profile, name='profile'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('auctions/won/', views.auctions_won, name='auctions_won'),
    path('category-data/', views.category_data, name='category_data'),
    path('help-center/', views.help_center, name='help_center'),
    path('create-payment/', views.create_payment, name='create_payment'),
    path('payment/<int:listing_id>/', views.payment_form, name='payment_form'),
    path('auctions/won/', views.auctions_won, name='won_auctions'),
    path('auctions/completed/', views.completed_auctions, name='completed_auctions'),
    path('listing/<int:listing_id>/confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('payment/<int:listing_id>/', views.payment_view, name='payment_view'),
    path('stripe-payment/<int:listing_id>/', views.stripe_payment, name='stripe_payment'),
    path('paypal-create-order/<int:listing_id>/', views.paypal_create_order, name='paypal_create_order'),
    path('paypal-capture-order/<int:listing_id>/', views.paypal_capture_order, name='paypal_capture_order'),
    path('payment-success/<int:listing_id>/', views.payment_success, name='payment_success'),
    path('listing/<int:listing_id>/delete/', views.delete_auction, name='delete_auction'),
    
    
    
    
    
    
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
