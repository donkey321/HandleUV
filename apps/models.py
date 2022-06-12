from django.db import models

# Create your models here.

class ReceiveImageTask(models.Model):
    remoteAddr = models.CharField('请求地址', max_length=32)
    algCode = models.CharField('算法类型', max_length=8)
    analyseId = models.CharField('分析ID', max_length=32)
    imageData = models.TextField('图片数据')
    ruleData = models.TextField('规则详情')

    status = models.CharField('状态', max_length=8, default='init',
            choices=(('init','未处理'),('pending','处理中'),('done','已完成')))

    created = models.DateTimeField(auto_now_add=True)
