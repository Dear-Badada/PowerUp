from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from adminn.models import Admin
from payment.models import Order, Transaction
from powerbank.models import Rental
from users.models import User
import hashlib


# 管理员登录
@csrf_protect
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(username=username)
            hashed_input_password = hashlib.sha256((password + admin.salt).encode()).hexdigest()

            if hashed_input_password == admin.password_hash:
                request.session['admin_id'] = admin.id
                messages.success(request, 'Logged in successfully!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid credentials')

    return render(request, 'admin/admin_login.html')


# 管理员仪表盘
def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')

    return render(request, 'admin/admin_dashboard.html')


# 管理员报告页面
def admin_reports(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')

    transactions = Transaction.objects.all().order_by('-created_at')
    orders = Order.objects.all().order_by('-start_time')

    context = {
        "transactions": transactions,
        "orders": orders
    }

    return render(request, 'admin/admin_reports.html', context)


# 支付首页
def payment_home(request):
    return render(request, 'payment/payment_home.html')


# 支付详情页面
def payment_details(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)

    context = {
        "rental": rental,
        "payment_amount": rental.total_cost,
        "remaining_balance": rental.user.balance,
        "start_station_name": rental.power_bank.station.name,
        "end_station_name": rental.power_bank.station.name,
    }

    return render(request, 'payment/payment_details.html', context)


# 用户支付历史页面
def payment_history(request, customer_id):
    user = get_object_or_404(User, id=customer_id)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'transactions': transactions,
    }

    return render(request, 'payment/payment_history.html', context)


# 支付成功页面
def payment_success(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)

    context = {
        "rental": rental,
        "message": "Payment Successful!",
        "total_cost": rental.total_cost,
    }

    return render(request, 'payment/payment_success.html', context)
