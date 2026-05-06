from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('verify-otp/<int:order_id>/', views.verify_otp, name='verify_otp'),
    path('resend-otp/<int:order_id>/', views.resend_otp, name='resend_otp'),
]
