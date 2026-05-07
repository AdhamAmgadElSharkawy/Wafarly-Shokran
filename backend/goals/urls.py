from django.urls import path
from . import views

urlpatterns = [
    # your goal URLs will go here
    path('', views.goal_list, name='goal_list'),
    path('create/', views.goal_create, name='goal_create'),
    path('edit/<int:pk>/', views.goal_edit, name='goal_edit'),
    path('delete/<int:pk>/', views.goal_delete, name='goal_delete'),
    path('add_funds/<int:pk>/', views.add_funds, name='add_funds'),
]