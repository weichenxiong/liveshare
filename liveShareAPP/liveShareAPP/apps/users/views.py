"""
__ author__: wcx
date:2020-05-01
version:1.0
"""

import json
import random
from rest_framework.views import APIView
from django.conf import settings
from urllib.parse import urlencode
from urllib.request import urlopen
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from .serializers import UserModelSerializer
from .models import User
from liveShareAPP.libs.yuntongxun.sms import CCP
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.core.mail import send_mail
import re
from rest_framework import serializers
from django_redis import get_redis_connection
from mycelery.sms.tasks import *


# 滑动验证码模块
class CaptchaAPIView(APIView):

    def get(self, request):
        AppSecretKey = settings.TENCENT_CAPTCHA["App_Secret_Key"]
        appid = settings.TENCENT_CAPTCHA["APPID"]
        Ticket = request.query_params.get("ticket")
        Randstr = request.query_params.get("randstr")
        UserIP = request._request.META.get("REMOTE_ADDR")
        params = {
            "aid": appid,
            "AppSecretKey": AppSecretKey,
            "Ticket": Ticket,
            "Randstr": Randstr,
            "UserIP": UserIP
        }
        params = urlencode(params)

        f = urlopen("%s?%s" % (settings.TENCENT_CAPTCHA["GATEWAY"], params))
        content = f.read()
        res = json.loads(content)
        print(res)
        if res:
            error_code = res["response"]
            if error_code == "16":
                return Response("验证通过！")
            else:
                return Response("验证失败！%s" % res["err_msg"], status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("验证失败！", status=status.HTTP_400_BAD_REQUEST)

# 用户注册模块
class Register(CreateAPIView):
    """
    用户注册模块
    """
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

#短信发送模块
class SMSAPIView(APIView):
    """
    短信发送模块
    """
    def get(self, request, mobile):
        print("mobile:",mobile)
        redis_conn = get_redis_connection("sms_code")
        #手机号是否处于发送短信的冷却时间内
        interval = redis_conn.get("sms_time_%s" %mobile)
        if interval is not None:
            return Response("不能频繁发生短信！")
        #生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        # print("短信验证码：", sms_code)
        #保存短信验证码与发生记录
        #使用redis提供的管道操作可以一次执行多条命令
        pl = redis_conn.pipeline()
        pl.multi()
        pl.setex("sms_%s" % mobile, 300, sms_code) # 设置短信的有效期
        pl.setex("sms_time_%s" % mobile, 60, "_") # 设置发生短信间隔时间为60秒
        pl.execute()
        # 1.发送短信验证码
        ccp = CCP()
        ccp.send_template_sms(mobile, [sms_code, 300//60], settings.SMS.get("_templateID"))
        # 2.使用celery发送短信
        # 发送短信验证码
        send_sms.delay(mobile, sms_code)
        # print("发送短信成功！")
        return Response({"message":"发送短息OK"}, status=status.HTTP_200_OK)

#邮件改密码
class SetPasswordByEmail(APIView):
    def get(self, request):
        """发送找回密码的链接地址"""
        #检测用户是否存在
        email = request.query_params.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("当前邮箱对应的用户不存在！")
        #生成找回密码的链接
        serializer = Serializer(settings.SECRET_KEY, 2 * 60 * 60)
        #dumps的返回值是加密的bytes信息
        access_token = serializer.dumps({"email":email}).decode()
        url = settings.CLIENT_HOST + "/user/set_password_by_email?access_token=" + access_token

        # 1.使用django提供的email发送短信
        send_mail(subject="找回密码",message="",from_email=settings.EMAIL_FROM,recipient_list=['1980575315@qq.com'],html_message='<a href="%s" target="_blank">重置密码</a>' % url)
        # 2. 使用celery 异步发送，因为测试代码时候每次都要启动celery，麻烦，所以先不用celery,一旦上线了用celery了，就注释上面一行代码．
        # 启动下面一行代码：send_email.delay([email], url)
        # send_email.delay([email], url)
        return Response("邮件已经发送，请留意您的邮箱")

    def post(self, request):
        #验证邮箱地址中的access_token是否正确且在有效期内
        access_token = request.data.get("access_token")
        serializer = Serializer(settings.SECRET_KEY, 2 * 60 * 60)
        try:
            data = serializer.loads(access_token)
            return Response({"email":data.get("email")})
        except BadData:
            #access_token过期或者错误
            return Response("重置密码的邮件已过期或者邮件地址有误！", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # 重置密码
        # 再次从access_token获取用户信息
        access_token = request.data.get('access_token')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        #判斷密碼和確認密碼是否一致
        if len(password) < 3 or len(password) > 16:
            return Response("密碼長度有誤!",status=status.HTTP_400_BAD_REQUEST)
        if password != password2:
            return Response("兩次密碼不一致!",status=status.HTTP_400_BAD_REQUEST)
        serializer = Serializer(settings.SECRET_KEY,5 * 60 * 60)
        try:
            data = serializer.loads(access_token)
        except BadData:
            #access_token過期或者錯誤
            return Response('重置密碼的郵件已過期或者郵件地址有誤!',status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email')
        #獲取用戶信息
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("重置密碼失敗!郵箱地址有誤!",status=status.HTTP_400_BAD_REQUEST)
        #修改密碼
        user.set_password(password)
        user.save()
        return Response("重置密码成功！")

#手机改密
class SetPasswordByPhone(APIView):

    def get(self,request):
        mobile = request.data.get("mobile")
        password = request.data.get("password")
        password2 = request.data.get("password2")
        sms_code = request.data.get("sms_code")
        #验证手机号码格式
        if not re.match("^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError("手机号码格式错误！")
        #验证手机号是否注册
        try:
            user = User.objects.get(mobile=mobile)
            if user is None:
                raise serializers.ValidationError("该手机号未注册！")
        except User.DoesNotExist:
            pass
        #验证两个密码是否一致
        if password != password2:
            raise serializers.ValidationError("两次输入密码不一致！")
        #验证输入验证码是否一致
        redis_conn = get_redis_connection("sms_code")
        redis_sms = redis_conn.get("sms_%s" %mobile).decode()
        if redis_sms != sms_code:
            raise serializers.ValidationError("验证码不一致！")
        #保存数据
        try:
            user.set_password(password)
            user.save()
            redis_conn = get_redis_connection("sms_code")
            redis_conn.delete("sms_%s" %mobile)
            redis_conn.delete("sms_time_%s" %mobile)
        except:
            raise serializers.ValidationError("重置密码失败！")
        return Response("重置密码成功")



