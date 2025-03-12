from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone
from django.http import JsonResponse

from users.views import login_required
from .models import PowerBank, Rental, Station
from payment.models import Pricing

@login_required
def rent_powerbank(request, powerbank_id):
    if Rental.objects.filter(user=request.user, order_status="ongoing").exists():
        return JsonResponse({"message": "You already have a rented PowerBank. Please return it first."}, status=400)

    powerbank = get_object_or_404(PowerBank, id=powerbank_id, status="available")
    pricing = Pricing.objects.first()

    if request.method == "POST":
        rental = Rental.objects.create(
            user=request.user,
            power_bank=powerbank,
            deposit=pricing.deposit_amount,
            hourly_rate=pricing.hourly_rate,
            start_time=timezone.now(),
            order_status='ongoing'
        )
        powerbank.status = "rented"
        powerbank.save()

        return JsonResponse({"message": "Rental successful", "rental_id": rental.id})

    stations = Station.objects.all()
    return render(request, 'users/rent.html', {'stations': stations})

@login_required
def return_powerbank(request, rental_id):
    rental = Rental.objects.filter(user=request.user, order_status="ongoing").first()

    if not rental:
        return JsonResponse({"message": "No active rental found."}, status=400)

    rental.end_time = timezone.now()
    rental_duration = (rental.end_time - rental.start_time).total_seconds() / 3600

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

    rental.total_cost = round(rental_cost, 2)
    rental.order_status = 'completed'
    rental.payment_status = 'pending'
    rental.save()

    powerbank = rental.power_bank
    powerbank.status = "available"
    powerbank.save()

    return JsonResponse({
        "message": "PowerBank returned successfully",
        "rental_id": rental.id,
        "total_time": f"{rental_duration:.2f} hours",
        "cost": f"£{rental.total_cost}"
    })
