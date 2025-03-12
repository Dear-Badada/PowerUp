from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from powerbank.models import Pricing
from .models import User

from users.forms import RegistrationForm, LoginForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})

# 用户登录视图
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    messages.success(request, "Login successful.")
                    return redirect("home")
                else:
                    messages.error(request, "Invalid username or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")

    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def view_wallet(request):
    user = User.objects.get(id=request.session['user_id'])  # Ensure the latest data is fetched
    return render(request, "users/wallet.html", {"username": user.username,
        "balance": user.balance})


def recharge_wallet(request):
    # 获取定价表中的押金金额
    pricing = Pricing.objects.first()  # 假设只有一个定价记录
    deposit_amount = pricing.deposit_amount

    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount"))  # 获取表单提交的充值金额

            # 验证充值金额是否大于或等于押金金额
            if amount < deposit_amount:
                messages.error(request, f"The minimum recharge amount is ${deposit_amount:.2f}, which is the deposit for a power bank.")
                return redirect("recharge_wallet")  # 返回充值页面

            # 获取当前用户并更新余额
            user = User.objects.get(id=request.session['user_id'])  # 根据 session 获取当前用户
            user.balance += amount  # 增加余额
            user.save()

            # 提示成功并跳转
            messages.success(request, f"Successfully recharged ${amount:.2f}.")
            return redirect("view_wallet")  # 成功后跳转到钱包页面

        except (ValueError, TypeError):
            messages.error(request, "Invalid amount. Please enter a valid number.")
    else:
        # 默认金额设置为 0
        amount = Decimal('0.00')

    return render(request, "users/recharge.html", {"amount": amount, "deposit_amount": deposit_amount})

def home(request):
    return render(request, 'includes/home.html')

# 用户主页（租借充电宝）
@login_required
def rent_powerbank(request, powerbank_id):
    return render(request, 'users/rent.html', {'powerbank_id': powerbank_id})

# 用户归还充电宝
@login_required
def return_powerbank(request):
    return render(request, 'users/return.html')
