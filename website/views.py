from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    controller_set = Controller.objects.all()
    devices_set = Network_devices.objects.all()
    context = {
        'var': controller_set,
        'rack_count': len(controller_set),
        'devices_count': len(devices_set)
    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def forms(request):
    return render(request, 'forms.html')


def d1config(request, sn):
    devices = Network_devices.objects.all()
    lis = []
    for i in devices:
        lis.append(i.ser_num)

    if sn == '0':
        serial = lis
    else:
        serial = sn

    context = {
        'sn': serial
    }

    return render(request, 'd1config.html', context)


def cmd(request):
    return render(request, 'commandLine.html')


def rack_detail(request, ip):
    ip_rpi = ip
    host_rpi = 'Raspi_1'
    ip_nd = ['100.10.1.10', '100.10.1.11', '100.10.1.12', '100.10.1.13']
    sn_nd = ['FOC1111Z352', 'FOC1111Z353', 'FOC1111Z354', 'FOC1111Z355']
    count_nd = len(sn_nd)
    context = {
        'host_rpi': host_rpi,
        'ip_rpi': ip_rpi,
        'ip_nd': ip_nd,
        'sn_nd': sn_nd,
        'count_nd': count_nd

    }
    return render(request, 'rack_detail.html', context)


def node_detail(request, ip, sn):
    host = sn
    ipRpi = ip
    fan = 'true'
    power = 'true'
    temp = 'true'
    context = {
        'var1': host,
        'ip_rpi': ipRpi,
        'fan': fan,
        'power': power,
        'temp': temp
    }
    return render(request, 'node_detail.html', context)


def template_file(request):
    return render(request, 'template_file.html')