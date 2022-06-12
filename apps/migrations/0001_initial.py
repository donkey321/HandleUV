# Generated by Django 4.0.5 on 2022-06-10 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiveImageTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remoteAddr', models.CharField(max_length=32, verbose_name='请求地址')),
                ('algCode', models.CharField(max_length=8, verbose_name='算法类型')),
                ('analyseId', models.CharField(max_length=32, verbose_name='分析ID')),
                ('imageData', models.TextField(verbose_name='图片数据')),
                ('ruleData', models.TextField(verbose_name='规则详情')),
                ('status', models.CharField(default='init', max_length=8, verbose_name='状态')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]