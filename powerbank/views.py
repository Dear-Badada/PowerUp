from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import PowerBank, Rental

@csrf_exempt
@login_required
def rent_powerbank(request, powerbank_id):
    powerbank = get_object_or_404(PowerBank, id=powerbank_id, status="available")
    # 防止用户重复租借
    if Rental.objects.filter(user=request.user, powerbank__status="in_use").exists():
        return JsonResponse({"message": "You already have a rented PowerBank. Return it before renting a new one."},
                            status=400)

    if request.method == "POST":
        rental = Rental.objects.create(user=request.user, powerbank=powerbank, start_time=timezone.now())
        powerbank.status = "in_use"
        powerbank.save()
        return JsonResponse({"message": "PowerBank rented successfully", "rental_id": rental.id})

@login_required
def return_powerbank(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    # 计算租借时长
    rental.end_time = timezone.now()
    rental_duration = (rental.end_time - rental.start_time).total_seconds() / 3600  # 转换为小时

    # 计算费用
    # 定价标准：
    # |   计费时长   |  价格 (£) |
    # |-------------|----------|
    # |  1 小时内    |  £1.5    |
    # |  2 小时内    |  £3      |
    # |  3 小时内    |  £4      |
    # |  超过 3 小时 | 每小时 £1 |

    if rental_duration <= 1:
        rental_cost = 1.5
    elif rental_duration <= 2:
        rental_cost = 3
    elif rental_duration <= 3:
        rental_cost = 4
    else:
        rental_cost = 4 + (rental_duration - 3) * 1

    rental.total_cost = round(rental_cost, 2)  # 保留两位小数
    rental.powerbank.status = "available"
    rental.powerbank.save()
    rental.save()

    return JsonResponse({
        "message": "PowerBank returned successfully",
        "rental_id": rental.id,
        "total_time": f"{rental_duration:.2f} hours",
        "cost": f"£{rental.total_cost}"
    })
