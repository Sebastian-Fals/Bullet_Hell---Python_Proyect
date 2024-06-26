import time as tm
import threading as th
from pygame import *
from random import *
from Assets.Python.GameEntities import Enemies
from Assets.Python.funciones import tamanoDinamico

class SpawnPoint():
    def __init__(self, position):
        self.position = position
        self.canSpawn = True

    def update(self, group):
        # Por defecto, permitir el spawn si el grupo está vacío
        self.canSpawn = True if not group.sprites() else False

        # Verificar si algún sprite en el grupo ocupa la misma posición
        for enemy in group:
            if enemy.final_position == self.position:
                self.canSpawn = False
                break  # Si encontramos un sprite en la misma posición, no necesitamos continuar verificando
            else:
                self.canSpawn = True
        

class EnemyGenerator():
    def __init__(self, path: str, group,  spawnPoints, enemyCount, enemy_IDs, bulletSprite, difficulty, screen, screenSize):
        self.path: str = path
        self.screen = screen
        self.screenSize = screenSize
        self.spawnPoints = spawnPoints
        self.enemyCount = enemyCount
        self.enemy_IDs = enemy_IDs
        self.bulletSprite = bulletSprite
        self.group = group
        self.difficulty = difficulty
        self.lock = th.Lock()
        self.enemies_generated = 0  # Contador de enemigos generados
        self.actualwave = 1 #Control de la oleada actual
        self.waveInText = 1
        self.waveFont = font.Font(self.path + "Fonts/Minecraft.ttf", int(tamanoDinamico(self.screenSize[1], 10)))
        self.waveText = self.waveFont.render("Wave " + str(self.waveInText), True, (255, 255, 255, 255))
        self.any_spawn_points_occupied = 0
        self.enmeyLife = 5

    def update(self, screen_size):
        self.any_spawn_points_occupied = all(spawn_point.canSpawn for spawn_point in self.spawnPoints)
        if self.any_spawn_points_occupied:
            self.waveText = self.waveFont.render("Wave " + str(self.waveInText), False, (255, 255, 255, 255))
            self.screen.blit(self.waveText, self.waveText.get_rect(center = ((tamanoDinamico(self.screenSize[0], 50), tamanoDinamico(self.screenSize[1], 50)))))
            self.setDifficulty()
            self.enemies_generated = 0
            # Utilizar threading para generar enemigos sin bloquear el hilo principal
            enemy_thread = th.Thread(target=self.generateEnemies, args=(screen_size, ))
            enemy_thread.daemon = True
            enemy_thread.start()

    def generateEnemies(self, screen_size):
        with self.lock:
            if self.any_spawn_points_occupied:
                self.actualwave += 1
                tm.sleep(2)
                while self.enemies_generated < self.enemyCount:
                    for position in self.spawnPoints:
                        position.update(self.group)
                    # Verifica si todos los spawnPoints están ocupados
                    all_spawn_points_occupied = all(not spawn_point.canSpawn for spawn_point in self.spawnPoints)
                    if all_spawn_points_occupied:
                        return
                    initialPositions = [(0,0), (0, screen_size[1]), (screen_size[0], 0), screen_size]
                    randomInitialPositions = randint(0, len(initialPositions) - 1)
                    randomPosition = randint(0, (len(self.spawnPoints) - 1))
                    randomID = randint(0, (len(self.enemy_IDs) - 1))
                    while self.spawnPoints[randomPosition].canSpawn == False:
                        randomPosition = randint(0, (len(self.spawnPoints) - 1))
                    if self.spawnPoints[randomPosition].canSpawn == True:
                        self.group.add(Enemies(self.path, image.load(self.path + "Images/circular_enemy.png").convert_alpha(), self.bulletSprite, initialPositions[randomInitialPositions], (40, 40), self.enmeyLife, self.screenSize, self.enemy_IDs[randomID], self.spawnPoints[randomPosition].position))
                    tm.sleep(0.5)
                    self.enemies_generated += 1
                    self.waveInText = self.actualwave
                for enemy in self.group:
                        enemy.canShoot = True                   

    def setDifficulty(self):
        if self.difficulty == "easy":
            self.enemyCount = randint(int(1 + (self.actualwave * 0.2)), int(3 + (self.actualwave * 0.2)))
            self.enmeyLife = 5
        if self.difficulty == "medium":
            self.enemyCount = randint(int(2 + (self.actualwave * 0.2)), int(5 + (self.actualwave * 0.2)))
            self.enmeyLife = 10
        if self.difficulty == "hard":
            self.enemyCount = randint(int(4 + (self.actualwave * 0.2)), int(8 + (self.actualwave * 0.2)))
            self.enmeyLife = 15