from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.room, name="room"),
    path('uploads/', views.uploads, name="uploads"),
    path("schedule/", views.schedule, name="schedule")
]

urlpatterns += static('images/',  document_root='/root/djangotutorial/chat/images') 
#nvm it is dynamically updated