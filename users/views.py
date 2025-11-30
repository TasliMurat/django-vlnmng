from django.shortcuts import render
from django.contrib import messages
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.views.decorators.cache import never_cache

# Kayıt (opsiyonel)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import re
from users.tasks import my_task

def register_view(request):
    if request.method == 'POST':
        # Form verilerini al
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Boş alan kontrolü
        if not all([first_name, last_name, username, email, password]):
            messages.error(request, 'Tüm alanları doldurmanız gerekmektedir.')
            return render(request, 'users/register.html')
        
        # Email format kontrolü
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Geçersiz email formatı.')
            return render(request, 'users/register.html')
        
        # Username format kontrolü (sadece harf, rakam ve _ karakteri)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            messages.error(request, 'Kullanıcı adı sadece harf, rakam ve alt çizgi içerebilir.')
            return render(request, 'users/register.html')
        
        # Username uzunluk kontrolü
        if len(username) < 3:
            messages.error(request, 'Kullanıcı adı en az 3 karakter olmalıdır.')
            return render(request, 'users/register.html')
        
        # Şifre güçlülük kontrolü
        if len(password) < 8:
            messages.error(request, 'Şifre en az 8 karakter olmalıdır.')
            return render(request, 'users/register.html')
        
        # Email uniqueness kontrolü
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu email adresi ile kayıtlı bir kullanıcı zaten var.')
            return render(request, 'users/register.html')
        
        # Username uniqueness kontrolü
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı ile kayıtlı bir kullanıcı zaten var.')
            return render(request, 'users/register.html')
        
        # İsim ve soyisim uzunluk kontrolü
        if len(first_name) < 2 or len(last_name) < 2:
            messages.error(request, 'İsim ve soyisim en az 2 karakter olmalıdır.')
            return render(request, 'users/register.html')
        
        try:
            # Kullanıcı oluşturma
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password  # create_user metodu şifreyi otomatik hash'ler
            )
            
            messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
            return redirect('login')  # login sayfasına yönlendir
            
        except IntegrityError as e:
            # Veritabanı seviyesinde unique constraint hatası
            if 'username' in str(e):
                messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor.')
            elif 'email' in str(e):
                messages.error(request, 'Bu email adresi zaten kullanılıyor.')
            else:
                messages.error(request, 'Kayıt işlemi sırasında bir hata oluştu.')
            return render(request, 'users/register.html')
        
        except Exception as e:
            # Beklenmeyen hatalar
            messages.error(request, 'Kayıt işlemi sırasında beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.')
            return render(request, 'users/register.html')
    
    # GET request - kayıt sayfasını göster
    return render(request, 'users/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
            
        
        else:
            messages.error(request, "Kullanıcı adı veya parola hatalı!")
            return redirect("login")
    
    else:
        return render(request, "users/login.html")
    


def logout_view(request):
    logout(request)
    return redirect("login")


@never_cache
@login_required(login_url="/users/login/")
def dashboard(request):
    """Kullanıcının yetkili olduğu entegrasyonları listeler"""
    return render(request, "users/dashboard.html")
