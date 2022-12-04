from django.urls import path, include
from rest_framework import routers

from .views import RedditV1 , HelloWorld

app_name = 'search'

urlpatterns = [
    path('reddit/v1/', RedditV1.as_view() , name='reddit_v1_search'),
    path('hw/v1/', HelloWorld.as_view() , name='helloworld'),
    ]


