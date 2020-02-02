from django.urls import path

from . import views

urlpatterns = [
    path('api/events', views.events, name='events'),
    path('', views.index, name='index'),
]
