from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(OrigUserAdmin):
    ordering = ("email",)
