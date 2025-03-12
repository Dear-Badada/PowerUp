from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from payment.models import RefundRequest, Transaction, Order
from powerbank.models import Station, PowerBank, Pricing
from .models import Admin
from .forms import StationForm, PricingForm


# ======【充电宝管理】======
@login_required
def powerbank_list(request, station_id):
    """管理员查看某个站点的所有充电宝"""
    station = get_object_or_404(Station, id=station_id)
    power_banks = PowerBank.objects.filter(station=station)

    return render(request, "admin/powerbank_list.html", {"station": station, "power_banks": power_banks})


@login_required
def update_powerbank_status(request, powerbank_id):
    """管理员更新充电宝状态"""
    power_bank = get_object_or_404(PowerBank, id=powerbank_id)

    # 轮换充电宝状态
    if power_bank.status == "available":
        power_bank.status = "in_use"
    elif power_bank.status == "in_use":
        power_bank.status = "charging"
    elif power_bank.status == "charging":
        power_bank.status = "available"

    power_bank.save()
    messages.success(request, f"Power bank status updated to {power_bank.status}.")

    return redirect("powerbank_list", station_id=power_bank.station.id)


@login_required
def delete_powerbank(request, powerbank_id):
    """删除充电宝"""
    power_bank = get_object_or_404(PowerBank, id=powerbank_id)
    station_id = power_bank.station.id
    power_bank.delete()
    messages.success(request, "Power bank deleted successfully.")
    return redirect("powerbank_list", station_id=station_id)


# ======【站点管理】======
@login_required
def station_list_admin(request):
    """ 显示所有站点（管理员视角） """
    stations = Station.objects.all()
    return render(request, "admin/station_list.html", {"stations": stations})


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

    return render(request, "admin/create_station.html", {"form": form})


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
    return render(request, "admin/refund_requests_list.html", {"refund_requests": refund_requests})


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

    return render(request, "admin/refund_request_detail.html", {"refund_request": refund_request})

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

    return render(request, "admin/update_pricing.html", {"form": form})