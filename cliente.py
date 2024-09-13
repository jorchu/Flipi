import socket
import threading
import pickle
import time

def connect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        return sock
    
    except ConnectionRefusedError:
        print("Wrong data server.")



def reciv_data(sock):
    try:
        data = sock.recv(20000)
        data = pickle.loads(data)
        #print(data)
        return data        
    except:

        return None


def send_data(sock, data):
    try:
        dato = pickle.dumps(data)
        sock.sendall(dato)
        #print(len(dato))
    except Exception as e:
        print(e)
    
def main():

    sock = connect("127.0.0.1", 8000)

    send_data(sock, input("KK"))
    
    while True:
        print(reciv_data(sock))
        


if __name__ == "__main__":
    main()
    
    

