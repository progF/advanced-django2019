from django.urls import path
# from rest_framework_jwt.views import obtain_jwt_token
from core.views import ProjectViewSet, ProjectDetailViewSet
from rest_framework import routers

urlpatterns = [
    path('projects/', ProjectViewSet.as_view({'get':'list','post':'create'}), name='available-projects'),
    path('projects/', ProjectDetailViewSet.as_view({
        'put':'update',
        'delete':'destroy'
    }), name='detailed-project')
]
# router = routers.DefaultRouter()
# router.register('projects', ProjectViewSet, base_name='core')
# urlpatterns += router.urls