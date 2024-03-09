from pygame import *
from math import *
import pygame_shaders

#Se importan las clases y demás
from GameEntities import Player, Enemies

#Se inicia el programa
init()

#Configuración de la pantalla
resolucion = (1920, 1080)


screen = display.set_mode(resolucion, OPENGL | FULLSCREEN)
screen_size = screen.get_size()
display = Surface(screen_size)
screen_shader = pygame_shaders.Shader(screen_size, screen_size, (0, 0), )

clock = time.Clock()
#----------------------------

#Colores
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
DARK_BLUE = (0, 1, 35, 14)
#----------------------------

#Variables
player_sprite = "Assets/tiny_ship14.png"
bullet_sprites = "Assets/laser_beam.png"
#----------------------------

#Objetos
All_sprite_in_game = sprite.Group()
player = Player(player_sprite, bullet_sprites, 500, 500, 40, 40, 10)
enemie = Enemies("Assets/circular_enemy.png", bullet_sprites, 300, 300, 40, 40, 10, "enemigo_patron_circular")
#----------------------------

#Logica de los niveles o pantallas
running = True
#----------------------------

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        #Para que funcione el disparo
        player.Shoot(e, All_sprite_in_game)

    screen.fill(DARK_BLUE)

    #Logica principal del juego

    screen_rect = display.get_surface().get_rect()

    #Posicion del mouse
    mouse_pos = mouse.get_pos()

<<<<<<< HEAD
        #Logica de las colisiones
        #Colisiones de los enemigos con las balas
    bullets_to_enemies = sprite.groupcollide(enemies, bullets, False, False)

    for enemy, bullet in bullets_to_enemies.items():
        for b in bullet:
            if b.bullet_target == "enemies":
                enemy.take_damage(1)
                b.kill()

        #Update de los objetos de la escena
=======
>>>>>>> parent of 132c137 (Se agrega mecánica de matar a los enemigos y se optimiza el disparo)
    player.update(player_sprite, mouse_pos, screen_size)
    enemie.update(All_sprite_in_game)
    screen.blit(player.image, player.rect)
    screen.blit(enemie.image, enemie.rect)
    All_sprite_in_game.update(screen_rect)
    #-----------------

    #Configuración de la pantalla (In-Game)
    All_sprite_in_game.draw(screen)
    display.flip()
    #Control de los fps o cuadros por segundo
    clock.tick(60)
    #-----------------

quit()