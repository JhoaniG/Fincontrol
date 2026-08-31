from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Credit, Saving, Expense
import datetime

@receiver(post_save, sender=Credit)
def sync_credit_to_expense(sender, instance, created, **kwargs):
    if created:
        today = datetime.date.today()
        # Generar un registro de gasto por la cuota mensual del crédito
        Expense.objects.create(
            user=instance.user,
            category='deuda',
            sub_category=f"Cuota {instance.bank} - {instance.product}",
            amount=instance.monthly_fee,
            month=today.month,
            year=today.year,
            description=f"Pago automático de deuda registrada el día {instance.payment_day}"
        )

@receiver(post_save, sender=Saving)
def sync_saving_to_expense(sender, instance, created, **kwargs):
    if created:
        today = datetime.date.today()
        # Generar un registro de gasto por el valor mensual del ahorro
        Expense.objects.create(
            user=instance.user,
            category='ahorro',
            sub_category=f"Ahorro {instance.bank} - {instance.saving_type}",
            amount=instance.monthly_value,
            month=today.month,
            year=today.year,
            description="Transferencia automática a ahorro"
        )
