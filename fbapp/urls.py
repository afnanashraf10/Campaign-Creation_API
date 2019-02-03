from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='FbApp-home'),
    path('view-campaign/', views.view_campaign, name='view-campaign'),
    path('view-adset/', views.view_adset, name='view-adset'),
    path('delete-campaign/<camid>/', views.delete_campaign, name='delete-campaign'),
    path('delete-adset/<adid>/', views.delete_adset, name='delete-adset'),
    path('create-campaign/', views.create_campaign, name='create-campaign'),
    path('create-adset/<camid>/', views.create_adset, name='create-adset'),
    path('create-ad/<adsetid>/', views.create_ad, name='create-ad'),
    path('view-ad/', views.view_ad, name='view-ad'),
    path('delete-ad/<adid>/', views.delete_ad, name='delete-ad'),
    path('update-adset/<adsetid>/<status>/', views.update_adset, name='update-adset'),
    path('update-campaign/<campid>/<status>/', views.update_campaign, name='update-campaign'),
]