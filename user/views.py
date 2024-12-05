import os
import re

from django.http import FileResponse
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from market01.settings import MEDIA_ROOT
from user.models import User, Address
from user.permission import UserPermission, AddressPermission
from user.serializers import UserSerializer, AddressSerializer
from user.smtp_message import send_test_email
from common.verify_code import verify_code


# Create your views here.
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定义登录成功后的返回结果
        result = serializer.validated_data
        result['id'] = serializer.user.id
        result['mobile'] = serializer.user.mobile
        result['email'] = serializer.user.email
        result['username'] = serializer.user.username
        result['token'] = result.pop('access')

        return Response(result, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        """
        注册：
        1.接受用户参数
        2.校验
        3.创建用户
        """
        # 1.接受用户参数
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')
        # 2.校验参数是否为空
        if not all([username, email, password, password_confirmation]):
            return Response({'error': '参数不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 3.校验用户名是否已存在
        if User.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 4.校验两次密码是否一致
        if password != password_confirmation:
            return Response({'error': '两次密码不一致'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 5.校验密码长度
        if not 6 <= len(password) <= 18:
            return Response({'error': '密码长度不符合要求'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 6.校验邮箱是否被占用
        if User.objects.filter(email=email).exists():
            return Response({'error': '该邮箱已被占用'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 7.校验邮箱格式
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return Response({'error': '邮箱格式不正确'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 8.创建用户
        obj = User.objects.create_user(username=username, email=email, password=password)
        res = {
            'id': obj.id,
            'username': obj.username,
            'email': obj.email,
        }
        return Response(res, status=status.HTTP_201_CREATED)


class UserView(GenericViewSet, mixins.RetrieveModelMixin):
    """用户相关操作视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 设置认证用户才能访问
    permission_classes = (IsAuthenticated, UserPermission,)

    def upload_avatar(self, request, *args, **kwargs):
        """上传用户头像"""
        avatar = request.data.get('avatar')
        # 校验文件是否为空
        if not avatar:
            return Response({'error': '文件不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验文件大小，不能超过300kb
        if avatar.size > 1024 * 300:
            return Response({'error': '文件大小不能超过300kb'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 保存文件
        user = self.get_object()
        serializer = self.get_serializer(user, data={'avatar': avatar}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'urls': serializer.data['avatar']}, status=status.HTTP_200_OK)


class FileView(APIView):
    """获取文件的视图"""

    def get(self, request, name):
        path = MEDIA_ROOT / name
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)


class AddressView(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  ):
    """收货地址管理视图"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, AddressPermission]
    # 指定过滤字段
    filterset_fields = ['user', ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 通过请求过来的用户进行过滤
        queryset = queryset.filter(user=request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_default_address(self, request, *args, **kwargs):
        """设置默认收货地址"""
        # 获取要设置的地址对象
        obj = self.get_object()
        # 将该地址设置为默认地址，将其他地址设置为非默认
        obj.is_default = True
        obj.save()
        queryset = self.get_queryset().filter(user=request.user)
        for item in queryset:
            if item != obj:
                item.is_default = False
                item.save()
        return Response({'message': '设置成功'}, status=status.HTTP_200_OK)


class SMTPSendClass:
    def send_email(self, recipient, subject, message):
        send_test_email(recipient, subject, message)


class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        curr_user = request.user
        curr_recipient = curr_user.email
        if not curr_recipient:
            return Response({'error': '当前用户无邮箱'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        subject = '测试邮件'
        message = '邮件验证码为' + verify_code()
        # 测试邮箱
        view_instance = SMTPSendClass()
        view_instance.send_email(curr_recipient, subject, message)
        # 测试邮箱
        return Response({'message': '邮件发送成功'}, status=status.HTTP_200_OK)
