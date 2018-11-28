import socket


def connection():
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)  # Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '192.168.1.100'  # Get local machine name
    port = 30002  # Reserve a port for your service.
    try:
        s.connect((host, port))    
    except Exception as e:
        print (e)
        connection()
    else:
        return s


def send_receive(inp):
    s = connection()
    command = inp
    s.send(command.encode())
    data_out = ''
    while True:
        reply = s.recv(2048)
        data = reply.decode()
        if 'Connect close...' == data:
            data_out += data
            break
            
        else:
            data_out += data
            s.send('end:'.encode())
            
    s.close()
    return data_out
        # Close the socket when done


# def main(inp):
#     return send_receive(inp)
    
if __name__ == '__main__':
    # inp = input()   # Input form 1:serial_port:command, 1 == config script function, 2 == CLI function
    # main(inp)
    send_receive(inp)