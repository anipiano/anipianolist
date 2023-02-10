from django.urls import path

from . import views

urlpatterns = [
    path('cockpit/', views.cockpit, name='cockpit'),
    path('cockpit/iam/', views.iam, name='iam'), 
    path('cockpit/log/', views.log, name='log'), 
    path('cockpit/dbms/', views.dbms, name='dbms'),
    path('cockpit/dbms/modify/<str:entry_id>', views.modify, name='modify'),
    path('cockpit/dbms/delete/<str:entry_id>', views.delete, name='delete'),
    path('cockpit/arrangements/', views.arrangements, name='arrangements')
]