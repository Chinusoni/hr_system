from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('request-leave/', views.submit_leave_request, name='request_leave'),
    path('success/', views.leave_request_success, name='leave_success'), 
    path('register/', views.register_employee, name='register'),
    path('export-csv/', views.export_leaves_csv, name='export_csv'),
]