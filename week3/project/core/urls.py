from django.urls import path
from core.views import (
    ProjectListAPIView,
    ProjectDetailAPIView,
    BlockListView,
    BlockDetailAPIView,
    TaskListView,
    TaskDetailAPIView,
    DocumentListViewSet
)
from rest_framework import routers


urlpatterns = [
    path('all/', ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view()),
    path('projects/<int:pk>/blocks/', BlockListView.as_view()),
    path('blocks/<int:type>/', BlockDetailAPIView.as_view()),
    path('blocks/<int:type>/tasks/', TaskListView.as_view()),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view()),
]

router = routers.DefaultRouter()
router.register('documents', DocumentListViewSet, base_name='core')

urlpatterns += router.urls