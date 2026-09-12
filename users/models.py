from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ACTIVITY_CHOICES = (
        ('empleado', 'Empleado'),
        ('independiente', 'Independiente'),
    )
    CURRENCY_CHOICES = (
        ('COP', 'Pesos Colombianos (COP)'),
        ('USD', 'Dólares (USD)'),
        ('EUR', 'Euros (EUR)'),
    )
    birth_date = models.DateField(null=True, blank=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='empleado')
    preferred_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='COP')
    is_verified = models.BooleanField(default=False) # Para validación OTP inicial

    def __str__(self):
        return self.username

class OTPVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='otp')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.username}"

class Subscription(models.Model):
    PLAN_CHOICES = (
        ('monthly', 'Mensual ($40 USD)'),
        ('annual', 'Anual ($400 USD)'),
    )
    STATUS_CHOICES = (
        ('active', 'Activa'),
        ('canceled', 'Cancelada'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='monthly')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    next_billing_date = models.DateField(null=True, blank=True)
    wompi_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({self.status})"
