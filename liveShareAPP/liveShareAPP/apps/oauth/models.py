from django.db import models
from liveShareAPP.utils.models import BaseModel
from users.models import User


class OauthUser(BaseModel):
    """
    QQ登录模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    openid = models.CharField(max_length=64, verbose_name="openid",db_index=True)

    class Meta:
        db_table = "live_oauth_qq"
        verbose_name = "qq登录"
        verbose_name_plural = verbose_name