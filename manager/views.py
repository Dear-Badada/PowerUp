from decimal import Decimal
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from order.models import Order, RefundRequest
from powerbank.models import Station, PowerBank, Pricing
from .forms import StationForm, PricingForm
from users.models import User

def manager_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, "manager_login.html")

        if user.check_password(password):
            login(request, user)  # 直接使用 login() 登录
            messages.success(request, "Admin login successful!")
            return redirect("manager_dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "manager/manager_login.html")

@login_required
def manager_dashboard(request):
    """管理员仪表盘视图"""
    total_users = User.objects.count()
    total_rentals = Order.objects.count()
    available_power_banks = PowerBank.objects.filter(status="available").count()
    powerbanks = PowerBank.objects.all()

    return render(request, "manager/manager_dashboard.html", {
        "total_users": total_users,
        "total_rentals": total_rentals,
        "available_power_banks": available_power_banks,
        "powerbanks": powerbanks
    })

# ======【充电宝管理】======
@login_required
def powerbank_list(request, station_id):
    """查看指定站点的充电宝列表"""
    station = get_object_or_404(Station, id=station_id)
    powerbanks = PowerBank.objects.filter(station=station)

    return render(request, "manager/powerbank_list.html", {
        "powerbanks": powerbanks,
        "station": station
    })

@login_required
def update_powerbank_status(request, powerbank_id):
    """管理员更新充电宝状态"""
    power_bank = get_object_or_404(PowerBank, id=powerbank_id)

    if power_bank.status == "available":
        power_bank.status = "rented"
    elif power_bank.status == "rented":
        power_bank.status = "available"
    elif power_bank.status == "damaged":
        messages.warning(request, "Damaged power banks must be repaired manually.")
        return redirect("powerbank_list", station_id=power_bank.station.id)

    power_bank.save()
    messages.success(request, f"Power bank status updated to {power_bank.get_status_display()}.")
    return redirect("powerbank_list", station_id=power_bank.station.id)


@login_required
def delete_powerbank(request, powerbank_id):
    """删除充电宝"""
    power_bank = get_object_or_404(PowerBank, id=powerbank_id)
    station_id = power_bank.station.id
    power_bank.delete()
    messages.success(request, "Power bank deleted successfully.")
    return redirect("powerbank_list", station_id=station_id)

@login_required
def repair_powerbank(request, powerbank_id):
    """修复充电宝"""
    power_bank = get_object_or_404(PowerBank, id=powerbank_id)
    if power_bank.status == "damaged":
        power_bank.status = "available"
        power_bank.save()
        return JsonResponse({"success": True, "message": "Power bank repaired successfully."})
    return JsonResponse({"success": False, "message": "Invalid status for repair."})


# ======【站点管理】======
@login_required
def station_list_manager(request):
    """ 显示所有站点（管理员视角） """
    stations = Station.objects.all()
    return render(request, "manager/station_list.html", {"stations": stations})


@login_required
def create_station(request):
    """ 创建新站点 """
    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Station created successfully.")
            return redirect("station_list_admin")
        else:
            messages.error(request, "Invalid data. Please check the form.")
    else:
        form = StationForm()

    return render(request, "manager/create_station.html", {"form": form})


@login_required
def delete_station(request, station_id):
    """ 删除站点 """
    station = get_object_or_404(Station, id=station_id)
    station.delete()
    messages.success(request, "Station deleted successfully.")
    return redirect("station_list_admin")


# ======【退款管理】======
@login_required
def refund_requests_list(request):
    """ 显示所有退款申请 """
    refund_requests = RefundRequest.objects.all()
    return render(request, "manager/refund_requests_list.html", {"refund_requests": refund_requests})


@login_required
def handle_refund_request(request, refund_request_id):
    """管理员处理退款申请（同意或拒绝）"""
    refund_request = get_object_or_404(RefundRequest, id=refund_request_id)
    order = refund_request.order
    user = refund_request.user

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            if refund_request.status == "pending":  # 避免重复退款
                user.balance += Decimal(order.deposit)
                user.save()

                order.order_status = "completed"
                order.save()

                refund_request.status = "approved"
                refund_request.processed_at = timezone.now()
                refund_request.save()

                messages.success(request, "Refund approved and deposit returned to user.")
        elif action == "reject":
            refund_request.status = "rejected"
            refund_request.processed_at = timezone.now()
            refund_request.save()

            messages.success(request, "Refund request rejected.")

        return redirect("refund_requests_list")

    return render(request, "manager/refund_request_detail.html", {"refund_request": refund_request})

@login_required
def update_pricing(request):
    """管理员修改租赁价格和押金"""
    pricing = Pricing.objects.first()  # 获取现有的定价信息
    if not pricing:
        pricing = Pricing.objects.create(hourly_rate=1.00, deposit_amount=15.00)  # 默认值

    if request.method == "POST":
        form = PricingForm(request.POST, instance=pricing)
        if form.is_valid():
            form.save()
            messages.success(request, "Pricing updated successfully.")
            return redirect("update_pricing")
        else:
            messages.error(request, "Invalid input. Please check the form.")
    else:
        form = PricingForm(instance=pricing)

    return render(request, "manager/update_pricing.html", {"form": form})