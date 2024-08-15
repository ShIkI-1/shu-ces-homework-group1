# 对接文档
## 涉及到模块交互写这里
### Ai引擎访问模块：
通过 使用prompt 转入使用引擎时，请通过GET方式向我的url传递一个可以唯一标示prompt数据的标识符。
使用方法：href地址设置为`"/chat?engineID=0&promptID=123445"`
其中，`engineID`范围为0-3，对应max,lite,pro,4.0四种模型；`promptID`为一个能够唯一标识prompt内容的ID字段，请由调用者说明对应数据库字段或实现传入参数为promptID的函数接口用于返回prompt文本

### 用户登陆态获取:`getUser(request)`:
直接传入`request`对象，该函数会自动解析用户id 返回用户对象
成功返回用户对象
失败返回`None`
老接口不会弃用，但是不再推荐使用

### 积分消费：
  `modifyCredits(user:UserAccount,creditsChange,sudo:bool = False):`

传入用户对象。尝试调用成功后会扣除余额 返回`True`。失败返回`False`,操作后余额小于零且非超级操作（`sudo=False`)则不进行操作并返回`False`；操作后余额小于零且为超级操作则会强制将余额置为负值。
消费积分请传入负值，增加传入正值

查询积分: `getCredits(user:UserAccount)`

### 我的订单
  /my_orders

### 呼出支付宝进行积分充值
创建订单的方式：/order/api/create_order/?product_id=商品名称/编号&amount=648&return_url=https://www.baidu.com(回调地址)

### ai详情页的调用：

进入ai的详情页的连接: /prompt/detail/{{x.id}}  其中x为ai表的一个对象 
具体可以参照ai_collect下的第57行代码的使用  (x的来源:views下的156行的函数 具体参数为list)

### 一些model模型的解释:

1.ai模型 ##主要用于detail的显示(发布时要进行信息的填充)

class ai(models.Model):  #差一些参数
    id = models.IntegerField(primary_key=True)  #所属id
    name = models.CharField(max_length = 255 )  #ai名字
    user = models.ForeignKey('UserAccount',on_delete=models.CASCADE,null=True,)  #所有者id 外键 便于删除操作 
    owner = models.CharField(max_length=255)  #所有者姓名
    brief = models.TextField()  #简介
    time = models.DateField(auto_now=True)  #发布时间
    marks = models.IntegerField(default=0) #评分
    #prompt = models.ForeignKey()   #ai对应的prompt训练模型
    level = models.IntegerField(default=0) #评论区总楼层 0视为没有评论

  负责编写发布的需要再发布的时候填写这些信息并且加上所使用的prompt模型 如果需要添加跟我联系探讨后添加

  ## 权限校验工具
`def grantModelAccess(user:UserAccount,number:int,engine:aiEngine):`ai引擎授权。user:userAccount对象，number为授权天数，engine为对应的引擎

`def checkModelAccess(request,engineID,prompt:ai=None):`通用引擎鉴权，检查对应engine，prompt是否均有权限。

`def grantPromptAccess(user:UserAccount,prompt:ai):`#授予prompt权限

`def checkPromptAccess(user:UserAccount,prompt:ai):` 检查有无prompt访问权限
