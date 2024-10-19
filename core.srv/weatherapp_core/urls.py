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
from ninja import NinjaAPI

from weatherapp_core import __version__
from weatherapp_core.geo.api import locations_router
from weatherapp_core.jwtauth.api import auth_router
from weatherapp_core.jwtauth.auth import async_auth_request
from weatherapp_core.uihelpers.api import uihelpers_router
from weatherapp_core.users.api import users_router

api = NinjaAPI(
    title="WeatherApp Core API",
    version=__version__,
    auth=async_auth_request,
)

api.add_router("", uihelpers_router)
api.add_router("/token/", auth_router)
api.add_router("/users/", users_router)
api.add_router("/locations/", locations_router)

urlpatterns = [
    path("core/admin/", admin.site.urls),
    path("core/api/v1/", api.urls),
]
