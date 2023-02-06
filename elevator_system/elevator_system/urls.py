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
from django.urls import include, path, re_path
from elevator import views as elevator_views
from elevator_admin import views as admin_views
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# schema_view = get_swagger_view(title='Elevator System APIs')
schema_view = get_schema_view(
    openapi.Info(
        title="Elevator System APIs",
        default_version='v1',
        description="Elevator System APIs",
        terms_of_service="",
        contact=openapi.Contact(email="prabhpreet.singh.pep@gmail.com"),
        license=openapi.License(name="Elevator System APIs"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(
    r"elevator",
    elevator_views.ElevatorViewSet,
)
router.register(
    r"floor",
    elevator_views.FloorViewSet,
)
router.register(
    r"system/admin",
    admin_views.ElevatorSystemViewSet,
)
router.register(
    r"elevator-request",
    admin_views.ElevatorRequestViewSet,
)

urlpatterns = [
    # path('doc/', schema_view),
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  #<-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  #<-- Here
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

]
