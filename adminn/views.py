from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from payment.models import RefundRequest
from powerbank.models import Station, PowerBank, Pricing
from .forms import StationForm, PricingForm


# ===== 站点管理 =====
def station_list_admin(request):
    """ 显示所有站点（管理员视角） """
    stations = Station.objects.all()
    return render(request, "admin/station_list.html", {"stations": stations})


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


def delete_station(request, station_id):
    """ 删除站点 """
    station = get_object_or_404(Station, id=station_id)
    station.delete()
    messages.success(request, "Station deleted successfully.")
    return redirect("station_list_admin")


# ===== 充电宝管理 =====
def powerbank_list(request, station_id):
    """ 查看站点内的所有充电宝 """
    station = get_object_or_404(Station, id=station_id)
    power_banks = PowerBank.objects.filter(station=station)

    if request.method == "POST":
        # 处理添加充电宝的请求，默认充电宝满电和正常状态
        PowerBank.objects.create(
            station=station,
            battery_level=100,  # 默认满电
            status="available"  # 默认状态正常
        )
        messages.success(request, "Power bank added successfully.")
        return redirect("powerbank_list", station_id=station.id)

    return render(request, "admin/powerbank_list.html", {"station": station, "power_banks": power_banks})


def delete_powerbank(request, powerbank_id):
    """ 删除充电宝 """
    power_bank = get_object_or_404(PowerBank, id=powerbank_id)
    station_id = power_bank.station.id  # 先获取站点 ID，删除后跳转回去
    power_bank.delete()
    messages.success(request, "Power bank deleted successfully.")
    return redirect("powerbank_list", station_id=station_id)


def update_powerbank_status(request, powerbank_id):
    """ 更新充电宝状态 """
    power_bank = get_object_or_404(PowerBank, id=powerbank_id)

    power_bank.status = 'available'
    power_bank.save()
    messages.success(request, f"Power bank status updated to available.")

    return redirect("powerbank_list", station_id=power_bank.station.id)


def update_pricing(request):
    """ 管理员修改租赁单价和押金 """
    pricing = Pricing.objects.first()  # 获取唯一的定价记录
    if not pricing:
        pricing = Pricing.objects.create(hourly_rate=1.00, deposit_amount=15.00)  # 如果没有，则创建默认值

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


def refund_requests_list(request):
    """ 显示所有退款申请 """
    refund_requests = RefundRequest.objects.all()  # 获取所有退款申请
    return render(request, "admin/refund_requests_list.html", {"refund_requests": refund_requests})


def handle_refund_request(request, refund_request_id):
    """ 管理员处理退款申请（同意或拒绝） """
    refund_request = get_object_or_404(RefundRequest, id=refund_request_id)
    order = refund_request.order  # 获取对应的订单
    user = refund_request.user  # 获取退款申请的用户

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            # 同意退款
            # 1. 将订单的押金退还到用户余额
            user.balance += Decimal(order.deposit)  # 退还押金
            user.save()

            # 2. 设置订单状态为 'completed'
            order.order_status = "completed"
            order.save()

            # 3. 更新退款状态为 'approved'
            refund_request.status = "approved"
            refund_request.processed_at = timezone.now()  # 标记处理时间
            refund_request.save()

            messages.success(request, "Refund approved and deposit returned to user.")

        elif action == "reject":
            # 拒绝退款
            refund_request.status = "rejected"
            refund_request.processed_at = timezone.now()  # 标记处理时间
            refund_request.save()

            messages.success(request, "Refund request rejected.")

        return redirect("refund_requests_list")  # 返回退款申请列表页面

    return render(request, "admin/refund_request_detail.html", {"refund_request": refund_request})
