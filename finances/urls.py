from django.urls import path
from .views import (
    TransactionListCreateAPIView, TransactionRetrieveUpdateDeleteAPIView,
    CategoryListCreateAPIView, CategoryRetrieveUpdateDeleteAPIView,
    MonthlyReportAPIView
)

urlpatterns = [
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDeleteAPIView.as_view(), name='transaction-detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteAPIView.as_view(), name='category-detail'),
    path('report/<int:year>/<int:month>/', MonthlyReportAPIView.as_view(), name='monthly-report')
]
