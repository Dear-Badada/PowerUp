from django.contrib import admin
from django.urls import path
from payment import views as payment_views
from users.views import home, user_login, rent_powerbank, return_powerbank, register, recharge_wallet, view_wallet
from adminn.views import admin_login, admin_dashboard, admin_reports

urlpatterns = [

    path('', home, name='home'),  # 主页
    path('admin/', admin.site.urls),  # Django 管理后台

    # 用户相关 URL
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('rent/', rent_powerbank, {'powerbank_id': 1}, name='rent_default'),
    path('rent/<int:powerbank_id>/', rent_powerbank, name='rent_powerbank'),
    path('return/', return_powerbank, name='return_powerbank'),
    path('wallet/', view_wallet, name='view_wallet'),
    path('wallet/recharge/', recharge_wallet, name='recharge_wallet'),

    # 支付相关 URL
    path('payment/details/<int:rental_id>/', payment_views.payment_details, name='payment_details'),
    path('payment/history/<int:customer_id>/', payment_views.payment_history, name='payment_history'),
    path('payment/success/<int:rental_id>/', payment_views.payment_success, name='payment_success'),

    # 管理员相关 URL
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-reports/', admin_reports, name='admin_reports'),
]
