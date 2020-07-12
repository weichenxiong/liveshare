from mycelery.main import app
import logging
from django.conf import settings
log = logging.getLogger("django")
from django.core.mail import send_mail

@app.task(name="send_email")
def send_email(recipient_list,url):
    """一部发生找回密码的邮件"""
    try:
        send_mail(subject="找回密码", message="", from_email=settings.EMAIL_FROM, recipient_list=recipient_list,
                  html_message='<a href="%s" target="_blank">重置密码</a>' % url)
        return Response("邮件已经发送，请留意您的邮箱")
    except:
        log.error("发生邮件失败！")