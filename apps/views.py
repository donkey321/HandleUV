from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .models import ReceiveImageTask
import json
import pprint


# 1.1.1.1 算法能力资源获取 [todo]
class ObtainResourceView(views.APIView):
    def post(self, request, *args, **kwargs):
        return Response({'ObtainResourceView-post-status':'ok'})

# 1.1.1.5 analysis image task(todo)
class AnalysisImageTaskView(views.APIView):
    def post(self, request, *args, **kwargs):
        #receive image task
        rit = request.data.copy()
        create_data = {}
        create_data.update({'algCode':rit.get('algCode')})
        create_data.update({'analyseId':rit.get('analyseId')})
        create_data.update({'imageData':rit.get('imageData')})

        if rit.get('rule',None):
            create_data.update({'ruleData': json.dumps(rit.get('rule'))})
        
        create_data.update({'remoteAddr':request.META.get('REMOTE_ADDR')})

        ritItem = ReceiveImageTask.objects.create(**create_data)

        pprint.pprint(create_data)

        return Response({'AnalysisImageTask-post-status':'ok'})

class TestView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({'get-status':"ok"})

    def post(self, request, *args, **kwargs):
        return Response({'post-status':"ok"})
