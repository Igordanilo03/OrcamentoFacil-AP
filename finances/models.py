from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    TYPE_CHOICES = (
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    )
    description = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.description} ({self.type})"
    
    