"""
URL configuration for driveshare project.

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

from django.contrib import admin #import admin feature
from django.urls import path,include #define proj urls
from django.conf import settings #get db and other important settings
from django.conf.urls.static import static #static media and files


urlpatterns = [
    path('admin/', admin.site.urls), #/admin as registered superuser
    path('users/', include('users.urls')), #users section
    path('cars/', include('cars.urls')), #cars section
    path('', include('home.urls')), #home/main page
    path('message/', include('message.urls')), #messages section
    path('notifications/', include('notifications.urls')), #notifications section

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)