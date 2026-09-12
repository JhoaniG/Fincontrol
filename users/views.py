from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'users/landing.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        currency = request.POST.get('currency', 'COP')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')
        
        if CustomUser.objects.filter(username=email).exists():
            messages.error(request, 'Ya existe una cuenta con este correo.')
            return redirect('register')
        
        # Crear usuario. Usamos el email como username
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name,
            preferred_currency=currency
        )
        
        # Automáticamente lo dejamos verificado para evitar problemas (el OTP se asume para Hotmart por ahora)
        user.is_verified = True
        user.save()

        messages.success(request, '¡Cuenta creada con éxito! Ahora puedes iniciar sesión.')
        return redirect('login')
        
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_verified:
                # Simular envío de OTP y redirigir a verificación
                return redirect('otp_verify', user_id=user.id)
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def otp_verify_view(request, user_id):
    # En un sistema real, aquí validas que el código ingresado coincide con OTPVerification
    if request.method == 'POST':
        code = request.POST.get('code')
        # Simulación de éxito (cualquier código pasa)
        user = CustomUser.objects.get(id=user_id)
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'users/otp_verify.html', {'user_id': user_id})

@csrf_exempt
def hotmart_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Procesar el JSON de Hotmart. 
            # Ejemplo: crear el usuario, generar contraseña aleatoria, enviar email con OTP.
            email = data.get('email')
            if email:
                user, created = CustomUser.objects.get_or_create(username=email, email=email)
                if created:
                    user.set_password('Teojhoanig12*') # En la vida real, se genera o se deja pendiente
                    user.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        currency = request.POST.get('currency')
        activity_type = request.POST.get('activity_type')
        
        if full_name: user.first_name = full_name
        # Si hubiera campo phone en el modelo, lo guardaríamos aquí. Por ahora no lo tenemos en DB, pero sí activity_type
        if currency: user.preferred_currency = currency
        if activity_type: user.activity_type = activity_type
        
        user.save()
        messages.success(request, '¡Perfil actualizado correctamente!')
        return redirect('profile')
        
    return render(request, 'users/profile.html', {'user': user})

@login_required
def pricing_view(request):
    return render(request, 'users/pricing.html')

@login_required
def checkout_view(request, plan):
    # plan puede ser 'monthly' o 'annual'
    amount_in_cents = 4000 if plan == 'monthly' else 40000
    if plan not in ['monthly', 'annual']:
        return redirect('pricing')
        
    context = {
        'plan': plan,
        'amount_in_cents': amount_in_cents, # Wompi usa centavos
        'reference': f'sub_{request.user.id}_{plan}'
    }
    return render(request, 'users/checkout.html', context)

@login_required
def cancel_subscription_view(request):
    user = request.user
    if hasattr(user, 'subscription'):
        user.subscription.status = 'canceled'
        user.subscription.save()
        messages.success(request, 'Suscripción cancelada correctamente. Sentimos verte partir.')
    return redirect('profile')
