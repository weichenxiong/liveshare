from django.urls import path
from . import views


urlpatterns = [
    path("qq/url/",views.OAuthQQAPIView.as_view()), # 生成ＱＱ链接功能
    path("qq/info/", views.QQInfoAPIView.as_view() ), # 获取用户信息
    path("qq/login/", views.BindQQUserAPIView.as_view() ), # 绑定用户信息
]