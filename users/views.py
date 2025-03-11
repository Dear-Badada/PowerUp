from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User

from users.forms import RegistrationForm, LoginForm, RechargeForm


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
    if request.method == "POST":
        form = RechargeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            user = User.objects.get(id=request.session['user_id'])  # Fetch the user again to get the latest balance
            user.balance += amount  # Update the balance
            user.save()
            messages.success(request, f"Successfully recharged ${amount:.2f}.")
            return redirect("view_wallet")  # Redirect to wallet page after successful recharge
        else:
            messages.error(request, "Invalid amount. Please enter a valid number.")
    else:
        form = RechargeForm()

    return render(request, "users/recharge.html", {"form": form})

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
