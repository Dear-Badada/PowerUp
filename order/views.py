from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from order.models import Order, Transaction, RefundRequest
from powerbank.models import PowerBank, Pricing
from users.models import User


# ======【支付相关】======
@login_required
def payment_details(request, order_id):
    """支付详情"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/payment_details.html', {
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
    return render(request, 'order/payment_history.html', {"user": user, "transactions": transactions})


@login_required
def payment_success(request, order_id):
    """支付成功页面"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/payment_success.html', {
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

    user_id = request.session.get('user_id')

    # 如果用户未登录，跳转到登录页面
    if not user_id:
        messages.error(request, "You must log in to rent a power bank.")
        return redirect('login')

    # 获取用户
    user = get_object_or_404(User, id=user_id)

    # 获取租赁单价和押金
    pricing = Pricing.objects.first()
    deposit = pricing.deposit_amount if pricing else Decimal("15.00")
    hourly_rate = pricing.hourly_rate if pricing else Decimal("1.00")

    from django.http import HttpResponseRedirect

    if user.balance < deposit:
        messages.error(request, "Insufficient balance. Please recharge.")
        next_url = request.get_full_path()
        recharge_url = f"{reverse('recharge_wallet')}?next={next_url}"
        return HttpResponseRedirect(recharge_url)

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
    power_bank.status = 'rented'
    power_bank.save()

    # 从用户余额扣除押金
    user.balance -= deposit
    user.save()

    # 记录押金交易
    Transaction.objects.create(user=user, type='deposit', amount=deposit, order=order)

    messages.success(request, f"order created successfully. Your deposit is ${deposit}.")
    return redirect('view_order', order_id=order.id)


@login_required
@csrf_protect
def return_order(request, order_id):
    """用户归还充电宝，结算费用"""
    order = get_object_or_404(Order, id=order_id)

    if order.order_status == 'completed':
        messages.info(request, "This order is already completed.")
        return redirect('view_order', order_id=order.id)

    # 计算租借费用
    end_time = timezone.now()
    duration = (end_time - order.start_time).total_seconds() / 3600  # 计算小时数
    total_cost = max(Decimal(duration) * order.hourly_rate, Decimal("0.00"))  # 确保金额不会是负数

    # 计算用户应退款额
    refund_amount = order.deposit - total_cost  # 押金 - 租借费用
    if refund_amount < 0:
        refund_amount = Decimal("0.00")  # 防止负数退款

    # 处理欠费情况
    user = order.user
    if total_cost > order.deposit:  # 如果租金 > 押金，用户需要额外支付
        extra_payment_due = total_cost - order.deposit
        if user.balance < 0:
            messages.error(request, "Your balance is insufficient to cover the rental cost. Please recharge.")
            return redirect(
                f"{reverse('recharge_wallet')}?next={reverse('return_order', args=[order.id])}")
        user.balance -= extra_payment_due
    else:
        # 退款给用户
        user.balance += refund_amount

    # 更新用户余额
    user.save()

    # 更新订单状态
    order.end_time = end_time
    order.total_cost = total_cost
    order.payment_status = "paid"
    order.order_status = "completed"
    order.save()

    # 更新充电宝状态为已归还
    if order.power_bank.status != "available":
        order.power_bank.status = "available"
        order.power_bank.save()

    # 记录交易（押金退款或额外支付）
    Transaction.objects.create(user=user, type="rental_fee", amount=total_cost, order=order)
    if refund_amount > 0:
        Transaction.objects.create(user=user, type="refund", amount=refund_amount, order=order)

    messages.success(request, f"order completed. Total cost: £{total_cost:.2f}. Refund: £{refund_amount:.2f}.")
    return redirect("view_order", order_id=order.id)


@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # 确保所有值都是 Decimal 类型
    deposit = order.deposit if order.deposit else Decimal("0.00")
    total_cost = order.total_cost if order.total_cost else Decimal("0.00")

    # 计算退款金额（确保 Decimal 运算）
    refund_amount = deposit - total_cost
    context = {
            "order": order,
            "refund_amount": refund_amount.quantize(Decimal("0.01")),  # 保留 2 位小数
        }
    return render(request, "users/order_detail.html", context)


# ======【用户反馈】======
@login_required
def report_feedback(request, order_id):
    """ 用户反馈充电宝状态，选择异常可申请退款 """
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # 如果订单已完成，不允许反馈
        if order.order_status == 'completed':
            messages.error(request, "This order has already been completed.")
            return redirect(reverse('view_order', kwargs={'order_id': order.id}))

        # 获取用户提交的反馈类型
        feedback_type = request.POST.get('feedback_type', '').strip().lower()
        feedback_message = request.POST.get('message', '').strip()

        # 校验反馈类型是否合法
        if feedback_type not in ['abnormal', 'normal']:
            messages.error(request, "Invalid feedback type.")
            return redirect(reverse('report_feedback', kwargs={'order_id': order.id}))

        if feedback_type == 'abnormal':
            # 检查是否已提交退款申请，避免重复创建
            existing_refund = RefundRequest.objects.filter(order=order).first()
            if existing_refund:
                messages.warning(request, "A refund request for this order has already been submitted.")
                return redirect(reverse('handle_refund_request', kwargs={'refund_request_id': existing_refund.id}))
            else:
                # 创建退款申请
                refund_request = RefundRequest.objects.create(
                    order=order,
                    user=order.user,
                    status="pending",
                    reason=feedback_message or "User reported an issue with the power bank."
                )
                order.order_status = "cancelled"  # 订单取消
                order.save()
                messages.success(request, "Refund request submitted successfully.")

                # 提交反馈后跳转到退款详情页
                return redirect(reverse('handle_refund_request', kwargs={'refund_request_id': refund_request.id}))

        else:
            # 正常反馈，无需退款
            order.feedback = feedback_message
            order.save()
            messages.success(request, "Feedback recorded as normal.")

            # 只有非异常反馈才跳转回订单页面
        return redirect(reverse('view_order', kwargs={'order_id': order.id}))

        # 处理 GET 请求，渲染反馈页面
    return render(request, "users/feedback.html", {"order": order})
