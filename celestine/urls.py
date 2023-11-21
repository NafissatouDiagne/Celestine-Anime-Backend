"""celestine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another U4Lconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from mikey import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('mikey.urls')),
    re_path(r'^api/register/$', views.register),
    re_path(r'^api/login_auth/$', views.login_auth),
    re_path(r'^api/updatephoto/<int:user_id>/$', views.updatephoto),
    re_path(r'^api/comments/<int:post_id>/$', views.Comment),
   
   
    path('api/', include('mikey.urls')),  # Include app-specific URLs
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
