from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostsListView.as_view(), name='index'),
    path('add/', views.PostsCreateView.as_view(), name='add'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='single_post'),
]
