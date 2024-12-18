"""
URL configuration for mysite project.

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
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    #html
    path('', views.home),
    path('loginregister/', views.loginregister),
    path("chat/", include("chat.urls")),
    path("stats/", views.stats),

    #css
    path('homecss/', views.homecss),
    path('loginregister.css/', views.loginregistercss),
    path('navbar.css/', views.navbarcss),

    #images
    path('backgroundhome/', views.homebackgroundimage),
    #path('foodz.jpg/', views.foodz),

    #loginregister
    path('register/', views.registeracc),
    path('login/', views.loginacc),
    path('logout/', views.logoutacc),

    #multimedia

    #js
]


#dynamically adds urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

