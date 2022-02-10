"""efoymedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django_filters.views import FilterView
from client import views
from client.models import Video
from client.views import MyTokenObtainPairView

API_TITLE = 'Ethio Trend Api'
API_DESCRIPTION = 'a web api for creating media trend'


urlpatterns = [

    path('admin-efoymedia/', admin.site.urls),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('schema/', get_schema_view(title=API_TITLE)),
    path('api/v1/', include('client.urls')),

    # path('api-auth/', include('rest_framework.urls')),
    # path('api/v1/auth/', include('dj_rest_auth.urls')),

    # path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]