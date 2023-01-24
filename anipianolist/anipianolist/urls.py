"""anipianolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# onii-chan please obey pep8-senpai https://peps.python.org/pep-0008/#imports

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import login, account_login_redirect

from allauth.account.views import logout

from allauth.socialaccount.providers.google.views import oauth2_login as google_oauth2_login
from allauth.socialaccount.providers.discord.views import oauth2_login as discord_oauth2_login
from allauth.socialaccount.providers.google.views import oauth2_callback as google_oauth2_callback
from allauth.socialaccount.providers.discord.views import oauth2_callback as discord_oauth2_callback

from allauth.socialaccount.views import login_cancelled, login_error, connections

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout, name="account_logout"),
    path('oauth2/google/login/', google_oauth2_login, name="google_login"),
    path('oauth2/google/login/callback/', google_oauth2_callback, name="google_callback"),
    path('oauth2/discord/login/', discord_oauth2_login, name="discord_login"),
    path('oauth2/discord/login/callback/', discord_oauth2_callback, name="discord_callback"),    
    path("login/", login, name="account_login"),
    path("login/cancelled/", login_cancelled, name="socialaccount_login_cancelled"),
    path("login/error/", login_error, name="socialaccount_login_error"),
    path("connections/", connections, name="socialaccount_connections"),
    path("accounts/login/", account_login_redirect, name="account_login_redirect"),
    path('', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
