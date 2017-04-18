# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import render
from .models import Question
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from .serializers import PollSerialiser, UserSerialiser
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from django.contrib.auth.models import User
# Create your views here.

class PollView(APIView):
    
    def get(self, request, username=None):
        if username is None:
            question=Question.objects.all()
            serializer=PollSerialiser(question, many=True)
            return Response(serializer.data)
        else:
            user=User.objects.get(username=username)
            token, created=Token.objects.get_or_create(user=user)
            if token:
                print 'valid user with token ' + token.key
            else:
                print 'not valid user.'
            return Response(status.HTTP_200_OK)
    
    def post(self, request, format=None):
        print request.data
        serializer=PollSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            question=Question.objects.get(question=request.data['question'])
            question.delete()
            return Response(status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
    
    def put(self, request, format=None):
        try:
            question=Question.objects.get(pub_date=request.data['pub_date'])
            serializer=PollSerialiser(question, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.data, status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

class MakeUser(APIView):
    def post(self, request, format=None):
        serializer=UserSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            token, created=Token.objects.get_or_create(user=user)
            serializer.validated_data['auth'] = token.key
            return Response(serializer.validated_data, status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, username=None, format=None):
        authentication_classes = (authentication.TokenAuthentication)
        # user = User.objects.get(username=username)
        return Response(request.user.profile.bio, status.HTTP_201_CREATED)

