from django.shortcuts import render
from django.core import serializers

from .serializers import RedditV1Serializer

from rest_framework import views, response, authentication


import redis
import json
import string
import random

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

        if search_serialzier.is_valid() : 
    
            serializer_data = search_serialzier.data
            search_job_name = ''.join(random.choices(string.ascii_lowercase , k=50))
            serializer_data['job_name'] = search_job_name

            job = Job(user=request.user , **serializer_data)
            job.save()
            
            redis_client.lpush('queued' , search_job_name)
            redis_client.set(search_job_name , 'queued')
            redis_client.hset('queued_job_details' , search_job_name, json.dumps(serializer_data))
                
            return response.Response({'status':'success','job_name' : search_job_name})

        else : 
            return response.Response(search_serialzier.errors)


class ListJobs(views.APIView) : 

    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request) :
        jobs = Job.objects.filter(user=request.user)
        print(serializers.serialize('json' , jobs))
        return response.Response(serializers.serialize('json' , jobs))

class JobStatus(views.APIView) :

    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, job_name) : 
        status = redis_client.get(job_name)
        return response.Response({'job_name' : status})

class GetFinishedJobs(views.APIView) : 

    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request) : 

        jobs = Job.objects.filter(user=request.user).order_by('-time_submitted')
        results = [json.loads(redis_client.hget('finished_job_details' , job.job_name)) for job in jobs]
        return response.Response(results)

        





