from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'search'

urlpatterns = [
    path('reddit/v1/', RedditV1.as_view() , name='reddit_v1_search'),
    path('reddit/v1/list_jobs' , ListJobs.as_view() , name='reddit_v1_list_jobs'),
    path('hw/v1/', HelloWorld.as_view() , name='helloworld'),
    path('reddit/v1/finished/' , GetFinishedJobs.as_view() , name='finished_jobs'),
    path('reddit/v1/status/<job_name>/' , JobStatus.as_view() , name='job_status')
    ]


