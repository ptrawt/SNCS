import serial
import sys
import socket
import time
import subprocess
import device_info
import tempDHT22

# Controller information function.

def init_socket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a UDP socket object
    host = '192.168.1.117'              # Get local machine name
    port = 30001                # Reserve a port for your service.
    s.connect((host, port))

    return s

def controller_info():

    testIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # setup UDP socket
    s.connect((testIP, 0))
    ipaddr = s.getsockname()[0]
    host = socket.gethostname()

    return "%s: %s" %(host, ipaddr)
#Function Ends Here

def get_serialPort_used():

    port_use = subprocess.check_output('dmesg | grep ttyUSB', shell=True)
    port_use = port_use.decode()
    port_use = port_use.split(' ')
    sett = set()
    for i in port_use:
        for j in i.split('\n'):
            if "ttyUSB" in j:
                if ":" in j:
                    pass
                else:
                    sett.add('/dev/'+j)

    return sett


def main():
    s = init_socket()
    con = controller_info()
    s.send('controller info:\n'.encode()+con.encode())
    print(get_serialPort_used())
    while 1:
        s.send('password\n'.encode())
        data = s.recv(1024)
        password = data.decode()
        temp = tempDHT22.main()
        cou = 0
        set_port = get_serialPort_used()
        lis_pass = []
        lis_all_pass = []
        name_port = []
        print(password)
        if password != 'no password':
            for line in password.split(':'):
                if line != '':
                    for var in line.split(','):
                        if var == '':
                            pass
                        else:
                            lis_pass.append(var)
                    lis_all_pass.append(lis_pass)
                    lis_pass = []
                else:
                    pass
            print(lis_all_pass)

            for i in lis_all_pass:
                name_port.append(i[0])

            for j in set_port:
                if j in name_port:
                    ser_temp = int(''.join([n for n in j if n.isdigit()]))
                    print(ser_temp)
                    s.send('device_info\n'.encode()+device_info.main(lis_all_pass[ser_temp]).encode())
                else:
                    set_pass = [j, '', '']
                    s.send('device_info\n'.encode()+device_info.main(set_pass).encode())
        else:
            for port in set_port:
                set_pass = [port, "", '']
                s.send('device_info\n'.encode()+device_info.main(set_pass).encode())
        time.sleep(60)

        while cou != 15:
            s.send('Sensor\n'.encode()+temp.encode()+con.encode())
            time.sleep(60)
            cou += 1


if __name__ == "__main__":
    main()
