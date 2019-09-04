from django.urls import path
from . import views


urlpatterns = [
    path('reviews/<int:pk>/', views.get_reviews),
    path('user_reviews/', views.get_user_reviews),
    path('user_reviews/<int:pk>/', views.users_review_detail),
    path('add_review/<int:pk>/', views.createReview),
]
