from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from client.views import  VideoViewSet
from client import views
router = SimpleRouter()
router.register(r'videos', VideoViewSet, basename='videos')
# router.register(r'^view$', views.auto_complete, basename='auto_complete')
urlpatterns = [
# router.register(r'^view$', views.auto_complete, basename='auto_complete')
    re_path(r'^view$', views.auto_complete, name='auto_complete'),
    re_path(r'^query$', views.search_youtube, name='search_youtube')
]
for url in router.urls:
    urlpatterns.append(url)
