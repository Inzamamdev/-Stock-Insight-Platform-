from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from prediction.models import Prediction
from prediction.serializers import PredictionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
           # Generate JWT token and set it in an HTTP-only cookie
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = redirect('dashboard')
            response.set_cookie(
                'jwt_token',
                access_token,
                httponly=False,
                secure=config('SESSION_COOKIE_SECURE', cast=bool, default=False),
                samesite='Lax',
                max_age=15 * 60,  # Match JWT_ACCESS_LIFETIME (15 minutes)
            )
            messages.success(request, 'Login successful!')
            return response
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('jwt_token')
    messages.success(request, 'Logged out successfully!')
    return response
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    serializer = PredictionSerializer(predictions, many=True, context={'request': request})
    return render(request, 'dashboard.html', {
        'predictions': serializer.data,
    })