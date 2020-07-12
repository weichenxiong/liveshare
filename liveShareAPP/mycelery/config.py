# 任务队列的链接地址
broker_url = 'redis://127.0.0.1:6379/15'
# 结果队列的链接地址
result_backend = 'redis://127.0.0.1:6379/14'

from celery.schedules import crontab
from .main import app
#定时任务的调度列表，用于注册定时任务
app.conf.beat_schedule = {
    'write_article_to_mysql': {
        # 本次定时调度的任务
        'task': 'write_article', # 这里的任务名称必须先到main.py中注册
        # 定时任务的调度周期
        # 'schedule': 120,   # 每120秒执行
        'schedule': crontab(hour=3),   # 每天凌晨3点
      	# 'args': (16, 16),  # 注意：任务就是一个函数，所以如果有参数则需要传递
    },
}