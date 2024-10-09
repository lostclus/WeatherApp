"""
URL configuration for weatherapp_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from weatherapp_core.uihelpers.api import router as uihelpers_router
from weatherapp_core.users.api import UsersController

from .api_auth import auth

api = NinjaExtraAPI(auth=auth)
api.register_controllers(NinjaJWTDefaultController, UsersController)
api.add_router("", uihelpers_router)

urlpatterns = [
    path("core/admin/", admin.site.urls),
    path("core/api/v1/", api.urls),
]
