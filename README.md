# 对接文档
## 涉及到模块交互写这里
### Ai引擎访问模块：
通过 使用prompt 转入使用引擎时，请通过GET方式向我的url传递一个可以唯一标示prompt数据的标识符。
使用方法：href地址设置为`"/chat?engine=0&promptID=123445"`
其中，`engine`范围为0-3，对应max,lite,pro,4.0四种模型；`promptID`为一个能够唯一标识prompt内容的ID字段，请由调用者说明对应数据库字段或实现传入参数为promptID的函数接口用于返回prompt文本

### 用户登陆态获取:`getUser(request)`:
直接传入`request`对象，该函数会自动解析用户id 返回用户对象
成功返回用户对象
失败返回`None`
老接口不会弃用，但是不再推荐使用

### 用户积分获取与变更：
  `modifyCredits(user:UserAccount,creditsChange=0,sudo:bool = False,descrip:str = '默认消息'):
`

传入用户对象。调用成功返回用户剩余`credits`。失败返回`None`,操作后余额小于零且非超级操作（`sudo=False`)则不进行操作并返回字符串类型‘余额不足’；操作后余额小于零且为超级操作则会正常将数字降低到0以下并返回余额。获取金额请令`creditsChange`参数为0或留空
消费积分请传入负值，增加传入正值

创建订单的方式：http://127.0.0.1:8000/order/api/create_order/?product_id=商品名称/编号&amount=648&return_url=https://www.baidu.com(回调地址)


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

## 关于支付接口：
转到地址: `/checkout/<str:checkoutType>?product=114514&price=114514&returnUrl='www.baidu.com'`
其中: `checkoutType`参数允许值为`prompt` , `engine` , `credit`
`prompt`: `checkout/prompt?product=114514&price=114514` product为aiPrompt标识符,price为价格
`credit`: `checkout/credit?product=114514&price=114514`  product为购买的点数数量,price为价格
`engine`: `checkout/engine?product=400005&price=114514`  product为购买的engineID和使用次数,构成方法为使用次数*10+engineID。price为价格

returnUrl为回调地址
不传递上述参数时判定为订单校验模式

接口只支持get方式