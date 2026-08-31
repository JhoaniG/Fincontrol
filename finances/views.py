from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Income, Expense, Saving, AntExpense, Credit
import datetime

@login_required
def dashboard_view(request):
    user = request.user
    today = datetime.date.today()
    
    req_month = request.GET.get('month')
    req_year = request.GET.get('year')
    current_month = int(req_month) if req_month and req_month.isdigit() else today.month
    current_year = int(req_year) if req_year and req_year.isdigit() else today.year

    currency = getattr(user, 'preferred_currency', 'COP')
    currency_symbol = '$'
    if currency == 'EUR':
        currency_symbol = '€'
    elif currency == 'USD':
        currency_symbol = 'US$'
    elif currency == 'COP':
        currency_symbol = 'COP$'

    # 1. Ingresos del mes
    incomes = Income.objects.filter(user=user, month=current_month, year=current_year)
    income_total = incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    # 2. Gastos del mes
    expenses = Expense.objects.filter(user=user, month=current_month, year=current_year)
    expense_total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    essential_total = expenses.filter(category='esencial').aggregate(Sum('amount'))['amount__sum'] or 0
    non_essential_total = expenses.filter(category='no_esencial').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 3. Ahorro
    savings = Saving.objects.filter(user=user)
    saving_total = savings.aggregate(Sum('monthly_value'))['monthly_value__sum'] or 0

    # 4. Límites 50-30-20
    limit_50 = float(income_total) * 0.50
    limit_30 = float(income_total) * 0.30
    limit_20 = float(income_total) * 0.20

    # 5. Gastos Hormiga
    ant_expenses = AntExpense.objects.filter(user=user, date__month=current_month, date__year=current_year)
    ant_total = ant_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Límite del 5%
    ant_limit = float(income_total) * 0.05
    ant_alert = bool(float(ant_total) > ant_limit and float(income_total) > 0)

    # Detección de onboarding / nuevo mes
    user_has_history = Income.objects.filter(user=user).exists() or Expense.objects.filter(user=user).exists()
    if not user_has_history:
        is_new_user = True
        is_new_month = False
    else:
        is_new_user = False
        current_month_has_data = Income.objects.filter(user=user, month=current_month, year=current_year).exists() or \
                                 Expense.objects.filter(user=user, month=current_month, year=current_year).exists()
        is_new_month = not current_month_has_data

    # Historial de Transacciones (Últimos 10 en general)
    from itertools import chain
    from operator import attrgetter
    
    incomes_list = list(incomes)
    expenses_list = list(expenses)
    credits_list = list(Credit.objects.filter(user=user))
    savings_list = list(Saving.objects.filter(user=user))
    
    # Combinar todas las listas
    history = sorted(
        chain(incomes_list, expenses_list, credits_list, savings_list),
        key=attrgetter('created_at'),
        reverse=True
    )[:10]

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_income':
            Income.objects.create(
                user=user,
                type=request.POST.get('type'),
                amount=request.POST.get('amount'),
                periodicity=request.POST.get('periodicity'),
                month=current_month,
                year=current_year,
                description=request.POST.get('description', '')
            )
            messages.success(request, '¡Ingreso registrado correctamente!')
        elif action == 'add_expense':
            sub_category = request.POST.get('sub_category')
            esenciales = ["Arriendo / Hipoteca", "Alimentación", "Transporte", "Servicios (Agua, Luz, Gas)", "Educación", "Salud"]
            category = 'esencial' if sub_category in esenciales else 'no_esencial'
            
            Expense.objects.create(
                user=user,
                category=category,
                sub_category=sub_category,
                amount=request.POST.get('amount'),
                month=current_month,
                year=current_year,
                description=request.POST.get('description', '')
            )
            messages.success(request, f'¡Gasto de {sub_category} registrado correctamente!')
        elif action == 'add_credit':
            Credit.objects.create(
                user=user,
                bank=request.POST.get('bank'),
                product=request.POST.get('product'),
                payment_day=request.POST.get('payment_day'),
                loan_amount=request.POST.get('loan_amount'),
                interest_rate=request.POST.get('interest_rate'),
                monthly_fee=request.POST.get('monthly_fee'),
                total_months=request.POST.get('total_months')
            )
            messages.success(request, '¡Crédito añadido correctamente!')
        elif action == 'add_saving':
            Saving.objects.create(
                user=user,
                bank=request.POST.get('bank'),
                saving_type=request.POST.get('saving_type'),
                monthly_value=request.POST.get('monthly_value')
            )
            messages.success(request, '¡Ahorro/Inversión registrado correctamente!')
        elif action == 'clone_previous_month':
            prev_month = current_month - 1
            prev_year = current_year
            if prev_month == 0:
                prev_month = 12
                prev_year -= 1
            
            # Clonar ingresos fijos
            for inc in Income.objects.filter(user=user, month=prev_month, year=prev_year, type='fijo'):
                Income.objects.create(
                    user=user,
                    type=inc.type,
                    amount=inc.amount,
                    periodicity=inc.periodicity,
                    description=inc.description,
                    month=current_month,
                    year=current_year
                )
            
            # Clonar gastos esenciales
            for exp in Expense.objects.filter(user=user, month=prev_month, year=prev_year, category='esencial'):
                Expense.objects.create(
                    user=user,
                    category=exp.category,
                    sub_category=exp.sub_category,
                    amount=exp.amount,
                    description=f"{exp.description} (Clonado)",
                    month=current_month,
                    year=current_year
                )
            messages.success(request, '¡Ingresos fijos y gastos esenciales clonados con éxito!')
            
        return redirect(f'/dashboard/?month={current_month}&year={current_year}')

    # Determinar estado de la regla 50-30-20
    status_50 = "¡Excelente!" if essential_total <= limit_50 else "¡Cuidado! Te pasaste del 50%"
    status_30 = "¡Bien controlado!" if non_essential_total <= limit_30 else "¡Reducir gastos no esenciales!"
    status_20 = "¡Buen trabajo ahorrando!" if saving_total >= limit_20 else "¡Intenta ahorrar más!"

    month_names = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    months_list = [{'num': i, 'name': month_names[i]} for i in range(1, 13)]

    context = {
        'income_total': income_total,
        'expense_total': expense_total,
        'saving_total': saving_total,
        'essential_total': essential_total,
        'non_essential_total': non_essential_total,
        'limit_50': limit_50,
        'limit_30': limit_30,
        'limit_20': limit_20,
        'status_50': status_50,
        'status_30': status_30,
        'status_20': status_20,
        'ant_total': ant_total,
        'ant_limit': ant_limit,
        'ant_alert': ant_alert,
        'history': history,
        'currency': currency,
        'currency_symbol': currency_symbol,
        'current_month': current_month,
        'current_year': current_year,
        'months_list': months_list,
        'is_new_user': is_new_user,
        'is_new_month': is_new_month,
    }

    return render(request, 'finances/dashboard.html', context)

@login_required
def hormiga_view(request):
    user = request.user
    today = datetime.date.today()

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        if amount and description:
            AntExpense.objects.create(
                user=user,
                amount=amount,
                description=description,
                date=today
            )
            # En Django clásico podríamos usar redirect a la misma página, pero omitido para simplificar

    ant_expenses = AntExpense.objects.filter(user=user, date__month=today.month, date__year=today.year).order_by('-date')
    ant_total = ant_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    incomes = Income.objects.filter(user=user, month=today.month, year=today.year)
    income_total = incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    ant_limit = float(income_total) * 0.05
    ant_alert = bool(float(ant_total) > ant_limit and float(income_total) > 0)

    context = {
        'ant_expenses': ant_expenses,
        'ant_total': ant_total,
        'ant_limit': ant_limit,
        'ant_alert': ant_alert,
        'income_total': income_total,
    }
    return render(request, 'finances/hormiga.html', context)

@login_required
def upgrades_view(request):
    user = request.user
    today = datetime.date.today()
    current_year = today.year

    # UVT 2026 (Proyectada)
    UVT_2026 = 47065
    UMBRAL_UVT = 1400
    limite_declaracion = UVT_2026 * UMBRAL_UVT

    incomes_year = Income.objects.filter(user=user, year=current_year)
    annual_income = incomes_year.aggregate(Sum('amount'))['amount__sum'] or 0

    debe_declarar = bool(float(annual_income) >= limite_declaracion)
    
    # Proyección si seguimos con el promedio mensual (Asumiendo que el mes actual es x)
    if today.month > 1 and annual_income > 0:
        avg_monthly = float(annual_income) / today.month
        projected_annual = avg_monthly * 12
    else:
        projected_annual = float(annual_income) * 12
        
    projected_debe_declarar = bool(projected_annual >= limite_declaracion)

    context = {
        'uvt': UVT_2026,
        'limite_declaracion': limite_declaracion,
        'annual_income': annual_income,
        'debe_declarar': debe_declarar,
        'projected_annual': projected_annual,
        'projected_debe_declarar': projected_debe_declarar,
    }
    return render(request, 'finances/upgrades.html', context)

@login_required
def yearly_summary_view(request):
    user = request.user
    today = datetime.date.today()
    
    req_year = request.GET.get('year')
    current_year = int(req_year) if req_year and req_year.isdigit() else today.year

    month_names = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    monthly_data = []
    
    for i in range(1, 13):
        # Ingresos de este mes
        incomes = Income.objects.filter(user=user, month=i, year=current_year)
        inc_total = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Gastos de este mes
        expenses = Expense.objects.filter(user=user, month=i, year=current_year)
        exp_total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        monthly_data.append({
            'num': i,
            'name': month_names[i],
            'income': float(inc_total),
            'expense': float(exp_total)
        })

    context = {
        'current_year': current_year,
        'monthly_data': monthly_data,
        'years_range': range(current_year - 2, current_year + 3)
    }

    return render(request, 'finances/yearly_summary.html', context)

@login_required
def delete_transaction(request, item_type, item_id):
    user = request.user
    
    # Mapeo simple
    models_map = {
        'income': Income,
        'expense': Expense,
        'saving': Saving,
        'credit': Credit,
        'ant': AntExpense
    }
    
    if item_type in models_map:
        try:
            obj = models_map[item_type].objects.get(id=item_id, user=user)
            obj.delete()
            messages.success(request, 'Transacción eliminada correctamente.')
        except Exception:
            messages.error(request, 'No se pudo eliminar la transacción.')
            
    # Redirigir a la página desde la que se hizo la petición si existe, sino al dashboard
    next_url = request.META.get('HTTP_REFERER', 'dashboard')
    return redirect(next_url)
