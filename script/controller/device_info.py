import serial
import sys
import time

READ_TIMEOUT = 8

def read_serial(console):

    data_bytes = console.inWaiting()
    if data_bytes:
        output = console.read(data_bytes)
        return output.decode()
    else:
        return "Not thing"


def check_logged_in(console, console_pass, enable_pass):

    console.write(b"\r")
    temp_pass = 0
    while 1:
        time.sleep(1)
        prompt = read_serial(console)
        print(prompt)
        if 'Would you like to enter the initial configuration' in prompt:
            console.write(b"no\r")
        elif 'Password' in prompt:
            if console_pass != '' and temp_pass == 0:
                console.write(console_pass.encode()+b'\n')
                print("Access to Privileged mode.")
                temp_pass += 1
            elif enable_pass != '' and temp_pass != 0:
                console.write(enable_pass.encode()+b'\n')
        elif '>' in prompt:
            console.write(b'en\n')
            temp_pass += 1
        elif '#' in prompt:
            print("Access to Enable mode.")
            if '(' in prompt or ')' in prompt:
                console.write(b"end\n")
            break

    return True


def getName(console):

    console.write(b"\n")
    time.sleep(1)
    outdata = read_serial(console)
    for line in outdata.split('\n'):
        if '#' in line:
            name = line.split('#')

    return name[0]


def showEnv(console):

    console.write(b"show env all\n")
    time.sleep(0.5)
    outdata = read_serial(console)
    for line in outdata.split('\r\n'):
        if "FAN" in line:
            fan = line.split(' ')
        elif "TEMPERATURE" in line:
            temp = line.split(' ')
        elif "POWER" in line:
            power = line.split(' ')

    return fan[2]+'\n'+temp[2]+'\n'+power[2]


def showInventory(console):

    console.write(b"show inven | include PID\n")
    time.sleep(1)
    outdata = read_serial(console)
#    print(outdata)
    pid = []
    sn = []
    for line in outdata.split('\r\n'):
        for val in line.split(', '):
            if "PID:" in val:
                a = val.split(': ')
                pid.append(a[1])
            elif "SN" in val:
                b = val.split(': ')
                sn.append(b[1])

    return sn[0]+'\n'+pid[0]


def software(console):
    console.write(b"show ver | include Software\n")
    time.sleep(0.5)
    outdata = read_serial(console)
    for line in outdata.split('\n'):
        for line2 in line.split(', '):
            if "Software (" in line2:
                sw_img = line2.split(' ')
            elif "Version" in line2:
                sw_ver = line2.split(' ')

    return sw_img[2]+'\n'+sw_ver[1]


def uptime(console):
    console.write(b"show ver | include uptime\n")
    time.sleep(0.5)
    outdata = read_serial(console)
    for line in outdata.split('\n'):
        if 'is' in line:
            data = line.split('\r')

    return data[0]


def reset(console):
    console.write(b"show ver | include reset\n")
    time.sleep(0.5)
    outdata = read_serial(console)
    for line in outdata.split('\n'):
        if "Last" in line:
            res = line.split(' ')
            data = res[3].split('\r')

    return data[0]


def interface(console):
    console.write(b"show ver | include interface\n")
    time.sleep(1)
    outdata = read_serial(console)
    outdata = outdata.split('\n')
    a = ''
    for line in outdata:
        if 'Ethernet interfaces' in line:
            lis = line.split('\r')
            a += lis[0]+': '
    return a


def manufacturer(console):
    console.write(b"show ver | include Copyright\n")
    time.sleep(0.5)
    outdata = read_serial(console)
    outdata = outdata.split('\n')
    for line in outdata:
        if 'by' in line:
            data = line.split('by')

    output = data[1].split('\r')
    return output[0]


def main(set_pass):
    port = set_pass[0]
    console_pass = set_pass[1]
    enable_pass = set_pass[2]
    print('device info start.')
    serial_port = port
    console = serial.Serial(serial_port,
        timeout=READ_TIMEOUT,
        #xonxoff=True,
        #rtscts=True,
        #dsrdtr=True
    )

    try:
        console.isOpen()
        print('serial is connect.')
        if check_logged_in(console, console_pass, enable_pass):
            print('check_logged_in is True.')
            console.write(b"terminal length 0\n")
            console.write(b"en\n")

            return (
                showInventory(console)+'\n'+
                getName(console)+'\n'+
                manufacturer(console)+'\n'+
                uptime(console)+'\n'+
                interface(console)+'\n'+
                software(console)+'\n'+
                reset(console)+'\n'+
                showEnv(console)+'\n'+
                serial_port
                )

            console.flushInput()
            console.write(b"exit\n")

        else:
            return "Down\n"+serial_port
        print('serial is close.')
        console.close()
    except:
        return "Cannot connect serial"

if __name__ == "__main__":
    main()