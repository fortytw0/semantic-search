from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from .serializers import RedditV1Serializer

from rest_framework import serializers, views, response
from rest_framework import authentication, permissions

class HelloWorld(views.APIView) : 

    def get(self, request) : 
        return response.Response({'message' : 'Hello World!'})


# Create your views here.

class RedditV1(views.APIView) : 

    # authentication_classes = [authentication.TokenAuthentication]

    def post(self, request) : 
        
        search_serialzier = RedditV1Serializer(data=request.data)
        print("Serializer Validity : " ,  search_serialzier.is_valid())
                
        return response.Response(search_serialzier.data)