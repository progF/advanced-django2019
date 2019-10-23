from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from users.views import RegisterViewSet
from rest_framework import routers

urlpatterns = [
    path('login/', obtain_jwt_token),
]
router = routers.DefaultRouter()
router.register('register', RegisterViewSet, base_name='users')
urlpatterns += router.urls