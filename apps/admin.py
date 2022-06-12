from django.contrib import admin

# Register your models here.
from .models import ReceiveImageTask

admin.site.site_header = "人工智能平台&统一视频平台集成"


class ReceiveImageTaskAdmin(admin.ModelAdmin):
    list_display = ['remoteAddr', 'algCode', 'analyseId','status', 'created']
    list_editable = []
    list_per_page = 10
    ordering = ('-created',)
    
admin.site.register(ReceiveImageTask, ReceiveImageTaskAdmin)
