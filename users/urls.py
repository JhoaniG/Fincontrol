from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('otp-verify/<int:user_id>/', views.otp_verify_view, name='otp_verify'),
    path('api/hotmart-webhook/', views.hotmart_webhook, name='hotmart_webhook'),
    path('profile/', views.profile_view, name='profile'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('checkout/<str:plan>/', views.checkout_view, name='checkout'),
    path('cancel-subscription/', views.cancel_subscription_view, name='cancel_subscription'),
]
