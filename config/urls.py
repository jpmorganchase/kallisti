"""kallisti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import path, include, reverse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from kallisticore.urls import urlpatterns as kallistiurls
from rest_framework import permissions

from kallisti.views.health import HealthAPI
from kallisti.views.info import InfoAPI

schema_view = get_schema_view(
    openapi.Info(
        title="Kallisti",
        default_version='v1',
        description="Create and manage your chaos experiments.",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def redirect_to_swagger_ui(*args, **kwargs):
    return redirect(reverse('swagger-ui'))


urlpatterns = [
                path('api/v1/', include([
                                        re_path(r'^', include(kallistiurls)),
                                        re_path(r'^info', InfoAPI.as_view(),
                                                name='info'),
                                        re_path(r'^health',
                                                HealthAPI.as_view(),
                                                name='health'),
                                        ])),
                re_path(r'^$', redirect_to_swagger_ui),
                re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                        schema_view.without_ui(cache_timeout=None),
                        name='schema-json'),
                re_path(r'^swagger/$',
                        schema_view.with_ui('swagger', cache_timeout=None),
                        name='swagger-ui'),
                re_path(r'^redoc/$',
                        schema_view.with_ui('redoc', cache_timeout=None),
                        name='swagger-redoc'),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
