from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'photo_sharing_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.show, name='show'),
    path('posts/create/', views.create, name='create'),
    path('posts/<int:id>/edit/', views.edit, name='edit'),
    path('posts/<int:id>/delete/', views.delete, name='delete'),
    path('accounts/login/',
         auth_views.LoginView.as_view(
             redirect_authenticated_user=True,
             template_name='photo_sharing_app/registration/login.html',
         ),
         name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
