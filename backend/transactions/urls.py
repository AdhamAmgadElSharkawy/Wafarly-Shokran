from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_page, name='transactions'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('delete/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('edit/<int:id>/', views.edit_transaction, name='edit_transaction'),
]