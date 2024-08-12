"""commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from allauth.account.views import confirm_email

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auctions.urls")),
    path('accounts/', include('django.contrib.auth.urls')),  
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/login/', TemplateView.as_view(template_name="account/login.html")),
    path('accounts/signup/', TemplateView.as_view(template_name="account/signup.html")),
    path('accounts/confirm-email/<str:key>/', confirm_email, name='account_confirm_email'),
    path('accounts/', include('allauth.urls')),
]