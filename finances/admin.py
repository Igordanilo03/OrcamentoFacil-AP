from django.contrib import admin
from finances.models import Transaction, Category


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('description', 'value', 'date', 'type', 'category', 'user')
    search_fields = ('description', 'category',)
    ordering = ('-date',)
    

admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Transaction, TransactionModelAdmin)
