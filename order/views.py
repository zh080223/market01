import time

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from alipay import AliPay
import alipay

app_private_key_string = open(settings.ALIPAY_KEY_DIRS + 'app_private_key.pem').read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIRS + 'alipay_public_key.pem').read()


class MyAlipayView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            app_notify_url=None,
            sign_type="RSA2",
            debug=True,  # True将请求转发沙箱
        )

    def get_pay_url(self, order_id, amount):
        order_string = self.alipay.api_alipay_trade_page_pay(
            subject=order_id,
            out_trade_no=order_id,
            total_amount=amount,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL,
        )
        return 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_string


# Create your views here.
class OrderView(MyAlipayView):

    def get(self, request):
        return render(request, 'pay.html')

    def post(self, request):
        order_id = int(time.time())
        pay_url = self.get_pay_url(order_id, 999)
        return JsonResponse({"pay_url": pay_url})
