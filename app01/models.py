from django.db import models

# Create your models here.

class User(models.Model):#用户表
    userid = models.CharField(max_length=32,unique=True)  #主键
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)#用id、昵称 密码


class Admin(models.Model):#管理员表，继承
    adminid=models.IntegerField(primary_key=True) #主键
    adminname=models.CharField(max_length=32)
    adminpassword=models.CharField(max_length=32)
    adminsex=models.CharField(max_length=32)


# #用户表
# class User(models.Model):
#     pass

#商品表
class Goods(models.Model):
    goodsid=models.CharField(max_length=32,primary_key=True)   #商品号为主键
    goodsname=models.CharField(max_length=64)
    goodsstatus=models.IntegerField()    #0 表示未卖出，1表示卖出
    checkstate=models.IntegerField()    #0 表示未审核，1表示审核
    pic=models.CharField(max_length=128)
    issuetime=models.DateField()    # null=true表示可为空

    #外键
    goodscate=models.ForeignKey('Category',to_field='categoryid',on_delete='CASCADE',null=True)   #d对应外键种类表的种类，CASCADE级联删除
    issueperson=models.ForeignKey('User',to_field='userid',on_delete='CASCADE')  #对应用户表的外键



#类别表
class Category(models.Model):
    categoryid=models.IntegerField(primary_key=True) #主键 以900开头，9001 9002
    categoryname=models.CharField(max_length=32)

    # def __str__(self):
    #     return self.categoryname

        # return self.categoryname+'cccc'

# #交易状态
# class Trade_state(models.Model):
#     pass

# #商品评论表
# class Goods_comments(models.Model):
#     pass


# #交易信息
# class Trade_info(models.Model):
#     pass
