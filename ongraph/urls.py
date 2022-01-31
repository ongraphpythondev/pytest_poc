
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),  # this is for my admin panel
    path('api-auth/', include('rest_framework.urls')),  # this helps in login and logout
    path('', include( 'app.urls')),      # this call my app urls
]