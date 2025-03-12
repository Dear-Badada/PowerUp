from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages

from powerbank.models import Pricing
from users.models import User
from .models import Order, PowerBank, Transaction, RefundRequest
from django.utils import timezone


def create_order(request, power_bank_id):
    """ 用户开启租借，支付押金 """
    power_bank = PowerBank.objects.get(id=power_bank_id)

    if power_bank.status != 'available':
        messages.error(request, "The power bank is not available.")
        return redirect('home')  # 如果充电宝不可用，返回首页

    # 获取租赁单价和押金
    pricing = Pricing.objects.first()
    deposit = pricing.deposit_amount
    hourly_rate = pricing.hourly_rate

    login_user = User.objects.get(id=request.session['user_id'])

    # 创建订单
    order = Order.objects.create(
        user=login_user,
        power_bank=power_bank,
        deposit=deposit,
        hourly_rate=hourly_rate,
        order_status='ongoing',
        payment_status='pending'
    )

    # 更新充电宝状态为租借中
    power_bank.status = 'rented'
    power_bank.save()

    # 从用户余额中扣除押金
    login_user.balance -= Decimal(order.deposit)
    login_user.save()

    # 记录充值交易（假设从用户余额中扣除押金）
    transaction = Transaction.objects.create(
        user=login_user,
        type='deposit',
        amount=deposit,
        order=order
    )
    transaction.save()

    messages.success(request, f"Order created successfully. Your deposit is ${deposit}.")
    return redirect('view_order', order_id=order.id)


def return_order(request, order_id):
    """ 用户归还充电宝，结算费用 """
    order = Order.objects.get(id=order_id)

    if order.order_status == 'completed':
        messages.info(request, "This order is already completed.")
        return redirect('home')

    # 结束租借，计算总费用
    end_time = timezone.now()
    duration = (end_time - order.start_time).total_seconds() / 3600  # 计算租借时长，单位为小时
    total_cost = Decimal(duration) * order.hourly_rate  # 总费用 = 时长 * 每小时费用

    # 从押金中扣除费用
    remaining_balance = order.deposit - total_cost
    if remaining_balance < 0:
        remaining_balance = 0  # 如果费用大于押金，不退还余额

    # 更新订单
    order.end_time = end_time
    order.total_cost = total_cost
    order.payment_status = 'paid' if remaining_balance == 0 else 'pending'
    order.order_status = 'completed'  # 订单完成
    order.save()

    # 更新充电宝状态
    PowerBank.objects.filter(id=order.power_bank_id).update(status='available')

    # 更新用户钱包余额
    user = order.user
    user.balance += remaining_balance
    user.save()

    # 创建支付交易记录
    Transaction.objects.create(
        user=user,
        type='rental_fee',
        amount=total_cost,
        order=order
    )

    messages.success(request, f"Order completed. Total cost is ${total_cost}. Remaining balance: ${remaining_balance}.")
    return redirect('view_order', order_id=order.id)


def report_feedback(request, order_id):
    """ 用户反馈充电宝状态，并申请退款（如果异常）"""
    order = Order.objects.get(id=order_id)

    if order.order_status == 'completed':
        messages.error(request, "This order has already been completed.")
        return redirect('home')

    feedback = request.POST.get('feedback', 'abnormal')  # 默认为异常
    if feedback == 'abnormal':
        # 如果是异常，创建退款申请
        login_user = User.objects.get(id=request.session['user_id'])
        RefundRequest.objects.create(
            order=order,
            user=login_user,
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


def view_order(request, order_id):
    """ 查看订单详情 """
    order = Order.objects.get(id=order_id)

    return render(request, "users/order_detail.html", {"order": order})
