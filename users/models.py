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
