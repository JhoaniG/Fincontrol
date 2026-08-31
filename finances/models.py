from django.db import models
from django.conf import settings

class Income(models.Model):
    INCOME_TYPES = (
        ('fijo', 'Fijo'),
        ('variable', 'Variable'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incomes')
    type = models.CharField(max_length=20, choices=INCOME_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    periodicity = models.CharField(max_length=50, blank=True, null=True) # Ej: Mensual, Quincenal
    month = models.IntegerField()
    year = models.IntegerField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.month}/{self.year}"

class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('esencial', 'Esencial'),
        ('no_esencial', 'No Esencial'),
        ('deuda', 'Deuda'),
        ('ahorro', 'Ahorro'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=100) # Ej: Arriendo, Alimentación
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.sub_category} - {self.amount}"

class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credits')
    bank = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    payment_day = models.IntegerField()
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2) # Ej: 1.5 %
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2)
    total_months = models.IntegerField()
    total_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_interests = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank} - {self.product}"

class Saving(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings')
    bank = models.CharField(max_length=100, default='Banco')
    saving_type = models.CharField(max_length=200, default='Ahorro')
    monthly_value = models.DecimalField(max_digits=12, decimal_places=2)
    total_time_months = models.IntegerField(null=True, blank=True)
    yield_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_saving = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank} - {self.saving_type}"

class AntExpense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ant_expenses')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hormiga - {self.amount} - {self.date}"
