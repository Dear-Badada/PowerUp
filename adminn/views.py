from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# 管理员登录
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  # 只有管理员可以登录
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'admin/admin_login.html', {'form': form})

def admin_reports(request):
    # 渲染 admin_reports.html 模板
    return render(request, 'admin/admin_reports.html')

# 管理员控制面板
@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')
