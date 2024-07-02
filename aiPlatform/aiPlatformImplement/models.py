# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db.models import UniqueConstraint
import uuid


class UserAccount(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user_id = models.CharField(
        null=False,
        unique=True,
        max_length=32,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(32),
            RegexValidator(
                regex='^[a-zA-Z0-9]+$',
                message='user_id must be an alphanumeric string.',
                code='invalid_user_id'
            ),
        ],
        help_text='Enter a user ID that is 6-32 characters long and contains only letters and numbers.'
    ) 
    user_password = models.CharField(max_length=255,null=False,blank=False)  
    user_nikeName = models.CharField(null=False,default='默认昵称',max_length=255)

class aiEngine(models.Model):
    id = models.IntegerField(default=0,primary_key=True)#引擎id
    name=models.CharField(max_length=32,default='默认对话Ai引擎')#引擎名称
    subname = models.CharField(max_length=88,default='默认提供,免费使用的轻量Ai引擎')#引擎介绍

class chatHistoryIndex(models.Model): #对话历史的目录
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) #对话的id
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    title = models.TextField()#对话的标题以文本形式保存
    engineID = models.ForeignKey(aiEngine,on_delete=models.CASCADE)

class chatHistoryContent(models.Model):
    indexID = models.ForeignKey(chatHistoryIndex,on_delete=models.CASCADE)#从属的对话目录Id
    role = models.BooleanField(default=False,null=False)#对话内容的角色（人还是机器）
    chatContent = models.TextField()#对话的内容以文本形式保存
    messageID = models.IntegerField(default=0)#消息顺序ID

    class Meta:
        constraints = [
            UniqueConstraint(fields=['indexID', 'messageID'], name='unique_indexID_messageID')
        ]

class ai(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255 )
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,) 
    owner = models.CharField(max_length=255)
    brief = models.TextField()  #简介
    time = models.DateField(auto_now=True)  #发布时间
    marks = models.IntegerField() #评分
    #prompt = models.ForeignKey()   #吴凡现在还没给我prompt models 说昨天给我现在都还没给 先不管    #ai对应的prompt训练模型
    level = models.IntegerField() #评论区总楼层 0视为没有评论

class great(models.Model):  #统计点赞情况 便于进行管理
    id = models.AutoField(primary_key=True)
    talk = models.ForeignKey('talk',on_delete=models.CASCADE,null=True,)
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,) 

class talk(models.Model):
    id = models.IntegerField(primary_key=True)
    follow = models.IntegerField()  #talk id && ai id  #属于 如果属于talk id 视为跟评 如果属于ai id 视为主评
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,)
    username = models.CharField(max_length=255)
    follownum = models.IntegerField()  #统计追评个数  追评默认为0 主频为n(追评个数)
    text = models.TextField()
    time = models.DateField(auto_now=True)
    greatNum = models.IntegerField() #统计点赞个数
    level = models.IntegerField() #统计楼层号



class favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,) 
    ai =  models.ForeignKey('ai',on_delete=models.CASCADE,null=True,) 
    time = models.DateField(auto_now=True)    
