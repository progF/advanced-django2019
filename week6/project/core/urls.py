from django.urls import path
from core.views import (
    ProjectViewSet,
    ProjectDetailViewSet,
    get_blocks_by_project,
    create_new_task
)
from rest_framework import routers

urlpatterns = [
    path('projects/', ProjectViewSet.as_view({'get':'list','post':'create'}), name='available-projects'),
    path('projects/<int:pk>/', ProjectDetailViewSet.as_view({
        'put':'update',
        'delete':'destroy'
    }), name='detailed-project'),
    path('project/', get_blocks_by_project),
    path('tasks/', create_new_task),
]
# router = routers.DefaultRouter()
# router.register('projects', ProjectViewSet, base_name='core')
# urlpatterns += router.urls