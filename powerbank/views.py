from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from payment.models import Order
from .models import PowerBank, Station, Pricing


@login_required
@csrf_exempt
def rent_powerbank(request, powerbank_id):
    """
    用户租借充电宝
    - 只能租借状态为 "available" 的充电宝
    - 用户只能租一个充电宝，不能重复租借
    """
    if request.method == "POST":
        user = request.user
        existing_order = Order.objects.filter(user=user, end_time__isnull=True).first()

        if existing_order:
            return JsonResponse({"error": "You already have a rented PowerBank. Please return it first."}, status=400)

        powerbank = get_object_or_404(PowerBank, id=powerbank_id, status="available")

        # 获取租赁单价和押金
        pricing = Pricing.objects.first()
        deposit = pricing.deposit_amount if pricing else Decimal("5.00")
        hourly_rate = pricing.hourly_rate if pricing else Decimal("1.00")

        # 创建订单
        order = Order.objects.create(
            user=user,
            power_bank=powerbank,
            deposit=deposit,
            hourly_rate=hourly_rate,
            order_status="ongoing",
            payment_status="pending"
        )

        # 更新充电宝状态
        powerbank.status = "rented"
        powerbank.save()

        return JsonResponse({"message": "PowerBank rented successfully", "order_id": order.id})


@login_required
@csrf_exempt
def return_powerbank(request, order_id):
    """
    用户归还充电宝
    - 归还时，充电宝状态会变回 "available"
    - 记录归还时间，并计算费用
    """
    order = get_object_or_404(Order, id=order_id, user=request.user, end_time__isnull=True)

    # 计算租借时长（小时）
    rental_duration = (timezone.now() - order.start_time).total_seconds() / 3600
    total_cost = round(order.hourly_rate * rental_duration, 2)

    # 归还充电宝
    order.power_bank.status = "available"
    order.power_bank.save()

    # 更新订单信息
    order.end_time = timezone.now()
    order.total_cost = total_cost
    order.order_status = "completed"
    order.save()

    return JsonResponse({"message": "PowerBank returned successfully", "total_cost": total_cost})


def station_list(request):
    """
    显示所有站点
    """
    stations = Station.objects.all()
    return render(request, "powerbank/stations.html", {"stations": stations})


def station_detail(request, station_id):
    """
    显示站点的所有可用充电宝
    """
    station = get_object_or_404(Station, id=station_id)
    available_power_banks = PowerBank.objects.filter(station=station, status="available")

    return render(request, "powerbank/station_detail.html", {"station": station, "power_banks": available_power_banks})
