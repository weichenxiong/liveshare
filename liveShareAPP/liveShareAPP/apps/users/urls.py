from django.urls import path, include,re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('login/', obtain_jwt_token), #　用户登录
    path("captcha/", views.CaptchaAPIView.as_view()), # 滑动验证码
    path("register/", views.Register.as_view()), # 注册模块
    re_path("sms/(?P<mobile>1[3-9]\d{9})/", views.SMSAPIView.as_view()), # 短信模块
    path("email/", views.SetPasswordByEmail.as_view()) # 邮件改密码


]