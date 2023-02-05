from django.urls import path

from . import views

urlpatterns = [
    path('cockpit/iam/', views.iam, name='iam'), 
    path('cockpit/log/', views.log, name='log'), 
    path('cockpit/dbms/', views.dbms, name='dbms'),
]