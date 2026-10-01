from django.contrib import admin
from django.contrib.sessions.models import Session
from unfold.admin import ModelAdmin
from .models import Visitor

@admin.register(Visitor)
class VisitorAdmin(ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ['session_key', 'expire_date']
    search_fields = ['session_key']
    list_filter = ['expire_date']
