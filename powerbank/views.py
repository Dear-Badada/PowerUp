from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Station, PowerBank

def station_list(request):
    """ 显示所有站点 """
    stations = Station.objects.all()
    return render(request, "powerbank/stations.html", {"stations": stations})

def station_detail(request, station_id):
    """ 显示站点的所有可用充电宝 """
    station = get_object_or_404(Station, id=station_id)
    available_power_banks = PowerBank.objects.filter(station=station, status='available')
    return render(request, "powerbank/station_detail.html", {"station": station, "power_banks": available_power_banks})