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
    subname = models.CharField(max_length=88,default='默认提供，免费使用的轻量Ai引擎')#引擎介绍

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