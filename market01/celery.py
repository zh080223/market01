import os

from celery import Celery
from market01.settings import INSTALLED_APPS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market01.settings')

app = Celery('market01')
app.conf.update(
    broker_url='redis://:803618@127.0.0.1:6379/0',
    broker_connection_retry_on_startup=True,
)

# 自动去注册的应用下寻找加载worker函数
app.autodiscover_tasks([INSTALLED_APPS[-4]])
