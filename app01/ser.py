from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app01.models import Admin,User,Goods,Category


class AdminSerializer(serializers.Serializer):
    #这不想要哪个字段 直接在类中注释掉哪个字段就是
    adminid = serializers.CharField()
    adminname = serializers.CharField(max_length=4,min_length=2)  #序列化器自带的校验功能 校验有三种 这是其中之一
    # 校验规则 1.钩子函数，分为局部与全局函数  2.利用自带的几种简单的校验规则 如上  3.在用validate在序列化时候校验，自己写函数，
    #3不常用

    #这里也可readonly与writeonly的使用，反序列化时候不穿过去
    adminpassword = serializers.CharField()
    adminsex = serializers.CharField()

    def validate_adminname(self,data): #需要接受一个参数 ,这个data其实就是validate_adminname的adminname
        # print(data)


        return data   #需要有返回值 不然报错

    def validate_adminsex(self,data):    #局部校验，校验性别的局部钩子
        #如果性别不是男或者女  校验失败
        # print(data)
        # print(type(data))
        if data=="男" or data == '女':
            return data
        else:
            #抛出异常
            raise ValidationError("性别只能为男或女")

    def validate(self, validate_data):  #全局钩子  逻辑可以自己实现
        # print(validate_data)    #这里就是字典集合 ，包含了所有前端传过来的数据
        adminid=validate_data.get('adminid')
        adminpassword = validate_data.get('adminpassword')

        if adminid==adminpassword:
            raise ValidationError('id与密码一致')
        else:
            return validate_data




    # 修改需要重写update方法
    def update(self, instance, validated_data):
        # instance是admin对象
        # validated_data是校验后的数据
        instance.adminid=validated_data.get('adminid')
        instance.adminname = validated_data.get('adminname')
        instance.adminpassword=validated_data.get('adminpassword')
        instance.adminsex = validated_data.get('adminsex')
        instance.save()  #admin.save() orm提供的

        #这里其实拿到东西后开始处理逻辑 就行 ，可以是对0 1判断之后再进行存储
        #或者是针对于树形数据进行存储
        return instance

    # 新增要重写create方法
    def create(self, validated_data):

        instance=Admin.objects.create(**validated_data)#全部字段都用的话 这句就行 否则一句一句的写
        # instance.adminid=Admin.objects.create(adminid=validated_data.get('adminid'))
        # instance.adminname=Admin.objects.create(adminname = validated_data.get('adminname'))
        # instance.adminpassword=Admin.objects.create(adminpassword=validated_data.get('adminpassword'))
        # instance.adminsex=Admin.objects.create(adminsex = validated_data.get('adminsex'))

        return instance



#用户表 该法用继承ModelSerializer
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=User   #对应model里面的模型
        fields='__all__'   #全部序列化
        # fields=["","",""]    #序列化指定的字段即可
        #exclude 排除 还有一个extra_kwargs 指定只读、只写

    #如果用模型序列化器的话 update和create方法已经重写过了


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['categoryid','categoryname']



class GoodsSerializer(serializers.Serializer):
    # 其实在理影藏了GOODS对象，goodsid就等于Goods.goods.id,source就是可以改 给家了对象
    #source的用法 1.改名字，让俩字段不一样 2.连表查询 3.括号里执行一个方法 ,P18 min36
    goodsid = serializers.CharField()
    goodsname = serializers.CharField()
    # status = serializers.CharField(source="goodsstatus")#修改名称
    status=serializers.SerializerMethodField()
    def get_status(self, instance):
        finstatus=''
        if instance.goodsstatus==0:
            finstatus="未出售"
        elif instance.goodsstatus==1:
            finstatus="已出售"
        return finstatus


    # checkstate= serializers.CharField()  原来写法
    checkstate=serializers.SerializerMethodField()
    #加入逻辑判断  返回审核状态
    def get_checkstate(self, instance):
        finstate=''
        # print(type(instance))
        # print(instance.checkstate)
        if instance.checkstate==0:
            finstate="未审核"
        elif instance.checkstate==1:
            finstate="已审核"
        return finstate

    pic = serializers.CharField()
    issuetime = serializers.CharField()

    goodscategory = serializers.CharField(source='goodscate.categoryname')  #连表显示 goods.goodscate.categoryname
    #如果修改model里面的方法 显示数码产品相当于调用 goods对象的类别对象的__str__方法 所有那样显示

    # issueperson = serializers.CharField(source='issueperson.username')

    #拿出所有发布者
    issueperson=serializers.SerializerMethodField()
    # SerializerMethodField需要一个配套方法，方法名有讲究，且返回值就是显示值
    def get_issueperson(self, instance):
        ll=[]
        issueperson=instance.issueperson  #取出所有发布者
        # print(issueperson)
        # print(type(issueperson))
        ll.append({'issueid':issueperson.userid})
        ll.append({'issuename': issueperson.username})
        # for i in issueperson:
        #     ll.append({'id':i.userid,"name":i.username})
        return ll


