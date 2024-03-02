
from django.urls import path
from .views import ProductAPIView, LessonListAPIView, GroupListAPIView

urlpatterns = [
    path('',ProductAPIView.as_view()),
    path('products/<str:product_name>/', LessonListAPIView.as_view(), name='product_lessons'),
    path('groups/', GroupListAPIView.as_view(), name='group-list'),

]