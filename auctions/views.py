from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max, Count, Sum, OuterRef, Subquery, Q
from django import forms
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import transaction
from .models import AuctionListing, Bid, Category, Watchlist, Message, Profile, User, RecentlyViewed, Payment,Comment
from .forms import AuctionForm, BidForm, CommentForm, MessageForm, UserForm, ProfileForm, AuctionImageFormSet, AuctionImageForm
from .utils import send_auction_message
from django.core.exceptions import ValidationError
import stripe
from django.http import Http404



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def index(request):
    active_listings = AuctionListing.objects.filter(is_active=True)
    categories = Category.objects.all()
    ending_soon_auctions = AuctionListing.objects.filter(
        is_active=True,
        end_date__gt=timezone.now()
    ).order_by('end_date')[:5]  # Get top 5 ending soon

    # Get recently viewed items
    recently_viewed_items = []
    if request.user.is_authenticated:
        recently_viewed = RecentlyViewed.objects.filter(user=request.user).order_by('-viewed_at')[:5]
        recently_viewed_items = [rv.listing for rv in recently_viewed]
    
    context = {
        "listings": active_listings,
        "categories": categories,
        "recently_viewed_items": recently_viewed_items,
        'ending_soon_auctions': ending_soon_auctions,
    }
    return render(request, "auctions/index.html", context)


@login_required
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "auctions/index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/index.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')  # or whatever your home page URL name is
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def dashboard(request):
    highest_bid_count = AuctionListing.objects.annotate(bid_count=Count('bids')).aggregate(Max('bid_count'))['bid_count__max']
    highest_bid_listing = AuctionListing.objects.annotate(bid_count=Count('bids')).order_by('-bid_count').first()
    
    highest_price = Bid.objects.aggregate(Max('amount'))['amount__max']
    highest_price_listing = AuctionListing.objects.filter(bids__amount=highest_price).first()
    active_listings = AuctionListing.objects.filter(is_active=True)
    ending_soon_auctions = AuctionListing.objects.filter(
        is_active=True,
        end_date__gt=timezone.now()
    ).order_by('end_date')[:5]  # Get top 5 ending soon
    active_listings = AuctionListing.objects.filter(is_active=True)

    
    context = {
        "total_auctions": AuctionListing.objects.count(),
        "active_auctions": AuctionListing.objects.filter(is_active=True).count(),
        "total_bids": Bid.objects.count(),
        "total_categories": Category.objects.count(),
        "highest_bid": Bid.objects.aggregate(Max('amount'))['amount__max'] or 0,
        "popular_category": Category.objects.annotate(
            listing_count=Count('auctionlisting')
        ).order_by('-listing_count').first(),
        "latest_auction": AuctionListing.objects.order_by('-created_at').first(),
        'highest_bid_count': highest_bid_count,
        'highest_bid_listing': highest_bid_listing,
        'highest_price': highest_price,
        'highest_price_listing': highest_price_listing,
        "listings": active_listings,
        'ending_soon_auctions': ending_soon_auctions,
    }
    return render(request, "auctions/dashboard.html", context)
@login_required
def create_listing(request):
    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        image_formset = AuctionImageFormSet(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.current_price = listing.starting_bid
            listing.save()
            images = image_formset.save(commit=False)
            for image in images:
                if image.image:
                    image.auction = listing
                    image.save()
            messages.success(request, 'Your listing has been created successfully!')
            return redirect('index')
        else:
            messages.error(request, 'There was an error with your form. Please check the details.')
    else:
        form = AuctionForm()
        image_formset = AuctionImageFormSet()

    context = {
        "form": form,
        "image_formset": image_formset,
    }
    return render(request, "auctions/create_listing.html", context)
def listing_detail(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    additional_images = listing.additional_images.all()

    # Get the highest bid and bidder
    highest_bid = listing.bids.order_by('-amount').first()
    highest_bidder = highest_bid.user if highest_bid else None

    context = {
        'listing': listing,
        'additional_images': additional_images,
        'bid_form': BidForm(),
        'comment_form': CommentForm(),
        'highest_bidder': highest_bidder,
        'buy_it_now_price': listing.buy_it_now_price,
    }

    if request.method == 'POST' and 'buy_it_now' in request.POST:
        if request.user.is_authenticated and request.user != listing.created_by:
            if listing.buy_it_now_price and listing.is_active:
                # Process the purchase
                listing.is_active = False
                listing.winner = request.user
                listing.current_price = listing.buy_it_now_price  # Correct assignment
                listing.save()
                messages.success(request, 'You have successfully purchased this item!')
                return redirect('payment_form', listing_id=listing.id)
        else:
            messages.error(request, 'You must be logged in to make a purchase.')

    return render(request, 'auctions/listing_detail.html', context)

@login_required

def watchlist(request):
    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.filter(user=request.user)
        context = {
            'watchlist': user_watchlist
        }
        return render(request, 'auctions/watchlist.html', context)
    else:
        return redirect('login')
def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": all_categories})

def category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    Watchlist.objects.get_or_create(user=request.user, listing=listing)
    messages.success(request, "Added to watchlist.")
    return redirect('index')

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    Watchlist.objects.filter(user=request.user, listing=listing).delete()
    messages.success(request, "Removed from watchlist.")
    return redirect('index')


@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['amount']
            if listing.is_active:
                if request.user != listing.created_by:
                    if bid_amount > listing.current_price:
                        bid = form.save(commit=False)
                        bid.user = request.user
                        bid.auction = listing
                        bid.save()
                        listing.current_price = bid_amount
                        listing.save()
                        
                        # Send messages about the new bid
                        send_auction_message(
                            sender=request.user, 
                            recipient=listing.created_by, 
                            listing=listing,
                            message_type="new_bid_seller",
                            additional_info={
                                "bid_amount": bid_amount, 
                                "bidder": request.user.username
                            }
                        )
                        send_auction_message(
                            sender=None, 
                            recipient=request.user, 
                            listing=listing,
                            message_type="new_bid_buyer",
                            additional_info={"bid_amount": bid_amount}
                        )
                        
                        messages.success(request, 'Your bid was placed successfully!')
                    else:
                        messages.error(request, 'Your bid must be higher than the current price.')
                else:
                    messages.error(request, 'You cannot bid on your own auction.')
            else:
                messages.error(request, 'This auction is no longer active.')
        else:
            messages.error(request, 'Invalid bid. Please enter a valid amount.')
    
    return redirect('listing', listing_id=listing_id)


@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    
    if request.user != listing.created_by:
        messages.error(request, "You don't have permission to close this auction.")
        return redirect('listing', listing_id=listing_id)
    
    if not listing.is_active:
        messages.warning(request, "This auction is already closed.")
        return redirect('listing', listing_id=listing_id)
    
    if request.method == 'POST':
        listing.is_active = False
        highest_bid = Bid.objects.filter(auction=listing).order_by('-amount').first()
        
        if highest_bid:
            listing.winner = highest_bid.user
            listing.current_price = highest_bid.amount
            
            # Send messages
            send_auction_message(None, listing.created_by, listing, 'auction_end_seller')
            send_auction_message(None, listing.winner, listing, 'auction_won')
            
            # Notify other bidders
            other_bidders = Bid.objects.filter(auction=listing).exclude(user=listing.winner).values_list('user', flat=True).distinct()
            for bidder in other_bidders:
                send_auction_message(None, bidder, listing, 'auction_end_buyer')
            
            listing.save()
            messages.success(request, 'Auction closed successfully.')
            return redirect('payment', listing_id=listing_id)
        else:
            listing.save()
            send_auction_message(None, listing.created_by, listing, 'auction_end_seller')
            messages.info(request, 'Auction closed, but there were no bids.')
    
    return redirect('listing', listing_id=listing_id)

@login_required
def confirm_payment(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.user != listing.winner:
        messages.error(request, "You are not authorized to confirm payment for this auction.")
        return redirect('listing', listing_id=listing_id)
    
    if request.method == 'POST':
        # Process the payment (you may want to integrate with a payment gateway here)
        listing.payment_received = True
        listing.save()
        
        # Send message to the seller
        Message.objects.create(
            sender=request.user,
            recipient=listing.created_by,
            subject=f"Payment received for {listing.title}",
            body=f"The payment for your auction item '{listing.title}' has been received."
        )
        
        messages.success(request, "Payment confirmed successfully.")
        return redirect('listing', listing_id=listing_id)
    
    return redirect('payment', listing_id=listing_id)



def send_user_message(sender, recipient, subject, body):
    Message.objects.create(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body
    )






# Modify the create_payment view:
@login_required
@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        
        if request.user != listing.winner:
            return JsonResponse({'success': False, 'error': 'Unauthorized payment attempt'})
        
        amount = int(listing.current_price * 100)  # amount in cents
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description=f'Payment for auction: {listing.title}',
                source=request.POST.get('stripeToken')
            )
            
            # Create Payment object in your database
            payments = Payment.objects.order_by('-created_at')(
                user=request.user,
                stripe_charge_id=charge.id,
                amount=listing.current_price
            )
            
            # Update auction listing payment status
            listing.payment_status = 'paid'
            listing.save()
            
            # Send message to the buyer
            send_user_message(
                sender=listing.created_by,
                recipient=request.user,
                subject=f"Payment successful for {listing.title}",
                body=f"Your payment of ${listing.current_price} for {listing.title} has been processed successfully. Thank you for your purchase!"
            )
            
            # Send message to the seller
            send_user_message(
                sender=request.user,
                recipient=listing.created_by,
                subject=f"Payment received for {listing.title}",
                body=f"The payment of ${listing.current_price} for your auction {listing.title} has been received from {request.user.username}."
            )
            
            messages.success(request, 'Payment successful!')
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            listing.payment_status = 'failed'
            listing.save()
            
            # Send message about failed payment
            send_user_message(
                sender=listing.created_by,
                recipient=request.user,
                subject=f"Payment failed for {listing.title}",
                body=f"Your payment of ${listing.current_price} for {listing.title} has failed. Please try again or contact support if you continue to have issues."
            )
            
            return JsonResponse({'success': False, 'error': str(e)})

@login_required
def payment_form(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.method == 'POST':
        # Process payment (you'll need to integrate with a payment gateway here)
        # For now, we'll just show a success message
        messages.success(request, 'Payment processed successfully!')
        return redirect('listing', listing_id=listing_id)
    return render(request, 'auctions/payment_form.html', {'listing': listing})

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
    return redirect('listing', listing_id=listing_id)




    
def active_auctions_view(request):
    active_listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/active_auctions.html", {
        "listings": active_listings
    })



@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
    
    if not created:
        watchlist_item.delete()
    
    return redirect('listing', listing_id=listing_id)

@login_required
def remove_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.user == listing.created_by:
        if request.method == "POST":
            listing.delete()
            return redirect('index')  # Redirect to the main page after deletion
        else:
            return render(request, "auctions/confirm_remove.html", {"listing": listing})
    else:
        return redirect('listing', listing_id=listing_id)
    
    
    
    
@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.user != listing.created_by:
        return redirect('listing', listing_id=listing_id)
    
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing', listing_id=listing_id)
    else:
        form = AuctionForm(instance=listing)
    
    return render(request, 'auctions/edit_listing.html', {'form': form, 'listing': listing})
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'auctions/inbox.html', {
        'messages': received_messages,
        'sent_messages': sent_messages
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'auctions/send_message.html', {'form': form})

@login_required
def view_message(request, message_id):
    # Try to get the message where the user is either the recipient or the sender
    message = Message.objects.filter(id=message_id).filter(
        Q(recipient=request.user) | Q(sender=request.user)
    ).first()

    if message is None:
        raise Http404("No Message matches the given query.")

    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')

    if not message.read and message.recipient == request.user:
        message.read = True
        message.save()

    return render(request, 'auctions/view_message.html', {'message': message, 'sent_messages': sent_messages})


def get_unread_count(user):
    return Message.objects.filter(recipient=user, read=False).count()
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    # Fetch recent bids
    recent_bids = Bid.objects.filter(user=request.user).order_by('-date')[:5]
    
    # Fetch recent created auctions
    recent_auctions = AuctionListing.objects.filter(created_by=request.user).order_by('-created_at')[:5]
    
    # Combine and sort recent activities
    recent_activities = sorted(
        list(recent_bids) + list(recent_auctions),
        key=lambda x: x.date if hasattr(x, 'date') else x.created_at,
        reverse=True
    )[:10]  # Limit to 10 most recent activities
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'recent_activities': recent_activities,
    }
    return render(request, 'auctions/profile.html', context)



@login_required
def auctions_won(request):
    # Subquery to get the highest bid for each auction
    highest_bids = Bid.objects.filter(auction=OuterRef('pk')).order_by('-amount')
    
    # Query to get auctions won by the user
    won_auctions = AuctionListing.objects.filter(
        is_active=False,
        bids__user=request.user
    ).annotate(
        highest_bid=Subquery(highest_bids.values('amount')[:1]),
        highest_bidder=Subquery(highest_bids.values('user')[:1])
    ).filter(highest_bidder=request.user)

    print(f"Number of won auctions: {won_auctions.count()}")
    for auction in won_auctions:
        print(f"Auction: {auction.title}, Highest bid: {auction.highest_bid}, Highest bidder: {auction.highest_bidder}")


    return render(request, 'auctions/auctions_won.html', {'won_auctions': won_auctions})

def category_data(request):
    categories = AuctionListing.objects.values('category__name').annotate(count=Count('category')).order_by('-count')
    data = [{'name': item['category__name'] or 'Uncategorized', 'count': item['count']} for item in categories]
    return JsonResponse(data, safe=False)



def help_center(request):
    return render(request, 'auctions/help_center.html')
@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if request.user == listing.created_by:
        listing.is_active = False
        highest_bid = Bid.objects.filter(auction=listing).order_by('-amount').first()
        if highest_bid:
            listing.winner = highest_bid.user
            listing.current_price = highest_bid.amount
            # Send message to the winner
            send_user_message(
                sender=request.user,
                recipient=listing.winner,
                subject=f"You've won the auction for {listing.title}!",
                body=f"Congratulations! You've won the auction for {listing.title} with a bid of ${listing.current_price}. Please proceed to make your payment."
            )
        listing.save()
        messages.success(request, 'Auction closed successfully.')
        return redirect('payment', listing_id=listing_id)
    return redirect('listing', listing_id=listing_id)

@login_required
def payment(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    payment = get_object_or_404(Payment, listing=listing, buyer=request.user, is_complete=False)
    
    if request.method == 'POST':
        try:
            # Here you would integrate with a payment gateway
            # For demonstration, we'll just mark the payment as complete
            with transaction.atomic():
                payment.is_complete = True
                payment.save()
                
                listing.payment_received = True
                listing.save()
                
                messages.success(request, 'Payment successful! The item will be shipped to you soon.')
                return redirect('listing', listing_id=listing.id)
        except Exception as e:
            messages.error(request, 'An error occurred while processing your payment. Please try again.')
    
    return render(request, 'auctions/payment.html', {'listing': listing, 'payment': payment})
@login_required
def buy_it_now(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    
    if request.method == 'POST':
        if not listing.is_active:
            messages.error(request, 'This listing is no longer active.')
            return redirect('listing', listing_id=listing.id)
        
        if not listing.buy_it_now_price:
            messages.error(request, 'This listing does not have a Buy It Now price.')
            return redirect('listing', listing_id=listing.id)
        
        if request.user == listing.created_by:
            messages.error(request, 'You cannot buy your own listing.')
            return redirect('listing', listing_id=listing.id)
        
        try:
            with transaction.atomic():
                listing.is_active = False
                listing.winner = request.user
                listing.current_price = listing.buy_it_now_price
                listing.save()
                
                Payment.objects.create(
                    listing=listing,
                    buyer=request.user,
                    amount=listing.buy_it_now_price,
                    is_complete=False
                )
                
                messages.success(request, 'You have successfully initiated the purchase. Please complete the payment.')
                return redirect('payment', listing_id=listing.id)
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'An error occurred while processing your purchase: {str(e)}')
    
    return redirect('listing', listing_id=listing.id)





@login_required
def completed_auctions(request):
    completed_auctions = AuctionListing.objects.filter(created_by=request.user, is_active=False)
    return render(request, 'auctions/completed_auctions.html', {'completed_auctions': completed_auctions})



@login_required
def payment_view(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    context = {
        'listing': listing,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'auctions/payment.html', context)

@csrf_exempt
def stripe_payment(request, listing_id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=listing_id)
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=int(listing.current_price * 100),
                currency='usd',
                description=f'Payment for {listing.title}',
                source=token,
            )
            # Process successful payment (e.g., mark listing as sold, create order, etc.)
            return redirect('payment_success', listing_id=listing_id)
        except stripe.error.CardError as e:
            # Handle failed payment
            return render(request, 'auctions/payment.html', {
                'listing': listing,
                'error': str(e)
            })

@csrf_exempt
def paypal_create_order(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    # Implement PayPal order creation logic here
    # This is a placeholder response
    return JsonResponse({'id': 'PAYPAL_ORDER_ID'})

@csrf_exempt
def paypal_capture_order(request, listing_id):
    # Implement PayPal order capture logic here
    # This is a placeholder response
    return JsonResponse({'status': 'success'})

def payment_success(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    return render(request, 'auctions/payment_success.html', {'listing': listing})


@login_required
def delete_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    
    if request.user != listing.created_by:
        messages.error(request, "You don't have permission to delete this auction.")
        return redirect('listing', listing_id=listing_id)
    
    if request.method == 'POST':
        listing_title = listing.title  # Store the title before deletion
        
        # Delete related objects
        Bid.objects.filter(auction=listing).delete()
        Comment.objects.filter(listing=listing).delete()
        Watchlist.objects.filter(listing=listing).delete()
        
        # Delete the auction
        listing.delete()
        
        # Add success message
        messages.success(request, f"Your auction '{listing_title}' has been successfully deleted.")
        
        # Send confirmation message to the user
        send_auction_message(
            user=request.user,
            listing=None,  # The listing is already deleted
            role="seller",
            message_type="auction_deleted",
            additional_info={"title": listing_title}
        )
        
        return redirect('index')  # Redirect to home page or user's listings
    
    return render(request, 'auctions/confirm_delete.html', {'listing': listing})