import pygame as pg
import numpy as np
import sys
import time
import cliente
import random

ID_PLAYER = 2
ID_PROYECTIL = 1
ID_ENTORNO = 0

WHITE = (255,255,255)
BLACK = (0,0,0)
GREN = (0, 255, 0)
RED = (255, 0, 0)

UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1
STATE = 0







class Objeto:
    pass

class Personaje:
    def __init__(self, mapa, pos, color, type, size, idf=0):
        self.pos = pos #fila-columna
        self.color = color
        self.last_mov = [0,0]
        self.type = type
        self.live = 3
        self.mapa = mapa
        self.id = idf if idf else random.randint(0, 1000000)
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
        
    def get_damage(self, personajes):
        self.life -= 1
        if self.life == 0:
            print("MUERTO")
    
class Proyectil:
    def __init__(self, pos, direction, mapa, dad_id, size, fase, idk=0):
        self.pos = pos
        self.direction = direction
        self.type = ID_PROYECTIL
        self.time_last_mov = time.time()
        self.mapa = mapa
        self.colide = False
        self.objetct_colide = None
        self.id = idk if idk else random.randint(0, 1000000)
        self.mapa[pos[0]][pos[1]] = self.id
        self.dad_id = dad_id
        self.color = GREN
        self.size = size
        self.mov = False
        self.fase = fase
        
    def draw(self, screen):
            x = self.pos[1] * 20
            y = self.pos[0] * 20
            width = self.size
            height = self.size
            pg.draw.rect(screen, self.color, (x, y, width, height))
            
    def movment(self, limit_x, limit_y, proyectiles, personajes):
        self.mapa[self.pos[0]][self.pos[1]] = 0
        self.mov = not self.fase
        if self.pos[1] + self.direction[1] in limit_x and self.pos[0] + self.direction[0] in limit_y:
            if self.direction[0] == UP:
                self.pos[0] -= 1
            elif self.direction[0] == DOWN:
                self.pos[0] += 1
            if self.direction[1] == LEFT:
                self.pos[1] -= 1
            elif self.direction[1] == RIGHT:
                self.pos[1] += 1

        else:
            
            if not (self.pos[1] + self.direction[1] in limit_x):
                self.direction[1] *= -1
            if not (self.pos[0] + self.direction[0] in limit_y):
                self.direction[0] *= -1
                
            if self.direction[0] == DOWN:
                self.pos[0] += 1
            elif self.direction[0] == UP:
                self.pos[0] -= 1
            if self.direction[1] == LEFT:
                self.pos[1] -= 1
            elif self.direction[1] == RIGHT:
                self.pos[1] += 1
                
        after_value = self.mapa[self.pos[0]][self.pos[1]]

        if after_value in proyectiles:
            #print(proyectiles[after_value].mov)
            return [self.id, proyectiles[after_value].id]
        
        elif after_value in personajes:
            personajes[after_value].get_damage()
            return [self.id]
        else:
            self.mapa[self.pos[0]][self.pos[1]] = self.id
            return []
         
        self.mov = self.fase
        self.fase = not self.fase
        
    def destroy(self):
        self.mapa[self.pos[0]][self.pos[1]] = 0


class Screen:
    def __init__(self, width, height) -> None:
        pg.init()

        self.map_width = width
        self.map_height = height

        self.map_rows = self.map_height // 20
        self.map_columns = self.map_width // 20
        
        self.limits_x = range(0, self.map_columns)
        self.limits_y = range(0, self.map_rows)    
        
        self.cuadricula = np.zeros((self.map_rows, self.map_columns))
        self.personajes = {}
        self.proyectiles = {}
        self.objects = [self.personajes, self.proyectiles]
        
        self.screen = pg.display.set_mode((self.map_width, self.map_height))
        pg.display.set_caption("FLIPI")
    
    def draw_all(self):
        self.screen.fill(BLACK)
        for elemento in self.objects:
            elemento.draw()
        pg.display.flip()
  
  
            
class Button:
    def __init__(self, width, height, screen, color_button, color_text, text, num_buttons, id_button):
        self.width = width
        self.height = height
        self.screen = screen
        self.color_button = color_button
        self.font = pg.font.SysFont('Arial', 30)
        self.render_text = self.font.render(text, 0, color_text)
        self.num_buttons = num_buttons
        self.id = id_button

    def draw_button(self, centredo, padding):
        if centredo:
            self.x = (self.screen.map_width - self.width) // 2
            self.y = ((self.height + padding) * self.num_buttons - padding) // self.screen.map_height + self.id * (self.height + padding)
            pg.draw.rect(self.screen.screen, self.color_button, (self.x, self.y, self.width, self.height))
            self.screen.screen.blit(self.render_text, (self.x+60, self.y+30))


def detectar_acciones():
    pass

def main_menu(screen, sock, personajes, local_player, mapa):
    button = Button(300, 100, screen, WHITE, BLACK, "START", 1, 2)
    screen.screen.fill(BLACK)
    button.draw_button(True, 50)
    pg.display.flip()
    
    while True:
        data = cliente.reciv_data(sock)
        if data:
            if data[0]:
                print(data)
                personaje = Personaje(mapa, data[0][1], RED, ID_PLAYER, 20, data[0][2])
                personajes[personaje.id] = personaje
                
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                sys.exit(0)
                
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if click[0] and pos[0] in range(button.x, button.x + button.width) and pos[1] in range(button.y, button.y + button.height):
            cliente.send_data(sock, [(ID_PLAYER, local_player.pos, local_player.id), 0])
            break

    
def game(screen, socket, limits_x, limits_y, local_player, jugadores, mapa):
    
    #local_player = Personaje(mapa, [random.randint(0, 15), random.randint(0,15)], WHITE, 2, 20)
    

    
    personajes = jugadores
    proyectiles = {}
    
    objetos = [personajes, proyectiles]
    
    personajes[local_player.id] = local_player
    
    instant_time = 0
    last_move_time = 0
    last_click_time = 0
    
    del_list = set()
    fase = True
    while True:
        new_proyectiles = 0
        info = 0
        data = cliente.reciv_data(socket)
        #print(data)
        if data:
            if data [0]:
                if data[0][0] == ID_PLAYER:
                    personaje = Personaje(mapa, data[0][1], RED, ID_PLAYER, 20, data[0][2])
                    personajes[personaje.id] = personaje
                    
                elif data[0][0] == ID_PROYECTIL:
                    proyectil = Proyectil(data[0][1], data[0][2], mapa, data[0][3], 20, False, data[0][4])
                    proyectiles[proyectil.id] = proyectil
                    
                    
            if data[1]:
                personajes[data[1][0]].movment(data[1][1], limits_x, limits_y, proyectiles, personajes)
                    
        screen.fill(BLACK)

        for objeto in objetos:
            for elemetnto in  objeto.values():
                elemetnto.draw(screen)
        
        instant_time = time.time()
        
        for event in pg.event.get():
            if pg.QUIT == event.type:
                pg.quit()
                sys.exit(0)
            
        teclas = pg.key.get_pressed()
        
        if instant_time - last_click_time > 0.5:  # Botón izquierdo
            direct = [0,0]
            if teclas[pg.K_UP]:
                direct[0] = UP
            elif teclas[pg.K_DOWN]:
                direct[0] = DOWN
            if teclas[pg.K_LEFT]:
                direct[1] = LEFT
            elif teclas[pg.K_RIGHT]:
                direct[1] = RIGHT
            if direct != [0, 0]:
                local_player.last_mov = direct.copy()
                proyectil = local_player.attack(Proyectil, fase)
                new_proyectiles = (ID_PROYECTIL, proyectil.pos, proyectil.direction, proyectil.dad_id, proyectil.id)
                proyectiles[proyectil.id] = proyectil
                last_click_time = instant_time
            
        if instant_time - last_move_time > 0.1:
            direct = [0,0]
            if teclas[pg.K_w]:
                direct[0] = UP
            elif teclas[pg.K_s]:
                direct[0] = DOWN
            if teclas[pg.K_a]:
                direct[1] = LEFT
            elif teclas[pg.K_d]:
                direct[1] = RIGHT
            if direct != [0,0]:
                del_list.update(local_player.movment(direct.copy(), limits_x, limits_y, proyectiles, personajes))
                last_move_time = instant_time
                info = (local_player.id, direct.copy())
                
                
        for proyectil in proyectiles.values():
            if instant_time - proyectil.time_last_mov > 0.5:
                eliminar = proyectil.movment(limits_x, limits_y, proyectiles, personajes)
                proyectil.time_last_mov = instant_time
                try:
                    del_list.update(eliminar)
                except:
                    pass
        fase = not fase

        #change_map(mapa, elementos)


        for element in del_list:
            #print(del_list)
            del proyectiles[element]
        
        #print(local_player.id, local_player.pos)
        if info or new_proyectiles:
            cliente.send_data(socket, [new_proyectiles, info])
        

        del_list.clear() 

        pg.display.flip()
        
def main():
    screen = Screen(1200, 700)
    socket = cliente.connect("127.0.0.1", 8000)
    local_player = Personaje(screen.cuadricula, [random.randint(0, 15), random.randint(0,15)], WHITE, 2, 20)
    screen.personajes[local_player.id] = local_player
    socket.setblocking(False)
    
    main_menu(screen, socket, screen.personajes, local_player, screen.cuadricula)
    game(screen.screen, socket, screen.limits_x,screen.limits_y, local_player, screen.personajes, screen.cuadricula)




if __name__ == "__main__":
    main()

"""                if colide:
                    if colide in personajes:
                        personajes[colide].get_damage()
                        proyectil.destroy()
                        del_list.append(proyectil.id)
                    elif colide in proyectiles:
                        if proyectiles[colide].direction[0] == proyectil.direction[0] * -1 and proyectiles[colide].direction[1] == proyectil.direction[1] * -1:
                            proyectiles[colide].destroy()
                            proyectil.destroy()
                            del_list.append(proyectil.id)
                            del_list.append(colide)
"""