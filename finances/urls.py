from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('hormiga/', views.hormiga_view, name='hormiga'),
    path('upgrades/', views.upgrades_view, name='upgrades'),
    path('anual/', views.yearly_summary_view, name='yearly_summary'),
    path('delete/<str:item_type>/<int:item_id>/', views.delete_transaction, name='delete_transaction'),
]
