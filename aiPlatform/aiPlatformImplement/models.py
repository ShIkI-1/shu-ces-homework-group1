# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

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

class ai(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,) 
    owner = models.CharField(max_length=255)
    brief = models.TextField()  #简介
    time = models.DateField(auto_now=True)  #发布时间
    marks = models.IntegerField() #评分
    level = models.IntegerField() #评论区总楼层 0视为没有评论


class talk(models.Model):
    id = models.IntegerField(primary_key=True)
    follow = models.IntegerField()  #talk id && ai id  #属于 如果属于talk id 视为跟评 如果属于ai id 视为主评
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,)
    username = models.CharField(max_length=255)
    follownum = models.IntegerField()  #统计追评个数  追评默认为0 主频为n(追评个数)
    text = models.TextField()
    time = models.DateField(auto_now=True)
    great = models.IntegerField() #统计点赞个数
    level = models.IntegerField() #统计楼层号



class favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,) 
    ai =  models.ForeignKey('ai',on_delete=models.CASCADE,null=True,)  #更改为ai id
    time = models.DateField(auto_now=True)    
