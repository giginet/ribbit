from django.contrib import admin
from models import Mention

class MentionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mention, MentionAdmin)
