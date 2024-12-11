import traceback

from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework import status

from user.smtp_message import send_test_email


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        recipient = '402306174@qq.com'
        subject = '网站出错啦！！！'
        # 捕获异常
        message = traceback.format_exc()
        # send_test_email(recipient, subject, message)
        return Response({'error': '网站出错了，请稍后再试！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
