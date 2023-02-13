from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import ReceiveVideoTask
import json
import pprint
import cv2
import datetime
import requests
import time
import ffmpeg
from multiprocessing import Pool


def formatAnJianResult(initRe):
    reRe = []
    for item in initRe:
        reRe.append(item.get('className'))
    return reRe

def handleVideoUrl(rvid,vInfos):
    print("======start ffmpeg capture image=========")
    rv = ReceiveVideoTask.objects.get(id=rvid)
    rv.status = 'pending'
    rv.save()
    for vInfo in vInfos:
        videoUrl = vInfo.get('videoUrl','')
        vImgs = []
        out,_ = (ffmpeg.input(videoUrl)
                    .filter('select','gte(n,{})'.format(2))
                    .output('pipe:',vframes=1,format='image2',vcodec='mjpeg')
                    .run(capture_stdout=True)
                )
        timeStr = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        writeImagePath = "tmpImages/" + timeStr + ".jpg"
        with open(writeImagePath,'wb') as f:
            f.write(out)
        vImgs.append(timeStr + ".jpg")
        vInfo["images"] = vImgs
    rv.videoInfo = json.dumps(vInfos)
    rv.save()

    print("======image message saved,start analyse==========")
    for item in vInfos:
        itemImages = item.get('images',[])
        for ima in itemImages:
            try:
                postData = {'image':(ima, open('tmpImages/'+ima,'rb'), 'image/jpeg')}
                resp = requests.post('http://25.67.137.20:8082/upload_image/',files=postData)
                respData = resp.content.decode('utf-8')
                data = json.loads(respData)
                FileName = data.get('FileName')
                verUrl = 'http://25.67.137.20:8082/aqzy/inspect_general/'
                verReqData = {"FileName":FileName, "DetModel":["all"]}
                verResp = requests.post(verUrl, json=verReqData)
                verRespData = json.loads(verResp.content.decode('utf-8'))
                print("Anjian Model Return:",verRespData)
                analyseResult = {
                        "algCode": item.get("algCode"),
                        "analyseId": item.get("analyseId"),
                        "analyseTime": datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S'),
                        "analyseResults": formatAnJianResult(verRespData.get("ImgRecgRes")),
                    }
                try:
                    tyUrl = 'http://25.66.192.70:22266/analysis/api/v1/analyseResult'
                    tyResp = requests.post(tyUrl, json=analyseResult)
                    tyRespData = json.loads(tyResp.content.decode('utf-8'))
                    print("TYSP Return:",tyRespData)
                    if tyRespData.get('resultCode',None):
                        rv.status = 'done'
                        rv.save()
                        print("Success!Done!")
                except Exception as e:
                    raise Exception("return analyse result to tongyishipinpingtai error")
            except Exception as e:
                rv.status = 'error'
                rv.save()
                print("==============ErrorErrorError==================")
                print(str(e))
    return "123"
'''
        video_content = requests.get(videoUrl).content
        timeStr = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        videoName = "tmpVideos/" + timeStr + ".mp4"
        with open(videoName,"wb") as f:
            f.write(video_content)
        print("视频下载完成！准备抽帧截图！")
        cap = cv2.VideoCapture(videoName)
        vImgs = []
        if cap.isOpened():
            rval, frame = cap.read()
            timeRate = 10
            c = 1
            FPS = cap.get(5)
            while rval:
                rval,frame = cap.read()
                frameRate = int(FPS)*timeRate
                if c%frameRate == 0:
                    if frame is not None:
                        timeStr = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                        WriteRGBPath = "tmpImages/" + timeStr + "-" + str(c) + ".jpg"
                        cv2.imwrite(WriteRGBPath, frame)
                        vImgs.append(timeStr + "-" + str(c) + ".jpg")
                c += 1
                cv2.waitKey(1)
            cap.release()
        print("抽帧截图完成！保存数据库！")
        vInfo["images"] = vImgs
    rv.videoInfo = json.dumps(vInfos)
    rv.save()
'''
# 1.1.1.1 算法能力资源获取 [todo]
class ObtainResourceView(views.APIView):
    def post(self, request, *args, **kwargs):
        return Response({'ObtainResourceView-post-status':'ok'})

#  analysis video task(todo)
class AnalysisVideoTaskView(views.APIView):
    def post(self, request, *args, **kwargs):
        #receive video task
        rit = request.data.copy()
        print("Request Data:")
        pprint.pprint(rit)

        create_data = {}
        create_data.update({'algCode':rit.get('algCode')})
        create_data.update({'algParams':rit.get('algParams','')})
        create_data.update({'analyseId':rit.get('analyseId')})
        create_data.update({'startTime':rit.get('startTime')})
        create_data.update({'endTime':rit.get('endTime')})
        create_data.update({'interval':rit.get('interval')})
        create_data.update({'command':rit.get('command')})
        if rit.get('videoInfo',None):
            create_data.update({'videoInfo':json.dumps(rit.get('videoInfo'))})

        if rit.get('rule',None):
            create_data.update({'rule': json.dumps(rit.get('rule'))})
        create_data.update({'remoteAddr':request.META.get('REMOTE_ADDR')})

        ritItem = ReceiveVideoTask.objects.create(**create_data)
        print("Create Data Done!")

        respData = {
                "resultCode":"200",
                "resultValue":[],
                "resultHint": None,
        }
        
        # handle video task
        videoInfos = json.loads(create_data.get('videoInfo',[]))
        pool = Pool(1)
        pool.apply_async(handleVideoUrl,args=(ritItem.id,videoInfos))

        for v in videoInfos:
            respData["resultValue"].append({
                "analyseId": v.get("analyseId"),
                "devCode": v.get("devCode"),
                "osdVideoUrl": v.get("videoUrl")
            })
        pprint.pprint(respData)
        return Response(respData)
        

class TestView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({'get-status':"ok"})

    def post(self, request, *args, **kwargs):
        return Response({'post-status':"ok"})
