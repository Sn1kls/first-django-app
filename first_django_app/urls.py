"""
URL configuration for first-django-app project.

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
from django.urls import include, path
from django_ratelimit.decorators import ratelimit
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/token/",
        ratelimit(key="user", rate="10000/d", block=True)(TokenObtainPairView.as_view()),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        ratelimit(key="user", rate="10000/d", block=True)(TokenRefreshView.as_view()),
        name="token_refresh",
    ),
    path(
        "api/token/verify/",
        ratelimit(key="user", rate="10000/d", block=True)(TokenVerifyView.as_view()),
        name="token_verify",
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/schema/swagger-ui/",
        ratelimit(key="user", rate="10000/d", block=True)(SpectacularSwaggerView.as_view(url_name="api-schema")),
        name="swagger-ui",
    ),
    path("api/users/", include("users.urls")),
]
