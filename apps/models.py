from django.db import models

# Create your models here.

class ReceiveVideoTask(models.Model):
    remoteAddr = models.CharField('请求地址', max_length=32)
    algCode = models.CharField('算法类型', max_length=8)
    algParams = models.CharField('参数', blank=True, null=True, max_length=32)
    analyseId = models.CharField('分析ID', max_length=32)
    startTime = models.CharField('start time', max_length=32)
    endTime = models.CharField('end time', max_length=32)
    interval = models.CharField('interval', max_length=8)
    command = models.CharField('command', max_length=64)
    videoInfo = models.TextField('video info')
    rule = models.TextField('规则详情')


    status = models.CharField('状态', max_length=8, default='init',
            choices=(('init','未处理'),('pending','处理中'),('error','已失败'),('done','已完成')))

    created = models.DateTimeField(auto_now_add=True)


class ReceiveImageTask(models.Model):
    remoteAddr = models.CharField('请求地址', max_length=32)
    algCode = models.CharField('算法类型', max_length=8)
    analyseId = models.CharField('分析ID', max_length=32)
    imageData = models.TextField('图片数据')
    ruleData = models.TextField('规则详情')

    status = models.CharField('状态', max_length=8, default='init',
            choices=(('init','未处理'),('pending','处理中'),('done','已完成')))
    created = models.DateTimeField(auto_now_add=True)
