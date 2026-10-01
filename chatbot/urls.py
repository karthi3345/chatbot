from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("chat/", views.chat),
    path("login/", views.login_user),
    path("register/", views.register_user),
    path("logout/", views.logout_user),
]
