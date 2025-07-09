"""
URL configuration for taller13 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from administrativo import views as api_views

router = routers.DefaultRouter()
router.register(r"edificios", api_views.EdificioViewSet)
router.register(r"departamentos", api_views.DepartamentoViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("administrativo.urls")),   # vistas HTML
    path("api/", include(router.urls)),         # servicios web
    path("api-auth/", include("rest_framework.urls")),
]