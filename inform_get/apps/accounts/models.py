from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    position = models.CharField(max_length=60)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    deployment = models.ForeignKey('Deployment', on_delete=models.DO_NOTHING)
    isLeader = models.BooleanField()
    isActive = models.BooleanField()
    syncmask = models.SmallIntegerField(default=0)
    utime = models.DateTimeField('更新时间')
    ctime = models.DateTimeField(auto_now=True)


class Deployment(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    level = models.IntegerField('层级')
    present = models.BooleanField()
    utime = models.DateTimeField('更新时间')
    ctime = models.DateTimeField(auto_now=True)
