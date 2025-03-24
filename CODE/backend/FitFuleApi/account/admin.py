from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': (
        'age',
        'height',
        'weight',
        'allergy',
        'favorites',
        'goal',
        'activity_level'
        )}),
)
admin.site.register(CustomUser, UserAdmin)
