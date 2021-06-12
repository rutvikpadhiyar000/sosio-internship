from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('subscribe', views.subscribe),
    path('subscribe_to_mail_list', views.subscribe_to_mail_list)
]