from django.shortcuts import render
from .models import *
import json


# Create your views here.
def index(request):
    controller_set = Controller.objects.all()
    devices_set = Network_devices.objects.all()
    detail = Detail.objects.all()
    sta_down = len(devices_set) - len(detail.filter(status='Up'))
    name_dev = ''
    count_dev = ''
    for i in Devices.objects.all():
        name_dev += i.name+','
        count_dev += str((len(devices_set.filter(devID=i.id))))+','

    context = {
        'var': controller_set,
        'rack_count': len(controller_set),
        'devices_count': len(devices_set),
        'sta_up': len(detail.filter(status='Up')),
        'sta_down': sta_down,
        'dev': name_dev,
        'count_dev': count_dev

    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def d1config(request, sn):
    devices = Network_devices.objects.all()
    sn_all = []
    d_all = []
    m_all = []
    c_all = []
    hn_all = []
    for i in devices:
        sn_all.append(i.ser_num)
        hn_all.append(i.hostname)
        if len(c_all) == 0:
            c_all.append(i.con_id.hostname)
        elif i.con_id.hostname == c_all[0]:
            pass
        if len(d_all) == 0:
            d_all.append(i.devID)
        elif i.devID == d_all[0]:
            pass
        m_all.append(i.modID)

    if sn == '0':
        serial = sn_all
        host = hn_all
        cont = c_all
        dev = d_all
        mod = m_all
    else:
        serial = [sn]
        d = devices.filter(ser_num=sn)
        for i in d:
            cont = [i.con_id.hostname]
            dev = [i.devID.name]
            mod = [i.modID.name]
            host = [i.hostname]

    context = {
        'sn': serial,
        'cont': cont,
        'dev': dev,
        'mod': mod,
        'host': host
    }

    return render(request, 'd1config.html', context)


def cmd(request, sn):
    devices = Network_devices.objects.all()
    sn_all = []
    d_all = []
    m_all = []
    c_all = []
    hn_all = []
    for i in devices:
        sn_all.append(i.ser_num)
        hn_all.append(i.hostname)
        if len(c_all) == 0:
            c_all.append(i.con_id.hostname)
        elif i.con_id.hostname == c_all[0]:
            pass
        if len(d_all) == 0:
            d_all.append(i.devID)
        elif i.devID == d_all[0]:
            pass
        m_all.append(i.modID)

    if sn == '0':
        serial = sn_all
        host = hn_all
        cont = c_all
        dev = d_all
        mod = m_all
    else:
        serial = [sn]
        d = devices.filter(ser_num=sn)
        for i in d:
            cont = [i.con_id.hostname]
            dev = [i.devID.name]
            mod = [i.modID.name]
            host = [i.hostname]

    context = {
        'sn': serial,
        'cont': cont,
        'dev': dev,
        'mod': mod,
        'host': host
    }

    return render(request, 'commandLine.html', context)


def rack_detail(request, ip):
    var1 = Controller.objects.get(ip=ip)
    net_device = Network_devices.objects.filter(con_id=var1.id)
    host_rpi = var1.hostname
    ip_nd = ['100.10.1.10', '100.10.1.11', '100.10.1.12', '100.10.1.13']
    sn_nd = net_device
    name_dev = ''
    count_dev = ''
    print(net_device)
    for i in net_device.all():
        if i.devID.name not in name_dev:
            name_dev += i.devID.name + ','
            count_dev += str(len(net_device.filter(devID=i.devID))) + ','
        else:
            pass

    context = {
        'host_rpi': host_rpi,
        'ip_rpi': ip,
        'ip_nd': ip_nd,
        'sn_nd': sn_nd,
        'dev': name_dev,
        'count_dev': count_dev

    }
    return render(request, 'rack_detail.html', context)


def node_detail(request, ip, sn):
    det = Detail.objects.get(ser_num=sn)
    dev = Network_devices.objects.get(ser_num=sn)
    context = {
        'var1': sn,
        'ip_rpi': ip,
        'det': det,
        'fan': det.fan,
        'power': det.power,
        'temp': det.temp,
        'host': dev.hostname,
        'dev': dev.devID.name,
        'mod': dev.modID.name
    }
    return render(request, 'node_detail.html', context)


def template_file(request):
    devices = Devices.objects.all()
    models = Model.objects.all()

    model = []
    model.append(['Select courses'])
    for d in devices:
        filtered_model = []
        for m in models:
            if m.devID.id == d.id:
                filtered_model.append(m.name)
        model.append(filtered_model)

    print(model)
    context = {
        'dev': devices.order_by('name'),
        'mod': models,
        'model': json.dumps(model)
    }

    return render(request, 'template_file.html', context)


