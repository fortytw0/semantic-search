
from django.contrib import admin
from django.urls import path, include

from .views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/' , include('search.urls')) , 
    path('auth/', include('djoser.urls')) , 
    path('auth/', include('djoser.urls.authtoken')),
    path('' , hello , name='hello') 
]
