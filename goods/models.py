from django.db import models


# Create your models here.
class Goods(models.Model):
    name = models.CharField(verbose_name='商品名称', max_length=50)
    details = models.TextField(verbose_name='商品详情')
    # image = models.ImageField(verbose_name='商品图片', upload_to='goods/')
    price = models.FloatField(verbose_name='价格')
    remain = models.IntegerField(verbose_name='库存量')
    status = models.BooleanField(verbose_name='是否在架', default=True)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'goods'
        verbose_name = '商品表'

