from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response

# Create your views here.

class TestView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({'get-status':"ok"})

    def post(self, request, *args, **kwargs):
        return Response({'post-status':"ok"})
