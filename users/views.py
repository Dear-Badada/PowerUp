import json
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme

from powerbank.models import Pricing, Station
from payment.models import Order, Transaction
from .models import User
from .forms import RegistrationForm, LoginForm
from payment.views import return_order
from django.urls import reverse


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

            # 创建用户并设置密码
            user = form.save(commit=False)
            user.set_password(password)
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
                # 手动查询用户
                user = User.objects.get(username=username)

                if user.check_password(password):
                    login(request, user)

                    request.session["user_id"] = user.id
                    request.session.modified = True

                    messages.success(request, "Login successful.")
                    return redirect("station_list")  # 登录后跳转到选择站点的页面
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
    pricing = Pricing.objects.first()
    deposit_amount = pricing.deposit_amount if pricing else Decimal('5.00')
    user = get_object_or_404(User, id=request.session.get("user_id"))

    if request.method == "POST":
        try:
            # 确保请求的内容是 JSON
            if request.content_type != "application/json":
                return JsonResponse({"success": False, "error": "Invalid content type."}, status=400)

            data = json.loads(request.body)
            amount_str = data.get("amount", "").strip()

            if not amount_str:
                return JsonResponse({"success": False, "error": "Amount cannot be empty."}, status=400)

            amount = Decimal(amount_str)

            if amount < deposit_amount:
                return JsonResponse({"success": False, "error": f"Minimum recharge amount is £{deposit_amount:.2f}."}, status=400)

            if amount <= 0:
                return JsonResponse({"success": False, "error": "Please enter a valid amount greater than £0."}, status=400)

            # 更新用户余额
            user.balance += amount
            user.is_active = True
            user.save()

            # 记录充值交易
            Transaction.objects.create(user=user, type='deposit', amount=amount)

            return JsonResponse({"success": True, "new_balance": float(user.balance)})

        except (json.JSONDecodeError, ValueError, InvalidOperation):
            return JsonResponse({"success": False, "error": "Invalid request format."}, status=400)

    return render(request, "users/recharge.html", {
        "balance": user.balance,
        "deposit_amount": deposit_amount,
    })


# ======【主页】======
def home(request):
    return render(request, 'includes/home.html')


# ======【租借充电宝】======
@login_required
def rent_powerbank(request):
    user = get_object_or_404(User, id=request.session.get("user_id"))
    stations = Station.objects.all()

    context = {
        "stations": stations,
        "balance": user.balance
    }
    return render(request, "users/rent.html", context)

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
