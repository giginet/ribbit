from django.contrib import admin
from models import Room

class RoomAdmin(admin.ModelAdmin):
    pass
admin.site.register(Room, RoomAdmin)
