from django.shortcuts import render

# 支付主页
def payment_home(request):
    return render(request, 'payment/payment.html')

# 支付详情
def payment_details(request, rental_id):
    mock_data = {
        "payment_amount": 12.50,
        "remaining_balance": 50.00,
        "rental": {
            "customer_id": {"customer_name": "John Doe"},
            "start_time": "2025-03-05 12:00:00",
            "end_time": "2025-03-05 14:00:00",
            "start_station_name": "Station A",
            "end_station_name": "Station B",
            "vehicle_id": {"vehicle_id": 12345},
        },
        "rental_id": rental_id,
    }
    return render(request, 'payment/payment_details.html', mock_data)

# 支付历史
def payment_history(request, customer_id):
    mock_data = {
        "customer": {"customer_name": "John Doe"},
        "payments": [
            {
                "payment_id": 1,
                "rental": {"rental_id": 101},
                "payment_amount": 10.00,
                "payment_time": "2025-03-04 10:30:00",
                "usage_hours": 2,
            },
            {
                "payment_id": 2,
                "rental": {"rental_id": 102},
                "payment_amount": 15.00,
                "payment_time": "2025-03-03 14:20:00",
                "usage_hours": 3,
            },
        ],
    }
    return render(request, 'payment/payment_history.html', mock_data)

# 支付成功
def payment_success(request, rental_id):
    mock_data = {
        "payment": {
            "payment_id": 20250305,
            "payment_amount": 12.50,
            "usage_hours": 2,
        },
        "rental": {
            "customer_id": {"customer_name": "John Doe"},
        },
        "wallet_balance": 50.00,
    }
    return render(request, 'payment/payment_success.html', mock_data)
