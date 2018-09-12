from django.shortcuts import render


# Create your views here.
def index(request):
    header_str = ['192.168.1.15', '192.168.1.16', '192.168.1.17', '192.168.1.18']
    context = {
        'var': header_str,
    }
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def forms(request):
    return render(request, 'forms.html')


def d1config(request):
    return render(request, 'd1config.html')


def cmd(request):
    return render(request, 'commandLine.html')


def rack_detail(request):
    host_rpi = 'Raspi_1'
    ip_rpi = '192.168.1.15'
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


def node_detail(request):
    header_str = 'test'
    fan = 'true'
    power = 'true'
    temp = 'true'
    context = {
        'var1': header_str,
        'fan': fan,
        'power': power,
        'temp': temp
    }
    return render(request, 'node_detail.html', context)


def template_file(request):
    return render(request, 'template_file.html')