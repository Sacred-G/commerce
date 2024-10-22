# Auction Web Application

# This was created for CS50w project2!!

## Screenshots

| HOMESCREEN | DASHBOARD | PROFILE |
|------------|-----------|---------|
| ![HOMESCREEN](https://i.ibb.co/3NNQWkt/Screenshot-2024-08-09-at-12-46-05-AM.png) | ![DASHBOARD](https://i.ibb.co/gT0HKfb/Screenshot-2024-08-09-at-12-45-55-AM.png) | ![PROFILE](https://i.ibb.co/KrPTHKv/Screenshot-2024-08-09-at-12-53-33-AM.png) |
| CATEGORY | HELP_LIBRARY | PAYMENT |
| ![CATEGORY](https://i.ibb.co/ryyP5gL/Screenshot-2024-08-09-at-12-52-14-AM.png) | ![HELP_LIBRARY](https://i.ibb.co/Z2wktpy/Screenshot-2024-08-09-at-12-52-41-AM.png) | ![PAYMENT](https://i.ibb.co/gvg87bK/Screenshot-2024-08-09-at-12-50-42-AM.png) |
| CREDITCARD | MESSAGING | RECENTLY_VIEWED |
| ![CREDITCARD](https://i.ibb.co/K7Qy2bM/Screenshot-2024-08-09-at-12-51-11-AM.png) | ![MESSAGING](https://i.ibb.co/tDL8qQS/Screenshot-2024-08-09-at-12-53-43-AM.png) | ![RECENTLY_VIEWED](https://i.ibb.co/jTGG1Qc/Screenshot-2024-08-09-at-1-50-16-AM.png) |
| BUYITNOW | COMMENTS | RECENT_ACTIVITY |
| ![BUYITNOW](https://i.ibb.co/RzDTtpt/BUYITNOW.png) | ![COMMENTS](https://i.ibb.co/RhYWyyL/Screenshot-2024-08-09-at-12-50-28-AM.png) | ![RECENT_ACTIVITY](https://i.ibb.co/T1bHMcn/Screenshot-2024-08-09-at-02-00-15-SGB-Auctions.png) |

## Overview
This is a Django-based web application for online auctions. Users can create listings, bid on items, add items to their watchlist, and interact with other users through a messaging system. The application now includes payment processing integration with PayPal and Stripe.

## Features

* User authentication (register, login, logout)
* Create, edit, and close auction listings
* Bid on active auctions
* Add items to a personal watchlist
* Comment on auction listings
* User messaging system
* User profiles with auction statistics
* Categories for organizing listings
* Dashboard with auction statistics and charts
* Responsive design for mobile and desktop
* Payment processing with PayPal and Stripe
* Photo uploads for auction listings and user profiles

## Technologies Used

* Django 3.x
* Python 3.x
* HTML5
* CSS3
* JavaScript
* Bootstrap 4
* SQLite (default database)
* PayPal SDK
* Stripe API

## Setup and Installation

1. Clone the repository:

   ```
   git clone https://github.com/Sacred-G/commerce.git
   cd commerce
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv auctionenv
   source auctionvenv/bin/activate  # On Windows use `auctionenv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables for PayPal and Stripe:

   ```
   export PAYPAL_CLIENT_ID=your_paypal_client_id
   export PAYPAL_SECRET=your_paypal_secret
   export STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
   export STRIPE_SECRET_KEY=your_stripe_secret_key
   ```

5. Run migrations:

   ```
   python manage.py migrate
   ```

6. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```
   python manage.py runserver

   ```

8. Open a web browser and navigate to `http://127.0.0.1:8000/`

## Adding Photos

To enable photo uploads for auction listings and user profiles:

1. Update your settings.py:

   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

2. Update your main urls.py to serve media files during development:

   ```python
   from django.conf import settings
   from django.conf.urls.static import static

   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. Add ImageField to your models:

   ```python
   from django.db import models

   class AuctionListing(models.Model):
       # ... other fields ...
       image = models.ImageField(upload_to='auction_images/', blank=True, null=True)

   class Profile(models.Model):
       # ... other fields ...
       profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
   ```

4. Install Pillow for image processing:

   ```
   pip install Pillow
   ```

5. Update your forms to include file upload fields:

   ```python
   from django import forms
   from .models import AuctionListing, Profile

   class AuctionListingForm(forms.ModelForm):
       class Meta:
           model = AuctionListing
           fields = ['title', 'description', 'starting_bid', 'image', ...]

   class ProfileForm(forms.ModelForm):
       class Meta:
           model = Profile
           fields = ['bio', 'profile_picture', ...]
   ```

6. In your templates, use the correct enctype for file uploads:

   ```html
   <form method="post" enctype="multipart/form-data">
       {% csrf_token %}
       {{ form.as_p }}
       <button type="submit">Submit</button>
   </form>
   ```

7. Display images in your templates:

   ```html
   {% if auction.image %}
       <img src="{{ auction.image.url }}" alt="{{ auction.title }}">
   {% endif %}
   ```

Remember to handle cases where images might not exist to avoid errors in your templates.

## Usage

* Register a new account or log in
* Create new auction listings with photos
* Browse active auctions
* Place bids on items
* Add items to your watchlist
* Leave comments on auction pages
* Use the messaging system to contact other users
* View and update your profile, including profile picture
* Process payments using PayPal or Stripe when winning an auction

## Credit

Thanks to BobsProgrammingAcademy for the dashboard. His work inspired the design

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
