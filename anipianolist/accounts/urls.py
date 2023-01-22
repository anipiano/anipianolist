from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path('@<str:username>/', views.user, name='user') # this should be tried last, but todo server-side validation of usernames so they don't interfere with URL routing
]