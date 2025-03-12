from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Admin
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

            if admin.password_hash == hashed_input_password:
                request.session['admin_id'] = admin.id
                messages.success(request, 'Login successful!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Incorrect username or password.')
        except Admin.DoesNotExist:
            messages.error(request, 'Incorrect username or password.')

    return render(request, 'admin/admin_login.html')

# 管理员仪表盘
def admin_dashboard(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('admin_login')

    return render(request, 'admin/admin_dashboard.html')

# 报告页面
def admin_reports(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('admin_login')
    return render(request, 'admin/admin_reports.html')
