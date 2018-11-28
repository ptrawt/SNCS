import serial
import sys
import time

READ_TIMEOUT = 8

def connection(port):

    console = serial.Serial(port,
        timeout=READ_TIMEOUT,
        xonxoff=True,
        rtscts=True,
        dsrdtr=True
    )

    if not console.isOpen():
        sys.exit()

    return console

def read_serial(console):

    data_bytes = console.inWaiting()
    if data_bytes:
        data = console.read(data_bytes)
#        print(data)
        return data.decode()
    else:
        return "Not thing"


def check_logged_in(console, console_pass, enable_pass):

    console.write(b"\r")
    while 1:
        time.sleep(1)
        prompt = read_serial(console)
        if 'Password' in prompt:
            if console_pass != '':
                console.write(console_pass.encode()+b'\n')
                print("Access to Privileged mode.")
        elif '>' in prompt:
            console.write(b'en\n')
            time.sleep(1)
            prompt = read_serial(console)
            if 'Password' in prompt:
                console.write(enable_pass.encode()+b'\n')
        elif '#' in prompt:
            print("Access to Enable mode.")
            if '(' in prompt or ')' in prompt:
                console.write(b"end\n")
            break

    return True


def send_command(console, txt):

    console.write(b"en\n")

    for line in txt:
        if '!' in line:
            pass
        else:
            console.write(line.encode()+b'\n')

    console.write(b'end\n')
    console.write(b"\r\n")

    print ("Configuration Successful")


def configuration(port, txt, console_pass, enable_pass):

    console = connection(port)
    if check_logged_in(console, console_pass, enable_pass):
        send_command(console, txt)
        console.flushInput()

    console.close()


def get_result(port, console_pass, enable_pass):
    console = connection(port)
    output = ''
    if check_logged_in(console, console_pass, enable_pass):
        console.write(b"\n")
        console.write(b"terminal len 0\n")
        console.write(b"en\n")
        console.write(b"sh run\n")
        while 1:
            bytes = console.readline()      #Read from Serial Port
            data =  bytes.decode('utf-8')
            if 'end\r\n' ==  data:
                break
            else:
                output += data+','

        console.flushInput()
        console.write(b"exit\n")

    console.close()
    return output

def main(sett):
    port = sett[1]
    console_pass = sett[2]
    enable_pass = sett[3]
    txt = sett[4].split(',')

    while 1:
        try:
            configuration(port, txt, console_pass, enable_pass)
            time.sleep(0.5)
            data = get_result(port, console_pass, enable_pass)
        except Exception as e:
            raise e
        else:
            return data
        break

if __name__ == "__main__":
    main(sett)
