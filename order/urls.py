from django.urls import path

from .views import OrderView

urlpatterns = [
    path('url/', OrderView.as_view()),
]
