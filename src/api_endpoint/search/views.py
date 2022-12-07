from django.shortcuts import render

from .serializers import RedditV1Serializer

from rest_framework import serializers, views, response
from rest_framework import authentication, permissions

import redis
import json
import string
import random
import pprint

from .models import Job

redis_client = redis.Redis('redis' , 6379)

class HelloWorld(views.APIView) : 

    def get(self, request) : 
        return response.Response({'message' : 'Hello World!'})


# Create your views here.

class RedditV1(views.APIView) : 

    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request) : 
        
        search_serialzier = RedditV1Serializer(data=request.data)
        print("Search Serializer Validity : " ,  search_serialzier.is_valid())

        if search_serialzier.is_valid() : 
            
            print('Search Serializer has been validated...')
            print('Current User is :' , request.user.name)

            serializer_data = search_serialzier.data
            search_job_name = ''.join(random.choices(string.ascii_lowercase , k=50))

            serializer_data['job_name'] = search_job_name
            print('Seralizer Data is : ' )
            pprint.pprint(serializer_data)

            job = Job(user=request.user , **serializer_data)
            job.save()
            
            redis_client.lpush('queued' , search_job_name)
            redis_client.hset(search_job_name, json.dumps(serializer_data))
                
        return response.Response(search_serialzier.data)