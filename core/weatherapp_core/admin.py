import kafkastreamer
from django.contrib import admin


@kafkastreamer.admin_site(source="admin")
class AdminSite(admin.AdminSite):
    pass


admin.site = AdminSite()
