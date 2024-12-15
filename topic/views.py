from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

# Create your views here.
class TopicView(View):

    def post(self, request, username):
        return JsonResponse({'code': 200})



