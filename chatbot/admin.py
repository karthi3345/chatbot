from django.contrib import admin
from django.contrib.sessions.models import Session
from unfold.admin import ModelAdmin, TabularInline
from .models import Visitor, ChatSession, ChatMessage

@admin.register(Visitor)
class VisitorAdmin(ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = ['session_key', 'expire_date']
    search_fields = ['session_key']
    list_filter = ['expire_date']

class ChatMessageInline(TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['sender', 'message', 'timestamp']
    can_delete = False

@admin.register(ChatSession)
class ChatSessionAdmin(ModelAdmin):
    list_display = ('__str__', 'session_id', 'ip_address', 'created_at', 'updated_at')
    search_fields = ('session_id', 'ip_address', 'user__username')
    list_filter = ('created_at',)
    inlines = [ChatMessageInline]

