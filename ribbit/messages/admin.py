from django.contrib import admin
from models import Message

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)
