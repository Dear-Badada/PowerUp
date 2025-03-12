from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from powerbank.models import Pricing, PowerBank
from payment.models import Order, Transaction
from .models import User
from .forms import RegistrationForm, LoginForm
from payment.views import create_order, return_order

# ======【用户注册】======
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "users/register.html", {"form": form})

            user = form.save(commit=False)
            user.set_password(password)  # ✅ Hash 密码
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


# ======【用户登录】======
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
                    request.session.set_expiry(3600)  # Session 1 小时后自动过期
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


# ======【查看钱包余额】======
@login_required
def view_wallet(request):
    user = get_object_or_404(User, id=request.session['user_id'])
    return render(request, "users/wallet.html", {"username": user.username, "balance": user.balance})


# ======【充值钱包】======
@login_required
def recharge_wallet(request):
    pricing = Pricing.objects.first()  # 获取定价表
    deposit_amount = pricing.deposit_amount if pricing else Decimal('0.00')

    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount"))

            if amount < deposit_amount:
                messages.error(request, f"The minimum recharge amount is ${deposit_amount:.2f}.")
                return redirect("recharge_wallet")

            user = get_object_or_404(User, id=request.session['user_id'])
            user.balance += amount
            user.save()

            # 记录充值交易
            Transaction.objects.create(
                user=user,
                type='deposit',
                amount=amount
            )

            messages.success(request, f"Successfully recharged ${amount:.2f}.")
            return redirect("view_wallet")

        except (ValueError, TypeError):
            messages.error(request, "Invalid amount. Please enter a valid number.")
    else:
        amount = Decimal('0.00')

    return render(request, "users/recharge.html", {"amount": amount, "deposit_amount": deposit_amount})


# ======【主页】======
def home(request):
    return render(request, 'includes/home.html')


# ======【租借充电宝】======
@login_required
def rent_powerbank(request, powerbank_id):
    """ 用户租借充电宝 """
    return create_order(request, powerbank_id)


# ======【归还充电宝】======
@login_required
def return_powerbank(request):
    """ 用户归还充电宝 """
    user = get_object_or_404(User, id=request.session['user_id'])
    order = Order.objects.filter(user=user, order_status="ongoing").first()

    if order:
        return return_order(request, order.id)

    messages.error(request, "No active rental found.")
    return redirect("home")
