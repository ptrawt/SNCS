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


def main(sett):
    port = sett[1]
    cmd = sett[2]

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
                console.write(b"       \n")
            else:
                data = data.split('\r\n')
                data_out += data[0]+'\n'

        return data_out

    else:
        return send_command(console, cmd)

    console.flushInput()
    console.close()

if __name__ == "__main__":

    main(sett)
