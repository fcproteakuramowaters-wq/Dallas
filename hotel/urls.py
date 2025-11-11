from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('facilities/', views.facilities, name='facilities'),
    path('reviews/', views.reviews, name='reviews'),
    path('contact/', views.contact, name='contact'),
]
