from pygame import *
from math import * 

#Se inicia el programa
init()

#Configuración de la pantalla
screen = display.set_mode((1920, 1080), FULLSCREEN)
clock = time.Clock()
screen_size = screen.get_size()
#----------------------------

#Colores
DARK_BLUE = (0, 1, 35, 14)
BLUISH_GREY = (86, 100, 135, 53)
#----------------------------

#Funciones

#----------------------------

#Clases
class GameEntity(sprite.Sprite):
    def __init__(self, sprite, posX, posY, sizeX, sizeY, vida):
        super().__init__()
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.scale(self.image, (sizeX, sizeY))
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)
        self.vida = vida

class Player(GameEntity):
    def __init__(self, sprite, posX, posY, sizeX, sizeY, vida):
        super().__init__(sprite, posX, posY, sizeX, sizeY, vida)
        self.velocityX = 0
        self.velocityY = 0

    def update(self, sprite, sizeX, sizeY):
        self.velocityX = 0
        self.velocityY = 0

        teclas = key.get_pressed()

        #Movimiento con WASD
        if teclas[K_w]:
            self.velocityY = -25
        if teclas[K_s]:
            self.velocityY = 25
        if teclas[K_a]:
            self.velocityX = -25
        if teclas[K_d]:
            self.velocityX = 25

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        #Rotacion del personaje hacia el mouse
        mouse_pos = mouse.get_pos()
        angle = degrees(atan2((mouse_pos[1] - self.rect.centery), (mouse_pos[0] - self.rect.centerx))) + 90
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        print(angle)

        #Distancia en x
        #mouse_pos[0] - self.rect.centerx 

        #Distancia en y
        #mouse_pos[1] - self.rect.centery

        #Distancia total
        #sqrt(((mouse_pos[0] - self.rect.centerx) ** 2) + ((mouse_pos[1] - self.rect.centery) ** 2))

        #Angulo entre el player, y el mouse
        #degrees(atan2((mouse_pos[1] - self.rect.centery), (mouse_pos[0] - self.rect.centerx)))


        #Limites en la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_size[1]:
            self.rect.bottom = screen_size[1]
#----------------------------

#Variables
player_sprite = "Assets/tiny_ship14.png"
#----------------------------

#Objetos
All_sprite_in_game = sprite.Group()
player = Player(player_sprite, 500, 500, 40, 40, 10)
All_sprite_in_game.add(player)
#----------------------------

#Logica de los niveles o pantallas
running = True
#----------------------------

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill(DARK_BLUE)

    #Logica principal del juego
    player.update(player_sprite, 40, 40)
    #-----------------

    #Configuración de la pantalla (In-Game)
    All_sprite_in_game.draw(screen)
    display.flip()
        #Control de los fps o cuadros por segundo
    clock.tick(60)
    #-----------------

quit()