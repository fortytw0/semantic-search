from django.urls import path, include
from rest_framework import routers

from .views import RedditV1 , HelloWorld , ListJobs

app_name = 'search'

urlpatterns = [
    path('reddit/v1/', RedditV1.as_view() , name='reddit_v1_search'),
    path('reddit/v1/list_jobs' , ListJobs.as_view() , name='reddit_v1_list_jobs'),
    path('hw/v1/', HelloWorld.as_view() , name='helloworld'),
    ]


