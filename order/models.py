from django.db import models

from user.models import User


class Order(models.Model):
    long_id = models.CharField(verbose_name='订单号', max_length=20, unique=True)
    user = models.ForeignKey(verbose_name='所属用户', to=User, on_delete=models.CASCADE)
    status_choices = {
        (1, '待支付'),
        (2, '已支付'),
        (3, '已取消'),
    }
    status = models.SmallIntegerField(verbose_name='订单状态', choices=status_choices)
    amount = models.DecimalField(verbose_name='订单总金额', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    payed_at = models.DateTimeField(verbose_name='支付时间', auto_now=True)

    class Meta:
        db_table = 'order'
        verbose_name = '订单表'
