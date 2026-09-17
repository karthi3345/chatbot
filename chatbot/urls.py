from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("chat-ui/", views.chat_ui),
    path("chat/", views.chat),
]