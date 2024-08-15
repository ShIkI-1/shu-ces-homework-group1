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
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.fields import validators

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
    user_Credits = models.FloatField(default=5,null=False)
    avaterindex = models.IntegerField(default=0, null=False)

class aiEngine(models.Model):
    id = models.IntegerField(default=0,primary_key=True)#引擎id
    name=models.CharField(max_length=32,default='默认对话Ai引擎')#引擎名称
    subname = models.CharField(max_length=88,default='默认提供,免费使用的轻量Ai引擎')#引擎介绍

class chatHistoryIndex(models.Model): #对话历史的目录
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) #对话的id
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    title = models.TextField()#对话的标题以文本形式保存
    engineID = models.ForeignKey(aiEngine,on_delete=models.CASCADE)
    createTime=models.DateTimeField(auto_now_add=True)

class chatHistoryContent(models.Model):
    indexID = models.ForeignKey(chatHistoryIndex,on_delete=models.CASCADE)#从属的对话目录Id
    role = models.BooleanField(default=False,null=False)#对话内容的角色（人还是机器）0=人
    chatContent = models.TextField()#对话的内容以文本形式保存
    messageID = models.IntegerField(default=0)#消息顺序ID

    class Meta:
        constraints = [
            UniqueConstraint(fields=['indexID', 'messageID'], name='unique_indexID_messageID')
        ]


class ai(models.Model):  # 差一些参数
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE, null=True, )
    owner = models.CharField(max_length=255)
    brief = models.TextField()  # 简介
    time = models.DateField(auto_now=True)  # 发布时间
    marks = models.FloatField(default=0)  # 评分
    prompt = models.ForeignKey('prompt', on_delete=models.CASCADE, null=True)
    level = models.IntegerField(default=0)  # 评论区总楼层 0视为没有评论
    price = models.IntegerField(default=0) #价格


class great(models.Model):  # 统计点赞情况 便于进行管理
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
    followflag = models.IntegerField(default=0)  #标识
    level = models.IntegerField() #统计楼层号


class favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,) 
    ai =  models.ForeignKey('ai',on_delete=models.CASCADE,null=True,) 
    time = models.DateField(auto_now=True)    




class prompt(models.Model):
    pid = models.IntegerField(primary_key=True, default=1)
    title = models.CharField(max_length=200)
    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE, null=True, )
    intro = models.CharField(max_length=2000)
    text = models.TextField()
    flexibility = models.FloatField(default=0, null=False)  # 限定范围没做
    randomness = models.FloatField(default=0, null=False)  # 同上


class rating(models.Model):
    rid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    aif = models.ForeignKey('ai', on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'aif')


@receiver(post_save, sender=rating)
@receiver(post_delete, sender=rating)
def update_ai_marks(sender, instance, **kwargs):
    ai_instance = instance.aif
    ratings = rating.objects.filter(aif=ai_instance)
    average_rating = ratings.aggregate(models.Avg('value'))['value__avg'] or 0
    ai_instance.marks = average_rating
    ai_instance.save()

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=False,)
    product_id = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')
    transaction_time = models.DateTimeField(auto_now_add=True)
    return_url = models.CharField(max_length=1000,null=True)
    operation = models.CharField(max_length=100, blank=True, default='充值')  # 保存操作类型
    note =  models.CharField(max_length=100, blank=True, default='无')
    def __str__(self):
        return self.id
    

class ModelAccess(models.Model): #模型访问权限
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=False) #对应访问权限的所有者
    engine = models.ForeignKey('aiEngine',on_delete=models.CASCADE,null=False) #权限对应的ai引擎
    expireTime = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False,null=False)


class promptAccess(models.Model): #prompt访问权限
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=False) #对应访问权限的所有者
    aiPrompt = models.ForeignKey('ai',on_delete=models.CASCADE,null=False) #权限对应的prompt
    payed = models.BooleanField(default=False,null=False) #是否已支付

class creditBuyHistory(models.Model): #积分购买记录
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=False) #对应访问权限的所有者
    credits = models.IntegerField(default=5,null=True) #此次购买量
    payed = models.BooleanField(default=False,null=False) #是否已支付
    price = models.IntegerField(default=68,null=False)
    settled = models.BooleanField(default=True,null=False)#是否已经发放

class creditHistory(models.Model):#用户积分变更记录
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=False) #对应访问权限的所有者
    credits = models.IntegerField(default=5,null=True) #此次变化量
    descriptionText = models.TextField(max_length=80,null=False,default='变化')#变化的描述
    
class modelHistory(models.Model):#模型访问变更记录
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=False) #对应访问权限的所有者
    engine = models.ForeignKey('aiEngine',on_delete=models.CASCADE,null=False) #权限对应的ai引擎
    eventTime = models.DateTimeField(auto_now=True,null=False)
    modifyTime = models.IntegerField(default=30,null=False)
