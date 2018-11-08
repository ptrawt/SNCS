from django.shortcuts import render, redirect, HttpResponse
from .models import *
import json
from . import forms
from subprocess import run, PIPE
from django.contrib.auth.decorators import login_required
count = 0


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    controller_set = Controller.objects.all()
    devices_set = Network_devices.objects.all()
    detail = Detail.objects.all()
    sta_down = len(devices_set) - len(detail.filter(status='Up'))
    name_model = ''
    count_model = ''
    for i in Model.objects.all():
        name_model += i.name+','
        count_model += str((len(devices_set.filter(modID=i.id))))+','

    context = {
        'var': controller_set,
        'rack_count': len(controller_set),
        'devices_count': len(devices_set),
        'sta_up': len(detail.filter(status='Up')),
        'sta_down': sta_down,
        'model': name_model,
        'count_model': count_model

    }
    return render(request, 'index.html', context)


def uploaded_file(f, port):
    inp = '1:'+port+':'
    with open('C:/Users/dell/Documents/GitHub/SNCS/website/data/config/config_script.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            chunk2 = chunk.decode()
            for i in chunk2.split('\r\n'):
                inp += i+','

        data = run(['python', 'C:\\Users\\dell\\Desktop\\python\\server\\client_config.py'],
                   stdout=PIPE, input=inp, encoding='ascii')

        return data.stdout


@login_required(login_url='/accounts/login/')
def d1config(request, sn):
    controller = Controller.objects.all()
    model = Model.objects.all()
    devices = Network_devices.objects.all()
    port = Detail.objects.all()
    sett = []

    if request.method == 'POST':
        form = forms.addConfig(request.POST, request.FILES)
        if form.is_valid():
            script = form.cleaned_data['script']
            p_ser = port.get(ser_num=sn)
            if script == '':
                result = uploaded_file(request.FILES['upload'], p_ser.serial_port)
                for line in result.split(','):
                    sett.append(line)
                return render(request, 'config_success.html', {'var': sett})
            else:
                inp = '1:'+p_ser.serial_port+':'
                for i in script.split('\r\n'):
                    inp += i+','
                data = run(['python', 'C:\\Users\\dell\\Desktop\\python\\server\\client_config.py'],
                           stdout=PIPE, input=inp, encoding='ascii')
                out = data.stdout
                for line in out.split(','):
                    sett.append(line)
                with open('C:/Users/dell/Documents/GitHub/SNCS/website/data/config/config_script.txt', 'wb+') as destination:
                    destination.write(script.encode())

                return render(request, 'config_success.html', {'var': sett})
    else:
        form = forms.addConfig()

    context = {
        'controller': controller,
        'model': model,
        'net_device': devices,
        'sn': sn,
        'form': form
    }

    return render(request, 'd1config.html', context)


@login_required(login_url='/accounts/login/')
def cmd(request, sn):
    controller = Controller.objects.all()
    model = Model.objects.all()
    devices = Network_devices.objects.all()
    port = Detail.objects.all()
    sett = []
    global count

    if request.method == 'POST':
        command = request.POST.get("command", "")
        port = port.get(ser_num=sn)
        # print(command)
        inp = '2:' + port.serial_port + ':' + command
        data = run(['python', 'C:\\Users\\dell\\Desktop\\python\\server\\client_config.py'],
                   stdout=PIPE, input=inp, encoding='ascii')
        data_out = data.stdout
        data_out = data_out.split('\n')
        # print(data_out)

        del data_out[0]
        print(data_out)
        print(len(data_out))
        output = ''
        count = 0
        for i in data_out:
            if i == '':
                count += 1
                pass
            elif 'Connect close' in i:
                count += 1
                pass
            else:
                if count != len(data_out)-3:
                    output += i+'\n'
                    count += 1
                else:
                    output += i

        print(output.encode())

        response_data = {}
        try:
            response_data['result'] = 'Input success.'
            response_data['message'] = output
        except:
            response_data['result'] = 'Oh No'
            response_data['message'] = 'subprocess is not run'

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    '''
    if request.method == 'POST':
        form = forms.cmd(request.POST)
        if form.is_valid():
            data_in = form.cleaned_data['data_in']
            port = port.get(ser_num=sn)
            #if data_in == '':
             #   data_in += '\r\n'
            #print(data_in.encode())
            inp = '2:'+port.serial_port+':'+data_in
            data = run(['python', 'C:\\Users\\dell\\Desktop\\python\\server\\client_config.py'],
                       stdout=PIPE, input=inp, encoding='ascii')
            data_out = data.stdout
            #print(data.stdout)
            for line in data_out.split(','):
                for out in line.split('\n'):
                    if out == '':
                        pass
                    elif 'Connect close' in out:
                        pass
                    elif out == data_in:
                        pass
                    elif out == '1':
                        pass
                    else:
                        sett.append(out+'\n')
            #print(sett)
            with open('C:/Users/dell/Documents/GitHub/SNCS/website/data/config/cmd_logging_'+sn+'.txt', 'ab+') as destination:
                destination.write(data_out.encode())

            form = forms.cmd()
            return render(request, 'commandLine.html', {'var': sett, 'form': form})
    else:
        form = forms.cmd()
    '''

    context = {
        'controller': controller,
        'model': model,
        'net_device': devices,
        'sn': sn,
        #'form': form
    }

    return render(request, 'commandLine.html', context)


@login_required(login_url='/accounts/login/')
def rack_detail(request, ip):
    controller = Controller.objects.get(ip=ip)
    net_device = Network_devices.objects.filter(con_id=controller.id)
    name_dev = ''
    count_dev = ''
    sensor = [controller.sensor1, controller.sensor2, controller.sensor3, controller.sensor4]
    temp = ''
    hum = ''
    c = 0

    for j in sensor:
        c += 1
        var = j.split(' ')
        var1 = var[0].split('=')
        v_temp = var1[1].split('*')
        var2 = var[1].split('=')
        v_hum = var2[1].split('%')
        if c != 4:
            temp += v_temp[0]+','
            hum += v_hum[0]+','
        else:
            temp += v_temp[0]
            hum += v_hum[0]

    for i in net_device.all():
        if i.devID.name not in name_dev:
            name_dev += i.devID.name + ','
            count_dev += str(len(net_device.filter(devID=i.devID))) + ','
        else:
            pass

    context = {
        'controller': controller,
        'ip_rpi': ip,
        'sn_nd': net_device,
        'dev': name_dev,
        'count_dev': count_dev,
        'temp': temp,
        'humidity': hum

    }
    return render(request, 'rack_detail.html', context)


@login_required(login_url='/accounts/login/')
def node_detail(request, ip, id):
    det = Detail.objects.get(ser_num=id)
    dev = Network_devices.objects.get(ser_num=id)
    context = {
        'var1': id,
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


@login_required(login_url='/accounts/login/')
def template_file(request):
    file = Base_template.objects.all()
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

    if request.method == 'POST':
        form = forms.UploadBasetemp(request.POST, request.FILES)
        if form.is_valid():
            # save base to db
            instance = form.save(commit=False)
            instance.save()

            return redirect('template_file')
    else:
        form = forms.UploadBasetemp()

    context = {
        'file': file,
        'dev': devices.order_by('name'),
        'mod': models,
        'model': json.dumps(model),
        'form': form
    }

    return render(request, 'template_file.html', context)


@login_required(login_url='/accounts/login/')
def delete_base_file(request, id):
    file = Base_template.objects.get(id=id)
    file.delete()

    return redirect('template_file')


@login_required(login_url='/accounts/login/')
def view_base_file(request, id):
    file = Base_template.objects.get(id=id)
    fo = open("C:/Users/dell/Documents/GitHub/SNCS/website/data/"+file.upload.name, "r")
    txt = fo.read()
    txt = txt.split('\n')

    return render(request, 'view_base_file.html', {'txt': txt, 'name': file.upload.name})