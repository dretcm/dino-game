import pygame, sys, random
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
WINDOW_SIZE = (600,300)
screen = pygame.display.set_mode(WINDOW_SIZE)


class Player:
        subida = 10
        bajada = 5
        gravedad = 0.5     

        limite = 150
        altura = limite

        floor = True
        font = pygame.font.Font(None,30)
        recorrido = 0
        
        def __init__(self,window_size):
                self.window_size = window_size
                self.x, self.y = window_size[0]//2 - 200, window_size[1]//2 -20
                self.collider = pygame.Rect(self.x,self.y,40,40)
                self.img = pygame.transform.scale(pygame.image.load('player.png'), (40, 40))
        
        def down_key(self,key):
                if key == K_UP and not self.floor:
                        self.altura = 0
                        self.bajada = 5
                        self.floor = True
                        
        def moving_player(self, screen):
                if self.floor:
                        if self.altura < self.limite:
                                self.collider.y -= self.subida
                                self.altura += self.subida
                        else:
                                self.bajada += self.gravedad 
                                self.collider.y += self.bajada

                        if self.window_size[1] - 20 < self.collider.y + 35:
                                self.collider.y = self.window_size[1] - 59

                self.recorrido += 1

                screen.blit(self.img, self.get_pos())

                message = self.font.render('metros: '+ str(self.recorrido), 1, (0, 0, 0))
                screen.blit(message, (self.window_size[0]-150, 10))
                
        def get_collider(self):
                return self.collider
        
        def get_pos(self):
                return (self.collider.x, self.collider.y)


class Obstaculos:
        t = 0
        limit = 20
        ago = 20
        times = [30, 40, 50, 60]
        speed = 10
        def __init__(self, window_size):
                self.window_size = window_size
                self.obs = []
        def update_obstaculos(self,screen, player): 
                aux = []
                for i in self.obs:
                        pygame.draw.rect(screen, (0,255,0), i)
                        i.x -= self.speed
                        if i.colliderect(player.get_collider()):
                                print('F')
                        if i.x > 0:
                                aux.append(i)
                                
                self.obs = aux.copy()
                
                if self.t < self.limit:
                        self.t += 1
                else:
                        obstaculo = pygame.Rect(WINDOW_SIZE[0] + 100,WINDOW_SIZE[1]-60,10,40)
                        self.obs.append(obstaculo)
                        self.t = 0
                        self.speed += 0.2
                        self.ago = self.limit
                        self.limit = random.choice(self.times)
                        while self.limit == self.ago:
                                self.limit = random.choice(self.times)
                
player = Player(WINDOW_SIZE)
obstaculos = Obstaculos(WINDOW_SIZE)

floor = pygame.Rect(0,WINDOW_SIZE[1]-20,WINDOW_SIZE[0],50)

color = 255
cambio = 500
op = True
while True:
        for event in pygame.event.get():
                if event.type == QUIT:
                        pygame.quit() 
                        sys.exit()
                if event.type == KEYDOWN:
                        player.down_key(event.key)
                        

        if player.recorrido < cambio:
                if op:
                        if color < 255:
                                color += 1
                else:
                        if color > 127:
                                color -= 1                       
        else:
                cambio += 500
                op = not op

                        
        screen.fill((color,color,color))

        player.moving_player(screen)

        pygame.draw.rect(screen, (255,128,0), floor)
        
        if player.get_collider().colliderect(floor):
                player.floor = False

        obstaculos.update_obstaculos(screen, player)
        
        pygame.display.update()
        clock.tick(30)
