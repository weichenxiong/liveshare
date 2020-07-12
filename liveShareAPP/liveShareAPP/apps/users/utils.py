from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q
import re


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token:
    :param user:
    :param request:
    :return:
    """
    print("http://api.liveshare.cn:8000"+user.avatar.url)
    return {
        "token": token,
        "id": user.id,
        "username": user.username,
        "avatar": "http://api.liveshare.cn:8000"+user.avatar.url,
        "nickname": user.nickname
    }


def get_user_account(account):
    """
    获取账号信息
    :param account:
    :return:
    """
    try:
        user = User.objects.get(Q(mobile=account) | Q(email=account) | Q(username=account))
    except User.DoesNotExist:
        user = None

    return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    登录验证账号密码
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        #改写authenticate方法
        user = get_user_account(username)
        #账号通过了还要进行密码验证，判断当前账号是否激活
        if isinstance(user, User) and user.check_password(password) and self.user_can_authenticate(user):
            return user


