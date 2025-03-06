from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import PowerBank, Rental
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def rent_powerbank(request, powerbank_id):
    powerbank = get_object_or_404(PowerBank, id=powerbank_id, status="available")
    if request.method == "POST":
        rental = Rental.objects.create(user=request.user, powerbank=powerbank)
        powerbank.status = "in_use"
        powerbank.save()
        return JsonResponse({"message": "PowerBank rented successfully", "rental_id": rental.id})

@csrf_exempt
def return_powerbank(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    rental.powerbank.status = "available"
    rental.powerbank.save()
    rental.end_time = timezone.now()
    rental.save()
    return JsonResponse({"message": "PowerBank returned successfully"})
