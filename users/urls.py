from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # /users/register/
    path('login/', views.login_view, name='login'),      # /users/login/
    path('profile/', views.profile, name='profile'),    # /users/profile/
    path('logout/', views.logout_view, name='logout'),
]
