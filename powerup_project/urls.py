from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from order.views import create_order, return_order, report_feedback, view_order
from powerbank.views import station_list, station_detail
from users.views import home, user_login, rent_powerbank, return_powerbank, register, recharge_wallet, view_wallet
from manager.views import manager_login_view, create_station, delete_station, powerbank_list, \
    delete_powerbank, update_powerbank_status, update_pricing, handle_refund_request, refund_requests_list, \
    manager_dashboard, station_list_manager, repair_powerbank, powerbank_details, manager_reports, refund_request_detail

urlpatterns = [
    path('', home, name='home'),  # 主页
    path('admin/', admin.site.urls),  # Django 管理后台

    # 用户相关 URL
    path('login/', user_login, name='login'),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path('register/', register, name='register'),
    path('rent/<int:powerbank_id>/', rent_powerbank, name='rent_powerbank'),
    path('return/', return_powerbank, name='return_powerbank'),
    path('recharge/', recharge_wallet, name='recharge_wallet'),
    path('wallet/', view_wallet, name='view_wallet'),

    # 订单 URL
    path("order/<int:power_bank_id>/create/", create_order, name="create_order"),  # 开启租借
    path("order/<int:order_id>/return/", return_order, name="return_order"),  # 结束租借
    path("order/<int:order_id>/feedback/", report_feedback, name="report_feedback"),  # 提交反馈
    path("order/<int:order_id>/", view_order, name="view_order"),  # 查看订单

    # 充电宝及站点 URL
    path("stations/", station_list, name="station_list"),  # 显示所有站点
    path("stations/<int:station_id>/", station_detail, name="station_detail"),  # 查看站点内的充电宝

    # 管理员登录
    path('manager/login/', manager_login_view, name='manager_login'),
    path("manager/dashboard/", manager_dashboard, name="manager_dashboard"),

    # 站点管理
    path("manager/stations/", station_list_manager, name="station_list_manager"),
    path("manager/stations/create/", create_station, name="create_station"),
    path("manager/stations/<int:station_id>/delete/", delete_station, name="delete_station"),
    path("manager/stations/<int:station_id>/powerbanks/", powerbank_list, name="powerbank_list"),

    # 充电宝管理
    path("manager/powerbanks/<int:powerbank_id>/", powerbank_details, name="powerbank_details"),
    path("manager/powerbanks/<int:powerbank_id>/repair/", repair_powerbank, name="repair_powerbank"),
    path("manager/powerbanks/<int:powerbank_id>/delete/", delete_powerbank, name="delete_powerbank"),
    path("manager/powerbanks/<int:powerbank_id>/update-status/", update_powerbank_status, name="update_powerbank_status"),

    # 报告管理
    path("manager/reports/", manager_reports, name="manager_reports"),

    # 价格管理
    path("manager/pricing/update/", update_pricing, name="update_pricing"),

    # 退款管理
    # 退款管理
    path('manager/refund-requests/', refund_requests_list, name='refund_requests_list'),
    path('manager/refund-requests/<int:refund_request_id>/', refund_request_detail, name='refund_request_detail'),
    path('manager/refund-requests/<int:refund_request_id>/handle/', handle_refund_request, name='handle_refund_request'),
]