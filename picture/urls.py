from django.urls import path
from picture import views

urlpatterns = [
    path('', views.picture, name='picture'),
    path('<int:picture_pk>/', views.picture_detail, name='picture_detail'),
]