from rest_framework import generics
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from django.db.models import Sum


class BaseTransactionAPIView(generics.GenericAPIView):
    """Base para views de transações."""    
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

class TransactionListCreateAPIView(BaseTransactionAPIView, generics.ListCreateAPIView):
    """Cria e lista transações"""
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_filds = ['type', 'date', 'categry']
    ordering_fields = ['date', 'value']
    search_fields = ['description']
    

class TransactionRetrieveUpdateDeleteAPIView(BaseTransactionAPIView, generics.RetrieveUpdateDestroyAPIView):
    """Detalha, Atualiza, deleta uma transação."""
    
class BaseCategoryAPIView(generics.GenericAPIView):
    """Base para views de categoria"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    

class CategoryListCreateAPIView(BaseCategoryAPIView, generics.ListCreateAPIView):
    """Lista ou Cria categorias."""


class CategoryRetrieveUpdateDeleteAPIView(BaseCategoryAPIView, generics.RetrieveUpdateDestroyAPIView):
    """Detalha, Atualiza ou Deleta uma categoria"""
    
    
class MonthlyReportAPIView(APIView):
    """
    Gera um relatorio mensal das transações (receita e despesas) de um usuário
    para o mês e ano especificados.
    Exemplo de URL: /report/2025/02/ para o fevereiro de 2025.
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, year, month):
        transaction = Transaction.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        )
        incomes = transaction.filter(type='income').aggregate(total=Sum('value'))['total'] or 0
        expenses = transaction.filter(type='expense').aggregate(total=Sum('value'))['total'] or 0
        balance = incomes - expenses
        
        expense_by_category = (
            transaction.filter(type='expense')
            .values('category__name')
            .annotate(total=Sum('value'))
            .order_by('category__name')
        )
        
        return Response({
            'year': year,
            'month': month,
            'incomes': incomes,
            'expenses': expenses,
            'balance': balance,
            'expense_by_category': [
                {'category': item['category__name'], 'total': item['total']}
                for item in expense_by_category
            ]
        })