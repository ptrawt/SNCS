import socket
import serial
import sys
from time import sleep

READ_TIMEOUT = 8


def read_serial(console):

    data_bytes = console.inWaiting()
    if data_bytes:
        data_bytes = console.read(data_bytes)
        return data_bytes.decode()
    else:
        return "Not thing"


def send_command(console, cmd):

    if cmd != '':
        console.write(cmd.encode()+b"\n")
    else:
        console.write(b'\r')
    sleep(.2)
    return read_serial(console)


def cli_readline(sett):
    port = sett[0]
    cmd = sett[1]

    console = serial.Serial(port,
        timeout=READ_TIMEOUT,
        xonxoff=True,
        rtscts=True,
        dsrdtr=True
    )

    if not console.isOpen():
        sys.exit()

    if 'sh' in cmd or '?' in cmd:
        console.write(cmd.encode() + b"\n")
        data_out = ''
        while 1:
            bytes = console.readline()      #Read from Serial Port
            data =  bytes.decode('utf-8')
            if '#' in data:
                break
            elif '--More--' in data:
                console.write(b"          \n")
            else:
                data = data.split('\r\n')
                data_out += data[0]+'\n'

        return '1\n'+data_out

    else:
        return send_command(console, cmd)

    console.flushInput()
    console.close()


def connection():
    host = '' # Get local machine name
    port = 30003                # Reserve a port for your service.
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((host, port))    # Bind to the port
    except socket.error as e:
        raise e
        # connection()
    global c
    s.listen(5)                 # Now wait for client connection.
    c, addr = s.accept()        # Establish connection with client.

    print( "Start socket.....")
    print ('Got connection from', addr)

    return c


def config_get_result():
    c = connection()
    while True:
        try:
            data = c.recv(1024)
            print(data)
        except Exception as e:
            print (e)
            config_get_result()
        else:
            sett = data.decode().split(':')
            if sett[0] == 'end':
                print('Close connection')
                c.send(b'Connect close...')
                c.close()
                break
            else:
                data = cli_readline(sett)
                c.send(data.encode())
    config_get_result()


if __name__ == '__main__':
    config_get_result()
