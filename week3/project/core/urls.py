from django.urls import path
from core.views import ProjectListAPIView, ProjectDetailAPIView, BlockListView
from rest_framework import routers


urlpatterns = [
    path('all/', ProjectListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
    path('blocks/', BlockListView.as_view()),
]