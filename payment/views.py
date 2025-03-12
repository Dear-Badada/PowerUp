from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from payment.models import Order, Transaction, RefundRequest
from powerbank.models import PowerBank, Pricing
from users.models import User


# ======【支付相关】======
@login_required
def payment_details(request, order_id):
    """支付详情"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment/payment_details.html', {
        "order": order,
        "payment_amount": order.total_cost,
        "remaining_balance": order.user.balance,
        "start_station_name": order.power_bank.station.name,
        "end_station_name": order.power_bank.station.name,
    })


@login_required
def payment_history(request, customer_id):
    """查看用户支付历史"""
    user = get_object_or_404(User, id=customer_id)
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')
    return render(request, 'payment/payment_history.html', {"user": user, "transactions": transactions})


@login_required
def payment_success(request, order_id):
    """支付成功页面"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment/payment_success.html', {
        "order": order,
        "message": "Payment Successful!",
        "total_cost": order.total_cost,
    })


# ======【订单管理】======
@login_required
@csrf_protect
def create_order(request, power_bank_id):
    """用户开启租借，支付押金"""
    power_bank = get_object_or_404(PowerBank, id=power_bank_id, status='available')

    # 获取租赁单价和押金
    pricing = Pricing.objects.first()
    deposit = pricing.deposit_amount if pricing else Decimal("15.00")
    hourly_rate = pricing.hourly_rate if pricing else Decimal("1.00")

    user = get_object_or_404(User, id=request.session['user_id'])

    if user.balance < deposit:
        messages.error(request, "Insufficient balance. Please recharge.")
        return redirect('recharge_wallet')

    # 创建订单
    order = Order.objects.create(
        user=user,
        power_bank=power_bank,
        deposit=deposit,
        hourly_rate=hourly_rate,
        order_status='ongoing',
        payment_status='pending'
    )

    # 更新充电宝状态
    power_bank.status = 'in_use'
    power_bank.save()

    # 从用户余额扣除押金
    user.balance -= deposit
    user.save()

    # 记录押金交易
    Transaction.objects.create(user=user, type='deposit', amount=deposit, order=order)

    messages.success(request, f"Order created successfully. Your deposit is ${deposit}.")
    return redirect('view_order', order_id=order.id)


@login_required
@csrf_protect
def return_order(request, order_id):
    """用户归还充电宝，结算费用"""
    order = get_object_or_404(Order, id=order_id)

    if order.order_status == 'completed':
        messages.info(request, "This order is already completed.")
        return redirect('home')

    # 计算租借费用
    end_time = timezone.now()
    duration = (end_time - order.start_time).total_seconds() / 3600  # 小时计算
    total_cost = max(Decimal(duration) * order.hourly_rate, Decimal("0.00"))  # 避免负数

    # 计算退款金额
    remaining_balance = max(order.deposit - total_cost, Decimal("0.00"))

    # 更新订单状态
    order.end_time = end_time
    order.total_cost = total_cost
    order.payment_status = 'paid' if remaining_balance == 0 else 'pending'
    order.order_status = 'completed'
    order.save()

    # 更新充电宝状态
    order.power_bank.status = 'available'
    order.power_bank.save()

    # 退款到用户钱包
    user = order.user
    user.balance += remaining_balance
    user.save()

    # 记录支付交易
    Transaction.objects.create(user=user, type='rental_fee', amount=total_cost, order=order)

    messages.success(request, f"Order completed. Total cost: ${total_cost}. Remaining balance: ${remaining_balance}.")
    return redirect('view_order', order_id=order.id)


@login_required
def view_order(request, order_id):
    """查看订单详情"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, "users/order_detail.html", {"order": order})


# ======【用户反馈】======
@login_required
def report_feedback(request, order_id):
    """ 用户反馈充电宝状态，申请退款 """
    order = get_object_or_404(Order, id=order_id)

    if order.order_status == 'completed':
        messages.error(request, "This order has already been completed.")
        return redirect('home')

    feedback = request.POST.get('feedback', 'abnormal')

    if feedback == 'abnormal':
        RefundRequest.objects.create(
            order=order,
            user=order.user,
            status='pending',
            reason="Abnormal feedback on power bank.",
        )
        order.feedback = 'abnormal'
        order.save()
        messages.success(request, "Refund request submitted successfully.")
    else:
        order.feedback = 'normal'
        order.save()
        messages.success(request, "Feedback recorded as normal.")

    return redirect('view_order', order_id=order.id)
