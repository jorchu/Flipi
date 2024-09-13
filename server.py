import socket
import pickle
import asyncio
import time
import pygame as pg

ID_PLAYER = 2
ID_PROYECTIL = 1
ID_ENTORNO = 0

WHITE = (255,255,255)
BLACK = (0,0,0)
GREN = (0, 255, 0)

UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1
STATE = 0

class Personaje:
    def __init__(self, mapa, pos, color, type, size):
        self.pos = pos #fila-columna
        self.color = color
        self.last_mov = [0,0]
        self.type = type
        self.live = 3
        self.mapa = mapa
        self.id = id(self)
        self.mapa[pos[0]][pos[1]] = self.id
        self.proyectiles = {}
        self.life = 3
        self.size = size
        
    def draw(self, screen):
            x = self.pos[1] * 20
            y = self.pos[0] * 20
            width = self.size
            height = self.size
            pg.draw.rect(screen, self.color, (x, y, width, height))
            
    def movment(self, direction, limit_x, limit_y, proyectiles, personajes):
        self.mapa[self.pos[0]][self.pos[1]] = 0
        before_post = self.pos.copy()

        if self.pos[1] + direction[1] in limit_x:
            if direction[1] == LEFT:
                self.pos[1] -= 1
            elif direction[1] == RIGHT:
                self.pos[1] += 1
                
        if self.pos[0] + direction[0] in limit_y:
            if direction[0] == UP:
                self.pos[0] -= 1
            elif direction[0] == DOWN:
                self.pos[0] += 1
                #### TEST ####
        if self.mapa[self.pos[0]][self.pos[1]] in personajes:
            self.pos = before_post
            
        value = self.mapa[self.pos[0]][self.pos[1]]
        self.mapa[self.pos[0]][self.pos[1]] = self.id
        
        if value in proyectiles:
            self.get_damage()
            return [proyectiles[value].id]
        return []
    
    def attack(self, Proyectil, fase):
        proyectil_pos = [self.pos[0]+self.last_mov[0], self.pos[1]+self.last_mov[1]]
        proyectil = Proyectil(proyectil_pos, self.last_mov.copy(), self.mapa, self.id, 20, fase)
        return proyectil
        
    def get_damage(self):
        self.life -= 1
        if self.life == 0:
            print("MUERTO")
  

def manejar_cliente(cliente_socket, direccion):
    print(f"Conexión aceptada de {direccion}")
    while True:
        try:
            mensaje = cliente_socket.recv(1024)  # Recibe el mensaje del cliente
            if not mensaje:
                break  # Si el cliente cierra la conexión, se rompe el bucle
            print(f"Mensaje recibido de {direccion}: {mensaje.decode()}")
            cliente_socket.sendall(b"Mensaje recibido")
        except ConnectionResetError:
            break  # Si el cliente cierra abruptamente la conexión, salimos
    print(f"Cliente {direccion} desconectado")
    cliente_socket.close()

def recibir_datos(clientes, sock):
    while True:
        clientes[sock] = sock.recv(1024)
        print(pickle.loads(clientes[sock]))


class Cliente:
    def __init__(self, sock) -> None:
        self.sock = sock
    
    def recib_data(self):
        while True:
            pass
    
    def send_data(self):
        pass
    
async def recibir_conexion(servidor, clientes):
    cliente_socket, direccion_cliente = servidor.accept()
    clientes[cliente_socket] = 0

async def recib_data(clientes, sock):
    clientes[sock] = sock.recv(1024)
    print(pickle.loads(clientes[sock]))
    
async def send_data(clientes):
    
    for element in clientes:
        if clientes[element]:
            for cliente in clientes:
                if cliente != element:
                    cliente.sendall(clientes[element])
            clientes[element] = 0
            
def main():

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.bind(('localhost', 8000))
    servidor.listen(5)
    servidor.setblocking(False)
    last_client = 0
    clientes = {}
    print("Servidor esperando conexiones...")

    while True:

        try:
            cliente_socket, direccion_cliente = servidor.accept()
            clientes[cliente_socket] = 0
            print(direccion_cliente)
            #print("Conexión de:", direccion_cliente[0], direccion_cliente[1])
            
        except:
            pass
        
        
        for cliente in clientes:
            try:
                data = cliente.recv(20000)
                clientes[cliente] = data
                #print(pickle.loads(data))
                
                #clientes[cliente]
            except:
                pass
    
        for element in clientes:
            if clientes[element]:
                for cliente in clientes:
                    if cliente != element:
                        try:
                            cliente.sendall(clientes[element])
                            #time.sleep(0.1)
                        except:
                            pass
                clientes[element] = 0
                

if __name__ == "__main__":
    main()