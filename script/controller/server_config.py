import socket
import config_script
import CLI_readline


def connection():
    host = '' # Get local machine name
    port = 30002                # Reserve a port for your service.
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((host, port))    # Bind to the port
    except socket.error as e:
        raise e
    global c
    s.listen(5)                 # Now wait for client connection.
    c, addr = s.accept()        # Establish connection with client.

    print( "Start socket.....")
    print('Got connection from', addr)

    return c


def config_get_result():
    c = connection()
    while True:
        data = c.recv(2048)
#        print(data)
        sett = data.decode().split(':')
        if sett[0] == 'end':
            print('Close connection')
            c.send(b'Connect close...')
            c.close()
            break
        else:
            if sett[0] == '1':
                data = config_script.main(sett)
                print(data)
                c.send(data.encode())

    config_get_result()


if __name__ == '__main__':
    config_get_result()