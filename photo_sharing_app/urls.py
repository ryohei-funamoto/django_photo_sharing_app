from django.urls import path
from . import views

app_name = 'photo_sharing_app'

urlpatterns = [
    path('', views.index, name='index'),
]
