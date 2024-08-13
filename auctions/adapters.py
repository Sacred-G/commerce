
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return reverse('index')  # or your desired redirect URL

    def get_signup_redirect_url(self, request):
        return reverse('index')  # or your desired redirect URL
