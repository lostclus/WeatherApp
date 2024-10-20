from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OrigUserAdmin
from django.utils.translation import gettext_lazy as _

from weatherapp_core.geo.models import DefaultLocation

from .models import User


class DefaultLocationInline(admin.StackedInline):
    model = DefaultLocation


@admin.register(User)
class UserAdmin(OrigUserAdmin):
    list_display = ("email", "is_staff", "is_superuser", "is_active")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Settings"),
            {
                "fields": (
                    "timezone",
                    "temperature_unit",
                    "wind_speed_unit",
                    "precipitation_unit",
                    "date_format",
                    "time_format",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "usable_password", "password1", "password2"),
            },
        ),
    )
    inlines = (DefaultLocationInline,)
