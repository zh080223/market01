from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

import traceback
from user.smtp_message import send_test_email


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        recipient = '402306174@qq.com'
        subject = '网站出错啦！！！'
        message = traceback.format_exc()
        send_test_email(recipient, subject, message)
        return HttpResponse('对不起，网页出错了，请稍后再试')
