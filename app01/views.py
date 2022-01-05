from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# 导入自己写的相应信息
from app01.utils import MsgResponse
# Create your views here.

def index(request):
    #业务逻辑


    #返回结果
    #return HttpResponse('INDEX') #返回一个字符串
    return render(request,'index.html')

def login(request):

    # print(request.type(request))
    # print(request.method,type(request.method))

    if  request.method=='POST':
        # print(request.POST,type(request.POST))
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        # print(user,pwd)
        #if user=="fuqc" and pwd =="123":
        if models.User.objects.filter(username=user,password=pwd):
            # return HttpResponse("chenggong")
            return redirect('/index/')
            # return redirect("http://www.baidu.com")  可以返回地址或者路径 都是可以的

    return render(request,'login.html')


def test(request): #c测试方法

    ret=models.User.objects.all()  #获取表中所哟数据，返回的是一个对象 列表 打印如下
    for i in ret:
        print(i.userid,i.username,i.password,type(i.userid))
    print(ret,type(ret))


    #ret=models.User.objects.get(username='fuqc',password='123') #获取数据 返回对象  ；但获取不到；或者多条数据会报错

    #ret=models.User.objects.filter()  #获取满足条件的对象列表 返回一个对象、空对象、


    return render(request,'test.html')



from rest_framework.views import APIView
from app01.models import Admin,User,Category,Goods
from app01.ser import AdminSerializer,GoodsSerializer
from app01.ser import UserModelSerializer,CategoryModelSerializer
from rest_framework.response import Response
from django.http import JsonResponse

class AdminView(APIView):    #继承APIview

    #Admin视图的Get 请求
    def get(self,request,pk):
        admin=Admin.objects.filter(adminid=pk).first()   #adminid对应model里面的字段名字
        # 实例化对象
        admin_ser=AdminSerializer(admin)

        #admin.data是序列化后的字典 还不是json数据
        return Response(admin_ser.data)

        #使用JsonResponse返回的就是json字符串，如果用这个 setting里就就可以不注册框架名字
        # 用上面的它自带的respnse就需要注册
        # return JsonResponse(admin_ser.data)



        #修改
    def put(self,request,pk):    #修改需要重写序列化器的父类下的update 方法
        response_msg={'status':100,'msg':'success'}
        #定位到该对象上来
        admin = Admin.objects.filter(adminid=pk).first()
        # 实例化该对象
        # admin_ser=AdminSerializer(admin,request.data)  最好如下写法
        admin_ser = AdminSerializer(instance=admin,data= request.data)

        if admin_ser.is_valid():#判断提交的是否为空
            admin_ser.save()
            response_msg['data']=admin_ser.data

        else:
            response_msg['status']=401
            response_msg['msg']="数据校验失败"
            response_msg['data']=admin_ser.errors

        return Response(response_msg)


    def delete(self,request,pk):
        #删除数据
        res=MsgResponse()
        ret=Admin.objects.filter(pk=pk).delete()
        return  Response(res.get_dict)






class AdminsView(APIView):    #继承APIview,查所有的
    # 查所有的
    #老写法
    # def get(self,request):
    #     response_msg = {'status': 100, 'msg': 'success'}
    #     admins=Admin.objects.all()
    #     admin_ser=AdminSerializer(admins,many=True)   #序列化多条，many=true,一条的话不用的
    #     response_msg['data'] = admin_ser.data
    #
    #     return Response(response_msg)

        # noinspection PyUnreachableCode
    def get(self, request):
        res=MsgResponse()
        admins = Admin.objects.all()
        admin_ser = AdminSerializer(admins, many=True)  # 序列化多条，many=true,一条的话不用的
        res.data= admin_ser.data

        return Response(res.get_dict)


        # 新增
        # noinspection PyUnreachableCode
    def post(self, request):
        # 修改才有instance 新增没有
        response_msg = {'status': 100, 'msg': 'success'}
        # admin_ser=AdminSerializer(request.data)
        # 第一个默认参数为instance，上面这样写报错
        admin_ser = AdminSerializer(data=request.data)

        if admin_ser.is_valid():  # 判断提交的数据是否为空
            admin_ser.save()
            response_msg['data'] = admin_ser.data

        else:
            response_msg['status'] = 401
            response_msg['msg'] = "数据校验失败"
            response_msg['data'] = admin_ser.errors

        return Response(response_msg)



class UsersView(APIView):
    def get(self, request):
        res=MsgResponse()
        users = User.objects.all()
        user_ser = UserModelSerializer(users, many=True)  # 序列化多条，many=true,一条的话不用的
        res.data= user_ser.data

        return Response(res.get_dict)


class CategoryView(APIView):
    def get(self,request):
        res = MsgResponse()
        category=Category.objects.all()
        cate_ser=CategoryModelSerializer(category,many=True)
        res.data=cate_ser.data

        # 如果用模型序列化器的话 update和create方法已经重写过了

        return Response(res.get_dict)



class GoodsView(APIView):    #继承APIview

    #Goods视图的Get 请求
    def get(self,request,pk):
        good=Goods.objects.filter(goodsid=pk).first()   #adminid对应model里面的字段名字
        # 实例化对象
        print(good)
        good_ser=GoodsSerializer(good)

        return Response(good_ser.data)