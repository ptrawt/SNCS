from django.shortcuts import render, redirect, HttpResponse
from .models import *
import json
import datetime
from . import forms
from subprocess import run, PIPE
from django.contrib.auth.decorators import login_required
from django.conf import settings
media_url = settings.MEDIA_ROOT

import socket

count = 0
count_cli = 0
sock_cli = ''
user_use_dic = {}


# Create your views here.
def connection_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # host = '192.168.1.22'  # Get local machine name
    # port = 30002  # Reserve a port for your service.
    sock.connect((host, port))

    return sock


def send_receive(host, port, inp):
    sock = connection_socket(host, port)
    sock.send(inp.encode())
    while True:
        reply = sock.recv(4096)
        data = reply.decode()
        if 'Connect close...' == data:
            return data
            break
        else:
            sock.send(b'end:')
            return data

    sock.close()
    # Close the socket when done


@login_required(login_url='/accounts/login/')
def index(request):
    user = User.objects.all()
    controller_set = Controller.objects.all()
    devices_set = Network_devices.objects.all()
    detail = Detail.objects.all()
    sta_down = len(devices_set) - len(detail.filter(status='Up'))
    name_model = ''
    count_model = ''
    for i in Model.objects.all():
        name_model += i.name + ','
        count_model += str((len(devices_set.filter(modID=i.id)))) + ','

    using_config = []
    # print(user_use_dic.items())
    for j, k in user_use_dic.items():
        if j == '0':
            pass
        else:
            data = devices_set.get(ser_num=j)
            using_config.append([k, data.con_id.hostname, data.hostname])
    # print(using_config)

    context = {
        'var': controller_set,
        'rack_count': len(controller_set),
        'devices_count': len(devices_set),
        'sta_up': len(detail.filter(status='Up')),
        'sta_down': sta_down,
        'model': name_model,
        'count_model': count_model,
        'users': user,
        'using_config': using_config

    }
    return render(request, 'index.html', context)


def uploaded_file(f, port, console_pass, enable_pass):
    inp = '1:' + port + ':' + console_pass + ':' + enable_pass + ':'
    for chunk in f.chunks():
        chunk2 = chunk.decode()
        for i in chunk2.split('\r\n'):
            inp += i + ','

    data = run(['python', 'C:\\Users\\dell\\Desktop\\python\\server\\client_config.py'],
               stdout=PIPE, input=inp, encoding='ascii')

    return data.stdout


def uploaded_file2(f, port, console_pass, enable_pass, device):
    inp = '1:' + port + ':' + console_pass + ':' + enable_pass + ':'
    for chunk in f.chunks():
        chunk2 = chunk.decode()
        for i in chunk2.split('\r\n'):
            inp += i + ','
            if 'pass' in i:
                if 'en' in i:
                    i = i.split(' ')
                    device.console_pass = i[len(i) - 1]
                else:
                    i = i.split(' ')
                    device.enable_pass = i[len(i) - 1]
    device.save()

    return inp


@login_required(login_url='/accounts/login/')
def d1config(request, sn, username):
    controller = Controller.objects.all()
    model = Model.objects.all()
    devices = Network_devices.objects.all()
    port = Detail.objects.all()
    user = User.objects.get(username=username)
    sett = []
    data_write = ''
    time = datetime.datetime.now()
    time_to_filename = time.strftime("%Y%m%d-%H%M%S")
    lis_user = []
    for u in user_use_dic.keys():
        lis_user.append(u)

    if request.method == 'POST':
        form = forms.addConfig(request.POST, request.FILES)
        if form.is_valid():
            console_pass = form.cleaned_data['console_pass']
            print(console_pass)
            enable_pass = form.cleaned_data['enable_pass']
            print(enable_pass)
            script = form.cleaned_data['script']
            p_ser = port.get(ser_num=sn)
            if script == '':
                result = uploaded_file(request.FILES['upload'], p_ser.serial_port, console_pass, enable_pass)
                for line in result.split(','):
                    data_write += line + '\r\n'
                    sett.append(line)
                with open('C:/Users/dell/Documents/GitHub/SNCS/website/data/logging_config/'
                          + sn + '_' + time_to_filename + '.txt', 'wb+') as destination:
                    destination.write(data_write.encode())
                insert_man = Management(userID_id=user.id, ser_num_id=sn,
                                        new_config=sn + '_' + time_to_filename + '.txt')
                insert_man.save()

                return render(request, 'config_success.html', {'var': sett})
            else:
                inp = '1:' + p_ser.serial_port + ':' + console_pass + ':' + enable_pass + ':'
                for i in script.split('\r\n'):
                    inp += i + ','
                data = run(['python', 'C:\\Users\\dell\\Desktop\\python\\server\\client_config.py'],
                           stdout=PIPE, input=inp, encoding='ascii')
                out = data.stdout
                for line in out.split(','):
                    data_write += line+'\r\n'
                    sett.append(line)
                with open('C:/Users/dell/Documents/GitHub/SNCS/website/data/logging_config/'
                          + sn + '_' + time_to_filename + '.txt', 'wb+') as destination:
                    destination.write(data_write.encode())
                insert_man = Management(userID_id=user.id, ser_num_id=sn,
                                        new_config=sn + '_' + time_to_filename + '.txt')
                insert_man.save()

                return render(request, 'config_success.html', {'var': sett})
    else:
        form = forms.addConfig()

    context = {
        'controller': controller,
        'model': model,
        'net_device': devices,
        'sn': sn,
        'form': form,
        'user_use': lis_user
    }

    return render(request, 'd1config.html', context)


@login_required(login_url='/accounts/login/')
def d1config2(request, sn, username):
    controller = Controller.objects.all()
    model = Model.objects.all()
    devices = Network_devices.objects.all()
    port = Detail.objects.all()
    user = User.objects.get(username=username)
    sett = []
    data_write = ''
    time = datetime.datetime.now()
    time_to_filename = time.strftime("%Y%m%d-%H%M%S")
    lis_user = []
    for u in user_use_dic.keys():
        lis_user.append(u)

    if request.method == 'POST':
        form = forms.addConfig(request.POST, request.FILES)
        if form.is_valid():
            console_pass = form.cleaned_data['console_pass']
            enable_pass = form.cleaned_data['enable_pass']
            script = form.cleaned_data['script']
            p_ser = port.get(ser_num=sn)
            if script == '':
                inp = uploaded_file2(request.FILES['upload'], p_ser.serial_port, console_pass, enable_pass
                                     , devices.get(ser_num=sn))
                data = send_receive(devices.get(ser_num=sn).con_id.ip, 30002, inp)
                for line in data.split(','):
                    data_write += line + '\r\n'
                    sett.append(line)
                with open(media_url + '/logging_config/' + sn + '_' + time_to_filename + '.txt', 'wb+') as destination:
                    destination.write(data_write.encode())
                mgmt = Management(userID_id=user.id, ser_num_id=sn, new_config=sn + '_' + time_to_filename + '.txt')
                mgmt.save()

                return render(request, 'config_success.html', {'var': sett})
            else:
                inp = '1:' + p_ser.serial_port + ':' + console_pass + ':' + enable_pass + ':'
                nd = devices.get(ser_num=sn)
                for i in script.split('\r\n'):
                    inp += i + ','
                    if 'pass' in i:
                        if 'en' in i:
                            i = i.split(' ')
                            nd.console_pass = i[len(i) - 1]
                        else:
                            i = i.split(' ')
                            nd.enable_pass = i[len(i) - 1]
                nd.save()

                data = send_receive(devices.get(ser_num=sn).con_id.ip, 30002, inp)
                for line in data.split(','):
                    data_write += line+'\r\n'
                    sett.append(line)
                with open(media_url + '/logging_config/' + sn + '_' + time_to_filename + '.txt', 'wb+') as destination:
                    destination.write(data_write.encode())
                mgmt = Management(userID_id=user.id, ser_num_id=sn, new_config=sn + '_' + time_to_filename + '.txt')
                mgmt.save()

                return render(request, 'config_success.html', {'var': sett})
    else:
        form = forms.addConfig()

    context = {
        'controller': controller,
        'model': model,
        'net_device': devices,
        'sn': sn,
        'form': form,
        'user_use': lis_user
    }

    return render(request, 'd1config.html', context)


@login_required(login_url='/accounts/login/')
def cmd(request, sn, user):
    controller = Controller.objects.all()
    model = Model.objects.all()
    devices = Network_devices.objects.all()

    lis_user = []
    for u in user_use_dic.keys():
        lis_user.append(u)

    # if request.method == 'POST':
    #     ser_num = request.POST.get("sn", "")
    #     username = request.POST.get("user", "")
    #     print(ser_num+'/'+username)
    #     port = port.get(ser_num=sn)
    #     # print(command)
    #     inp = '2:' + port.serial_port + ':' + command
    #     data = run(['python', 'C:\\Users\\dell\\Desktop\\python\\server\\client_config.py'],
    #                stdout=PIPE, input=inp, encoding='ascii')
    #     data_out = data.stdout
    #     data_out = data_out.split('\n')
    #     # print(data_out)
    #
    #     del data_out[0]
    #     # print(data_out)
    #     # print(len(data_out))
    #     output = ''
    #     count = 0
    #     for i in data_out:
    #         if i == '':
    #             count += 1
    #             pass
    #         elif 'Connect close' in i:
    #             count += 1
    #             pass
    #         else:
    #             if count != len(data_out) - 3:
    #                 output += i + '\n'
    #                 count += 1
    #             else:
    #                 output += i
    #
    #     # print(output.encode())
    #
    #     response_data = {}
    #     try:
    #         response_data['result'] = 'Input success.'
    #         response_data['message'] = output
    #     except:
    #         response_data['result'] = 'Oh No'
    #         response_data['message'] = 'subprocess is not run'
    #
    #     return HttpResponse(json.dumps(response_data), content_type='application/json')

    context = {
        'controller': controller,
        'model': model,
        'net_device': devices,
        'sn': sn,
        'user_use': lis_user
    }

    return render(request, 'commandLine.html', context)


@login_required(login_url='/accounts/login/')
def cli(request, sn, username):
    devices = Network_devices.objects.all()
    port = Detail.objects.all()
    serial_port = port.get(ser_num=sn).serial_port
    ser_port_num = int(''.join([n for n in serial_port if n.isdigit()]))
    global user_use_dic
    user_use_dic[sn] = username
    global count_cli
    global sock_cli
    if count_cli == 0:
        sock_cli = connection_socket(devices.get(ser_num=sn).con_id.ip, 30003)
    else:
        pass
    count_cli += 1

    if request.method == 'POST':
        command = request.POST.get("command", "")
        port = port.get(ser_num=sn)
        inp = port.serial_port + ':' + command
        nd = devices.get(ser_num=sn)
        if 'pass' in command:
            if 'en' in command:
                en_pss = command.split(' ')
                nd.console_pass = en_pss[len(en_pss) - 1]
            else:
                con_pss = command.split(' ')
                nd.enable_pass = con_pss[len(con_pss) - 1]
        nd.save()

        if command == 'stop':
            # inp = 'end:'
            # sock_cli.send(inp.encode())
            user_use_dic.pop(sn)
            # count_cli = 0
        else:
            try:
                sock_cli.send(inp.encode())
                reply = sock_cli.recv(2048)
            except:
                data_out = 'insert command again.'
            else:
                data = reply.decode()
                data = data.split('\n')
                del data[0]
                data_out = ''
                for d in data:
                    data_out += d + '\n'
        # print(data.encode())
    #     data_out = data_out.split('\n')
    #     print(data_out)
    #
    #     del data_out[0]
    #     print(data_out)
    #     print(len(data_out))
    #     output = ''
    #     count = 0
    #     for i in data_out:
    #         if i == '':
    #             count += 1
    #             pass
    #         elif 'Connect close' in i:
    #             count += 1
    #             pass
    #         else:
    #             if count != len(data_out) - 3:
    #                 output += i + '\n'
    #                 count += 1
    #             else:
    #                 output += i
    #
    #     # print(output.encode())
    #
        response_data = {}
        try:
            response_data['result'] = 'Input success.'
            response_data['message'] = data_out
        except:
            response_data['result'] = 'Oh No'
            response_data['message'] = 'subprocess is not run'

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return render(request, 'cli.html', {'sn': sn})


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
            temp += v_temp[0] + ','
            hum += v_hum[0] + ','
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
        'humidity': hum,

    }
    return render(request, 'rack_detail.html', context)


@login_required(login_url='/accounts/login/')
def node_detail(request, ip, id):
    detail = Detail.objects.get(ser_num=id)
    device = Network_devices.objects.get(ser_num=id)
    lis_user = []
    for u in user_use_dic.keys():
        lis_user.append(u)

    context = {
        'var1': id,
        'ip_rpi': ip,
        'detail': detail,
        'device': device,
        'user_use': lis_user
    }
    return render(request, 'node_detail.html', context)


@login_required(login_url='/accounts/login/')
def template_file(request):
    file = Base_template.objects.all()
    devices = Devices.objects.all()
    model = Model.objects.all()
    model_set = [['Select courses']]
    for d in devices:
        filtered_model = []
        for m in model:
            if m.devID.id == d.id:
                filtered_model.append(m.name)
        model_set.append(filtered_model)

    if request.method == 'POST':
        form = forms.UploadBasetemp(request.POST, request.FILES)
        if form.is_valid():
            # save base to db
            instance = form.save(commit=False)
            instance.save()

            return redirect('template_file')
    else:
        form = forms.UploadBasetemp()

    return render(request, 'template_file.html', {'file': file, 'form': form})


@login_required(login_url='/accounts/login/')
def delete_base_file(request, id):
    file = Base_template.objects.get(id=id)
    file.delete()

    return redirect('template_file')


@login_required(login_url='/accounts/login/')
def view_base_file(request, id, files):
    if id == '0':
        config_f_name = Management.objects.get(id=files)
        fo = open(media_url + '/logging_config/' + config_f_name.new_config, "r")
        txt = fo.read()
        txt = txt.split('\n')
        file_name = config_f_name.new_config
    else:
        file = Base_template.objects.get(id=id)
        fo = open(media_url + '/' + file.upload.name, "r")
        txt = fo.read()
        txt = txt.split('\n')
        file_name = file.upload.name

    return render(request, 'view_base_file.html', {'txt': txt, 'name': file_name})


@login_required(login_url='/accounts/login/')
def logging(request):
    manage_data = Management.objects.all()

    return render(request, 'logging.html', {'data': manage_data})


def cli_success(request, sn):
    user_use_dic.pop(sn)
    return render(request, 'commandLine.html')
