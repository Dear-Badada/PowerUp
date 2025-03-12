from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from .models import Rental, powerbank

# 用户注册（成功后自动登录）
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 注册成功后自动登录
            return redirect('rent_powerbank')  # 跳转到租借页面
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# 用户登录（失败时显示错误信息）
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('rent_powerbank')  # 登录后跳转到租借页面
        else:
            messages.error(request, "Invalid username or password.")  # 显示错误信息
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# 用户登出
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # 退出后跳转到登录页


# 主页（如果已登录，跳转到租借充电宝页面）
def home(request):
    if request.user.is_authenticated:
        return redirect('rent_powerbank')
    return render(request, 'users/home.html')


# 充电宝租借（防止重复租借）
@login_required
def rent_powerbank(request, powerbank_id):
    if Rental.objects.filter(user=request.user, powerbank__status="in_use").exists():
        return JsonResponse({"message": "You already have a rented PowerBank. Return it first."}, status=400)

    powerbank = get_object_or_404(PowerBank, id=powerbank_id, status="available")

    # 创建租借订单
    rental = Rental.objects.create(user=request.user, powerbank=powerbank, start_time=timezone.now())
    powerbank.status = "in_use"
    powerbank.save()

    return render(request, 'users/rent.html', {'powerbank_id': powerbank_id})


# 归还充电宝（确保用户归还的是自己租借的）
@login_required
def return_powerbank(request):
    rental = Rental.objects.filter(user=request.user, powerbank__status="in_use").first()

    if not rental:
        return JsonResponse({"message": "No active rental found."}, status=400)

    rental.end_time = timezone.now()
    rental.powerbank.status = "available"
    rental.powerbank.save()

    # 计算租借时长
    rental_duration = (rental.end_time - rental.start_time).total_seconds() / 3600  # 转换为小时

    # 计算费用（定价规则）
    if rental_duration <= 1:
        rental_cost = 1.5
    elif rental_duration <= 2:
        rental_cost = 3
    elif rental_duration <= 3:
        rental_cost = 4
    else:
        rental_cost = 4 + (rental_duration - 3) * 1  # 超过3小时，每小时£1

    rental.total_cost = round(rental_cost, 2)  # 保留两位小数
    rental.save()

    return render(request, 'users/return.html', {
        "message": "PowerBank returned successfully",
        "rental_time": f"{rental_duration:.2f} hours",
        "cost": f"£{rental.total_cost}"
    })
