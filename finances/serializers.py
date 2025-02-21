from rest_framework import serializers
from .models import Transaction, Category
from datetime import date


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError('O nome da categoria é obrigatório."')
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = instance.user
        return super().update(instance, validated_data)
        

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'description', 'value', 'date', 'type', 'category']
        
    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError('O valor não pode ser menor que zero.')
        return value
    
    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError('A data não pode ser futura.')
        return value
    
    def validate(self, data):
        data['user'] = self.context['request'].user
        if data['type'] == 'expense' and not data.get('category'):
            raise serializers.ValidationError('Despesas devem ter uma categoria.')
        return data
        
        