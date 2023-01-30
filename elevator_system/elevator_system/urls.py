"""elevator_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from elevator import views as elevator_views
from elevator_admin import views as admin_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"elevator", elevator_views.ElevatorViewSet, "elevator")
router.register(r"floor", elevator_views.FloorViewSet, "floor")
router.register(r"system/admin", admin_views.ElevatorSystemViewSet, "elevator_system")
router.register(
    r"elevator/request", admin_views.ElevatorRequestViewSet, "elevator_request"
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
