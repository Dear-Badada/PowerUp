from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Rental
# 支付主页
@login_required
def payment_home(request):
    return render(request, 'payment/payment.html')

# 支付详情
@login_required
def payment_details(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    if rental.total_cost is None:
        return JsonResponse({"message": "Rental cost not calculated yet"}, status=400)

    payment_data = {
        "payment_amount": rental.total_cost,
        "rental_id": rental.id,
        "start_time": rental.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": rental.end_time.strftime("%Y-%m-%d %H:%M:%S") if rental.end_time else "Ongoing",
        "status": rental.payment_status
    }
    return JsonResponse(payment_data)

# 支付历史
@login_required
def payment_history(request):
    rentals = Rental.objects.filter(user=request.user, payment_status="paid").order_by("-end_time")

    payment_records = []
    for rental in rentals:
        payment_records.append({
            "payment_id": rental.id,
            "rental": {"rental_id": rental.powerbank.id},
            "payment_amount": float(rental.total_cost),
            "payment_time": rental.end_time.strftime("%Y-%m-%d %H:%M:%S") if rental.end_time else "Ongoing",
            "usage_hours": round((rental.end_time - rental.start_time).total_seconds() / 3600, 2) if rental.end_time else "Ongoing",
        })

    context = {
        "customer": {"customer_name": request.user.username},
        "payments": payment_records
    }

    return render(request, 'payment/payment_history.html', context)


# 支付成功
@login_required
def payment_success(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    if rental.payment_status != "paid":
        return redirect('payment_home')  # 如果未支付，跳转回支付首页

    mock_data = {
        "payment": {
            "payment_id": rental.id,
            "payment_amount": rental.total_cost,
        },
        "rental": {
            "customer_name": request.user.username,
            "start_time": rental.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": rental.end_time.strftime("%Y-%m-%d %H:%M:%S") if rental.end_time else "Ongoing",
        },
    }
    return render(request, 'payment/payment_success.html', mock_data)