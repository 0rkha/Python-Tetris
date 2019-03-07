import pygame
import pygame
import random
import numpy as np

class game:
    def __init__(self):
        self.w             = 1500
        self.h             = 900
        self.WHITE         = (0,0,0)
        self.time          = 0
        self.pygame_init()
        self.block         = block()
        self.blockset      = block_set()
    
    def pygame_init(self):
        # config
        pygame.init()
        pygame.display.set_caption('Unifox-Tetris')
        # image config
        self.pad           = pygame.display.set_mode((self.w, self.h))
        self.clock         = pygame.time.Clock() 
        self.bg            = pygame.image.load('image/bg.png')
        self.pad.fill(self.WHITE)
        
        self.page = 0
    
    def draw_bg(self,x,y):
        self.pad.blit(self.bg, (x, y))


    def system(self):
        gamedone = False
        systemdone = False
        while not systemdone:
            while self.page == 0:
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT: # If user clicked close
                        gamedone=True # Flag that we are done so we exit this loop
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.page=1
                self.render()
           
            while self.page==1 and not gamedone:
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT: # If user clicked close
                        gamedone=True # Flag that we are done so we exit this loop
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.block.rotate+=1
                        if event.key == pygame.K_d:
                            self.block.rotate-=1
                        if event.key == pygame.K_LEFT:
                            if self.block.left() and self.block.block_collision_left(self.blockset):
                                self.block.x-=1
                        if event.key == pygame.K_RIGHT:
                            if self.block.right() and self.block.block_collision_right(self.blockset):
                                self.block.x+=1
                        # if event.key == pygame.K_DOWN:
                        #     self.block.y+=1
                self.render()
                self.next()

            while self.page==2:
                pass
    
    def next(self):
        if self.time % self.block.level == self.block.level-1:
            if self.block.collision() or self.block.block_collision_down(self.blockset):
                self.blockset.merge(self.block)
                self.block.init_variable()
            else:
                self.block.y+=1
        self.time+=1

    def render(self):
        if self.page == 0:
            pass
        
        elif self.page == 1:
            self.pad.fill(self.WHITE)
            self.block.draw_block_shape(self.pad)
            
        else:
            pass
        pygame.display.update()
            
             
class block_set:
    def __init__(self):
        self.map = np.zeros((7,6))

    def merge(self,block):
        tel = int(block.bag[(block.step)%21])
        ac  = block.rotate%4
        length = len(block.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if block.telomino[tel][ac][i][j] == 1:
                    if block.y+i < block.max_height and block.x+j < block.max_width and block.y+i >=0 and block.x+j >=0:
                        self.map[block.y+i][block.x+j] = 1
                        
class block:
    def __init__(self):
        self.telomino =[
            [
             [[0,0,0],
             [1,1,1],
             [0,1,0]],

             [[0,1,0],
             [1,1,0],
             [0,1,0]],
             
             [[0,1,0],
             [1,1,1],
             [0,0,0]],
             
             [[0,1,0],
             [0,1,1],
             [0,1,0]]
            ],
            [
             [[0,0,0],
             [1,1,0],
             [0,1,1]],

             [[0,1,0],
             [1,1,0],
             [1,0,0]],
             
             [[1,1,0],
             [0,1,1],
             [0,0,0]],

             [[0,0,1],
             [0,1,1],
             [0,1,0]]
            ],

            [
             [[0,0,0],
             [0,1,1],
             [1,1,0]],

            [[1,0,0],
             [1,1,0],
             [0,1,0]],

            [[0,1,1],
             [1,1,0],
             [0,0,0]],

            [[0,1,0],
             [0,1,1],
             [0,0,1]]
            ],
            [
             [[0,1,0],
             [0,1,0],
             [0,1,1]],

             [[0,0,0],
             [1,1,1],
             [1,0,0]],

             [[1,1,0],
             [0,1,0],
             [0,1,0]],

             [[0,0,1],
             [1,1,1],
             [0,0,0]],
             ],
             [
            [[0,1,0],
             [0,1,0],
             [1,1,0]],
             
            [[1,0,0],
             [1,1,1],
             [0,0,0]],

            [[0,1,1],
             [0,1,0],
             [0,1,0]],

            [[0,0,0],
             [1,1,1],
             [0,0,1]],
             ],
            [
            [[1,1,],
             [1,1,]],
            [[1,1,],
             [1,1,]],
            [[1,1,],
             [1,1,]],
             [[1,1,],
             [1,1,]],
          ],
          [
            [[0,1,0,0],
             [0,1,0,0],
             [0,1,0,0],
             [0,1,0,0]],

            [[0,0,0,0],
             [1,1,1,1],
             [0,0,0,0],
             [0,0,0,0]],

            [[0,0,1,0],
             [0,0,1,0],
             [0,0,1,0],
             [0,0,1,0]],

            [[0,0,0,0],
             [0,0,0,0],
             [1,1,1,1],
             [0,0,0,0]]
          ]
        ]
        self.rotate= 0
        self.x    = 0
        self.y    = 0
        self.maptop_x      = 10
        self.maptop_y      = 10
        self.max_height    = 7
        self.max_width     = 6
        self.min_width     = 0
        self.n    = 0
        self.level = 200
        self.step = 0
        self.bag = []
        self._set_bag()
        
        self.I_block       = pygame.image.load('image/I_block.png')
        self.J_block       = pygame.image.load('image/J_block.png')
        self.L_block       = pygame.image.load('image/L_block.png')
        self.O_block       = pygame.image.load('image/O_block.png')
        self.S_block       = pygame.image.load('image/S_block.png')
        self.T_block       = pygame.image.load('image/T_block.png')
        self.Z_block       = pygame.image.load('image/Z_block.png')

    def _set_bag(self):
        bag_order = np.arange(0,7)
        for i in range(3):
            np.random.shuffle(bag_order)
            self.bag = np.append(self.bag, bag_order)
        
    def collision(self):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j] == 1:
                    if self.y + j + 1 == self.max_height:
                        return True
        return False        
    
    def draw_block(self,pad,num,x,y):
        if num == 0:
            pad.blit(self.I_block,(x,y))
        if num == 1:
            pad.blit(self.J_block,(x,y))
        if num == 2:
            pad.blit(self.L_block,(x,y))
        if num == 3:
            pad.blit(self.O_block,(x,y))
        if num == 4:
            pad.blit(self.S_block,(x,y))
        if num == 5:
            pad.blit(self.T_block,(x,y))
        if num == 6:
            pad.blit(self.Z_block,(x,y))
            
    def init_variable(self):
        self.x=0
        self.y=0
        self.step+=1
    
    def draw_block_shape(self,pad):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j] == 1:
                    self.draw_block(pad,tel,self.maptop_x+(self.x+i)*100, self.maptop_y+(self.y+j)*100)
    def right(self):
        max_w = 0
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j]==1:
                    max_w = max(max_w, j)
        if max_w == self.max_width - 1:
            return False
        else:
            return True 
            
    def left(self):
        min_w = 5
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j]==1:
                    min_w=min(min_w,j)
        if min_w == self.min_width:
            return False
        else:
            return True 

    def block_collision_right(self, blockset):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.y+i < self.max_height and self.x+j+1 < self.max_width and self.y+i>= 0 and self.x+j+1 >=0:
                    if self.telomino[tel][ac][i][j] == 1 and blockset.map[self.y+i][self.x+1+j] == 1:
                        return False
        return True

    def block_collision_left(self, blockset):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.x+j-1 < self.max_width and self.y+i < self.max_height and self.x+j-1 >= 0 and self.y+i >=0 :
                    if self.telomino[tel][ac][i][j] == 1 and blockset.map[self.y+i][self.x-1+j] == 1:
                        return False
        return True

    def block_collision_down(self, blockset):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.x+j < self.max_width and self.y+1+i < self.max_height and self.x+j >= 0 and self.y+1+i >= 0:
                    if self.telomino[tel][ac][i][j] == 1 and blockset.map[self.y+1+i][self.x+j] == 1:
                        return True
        return False

if __name__ == "__main__":
    env = game()
    env.system()
