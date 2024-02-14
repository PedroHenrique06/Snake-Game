import random
import pygame
import tkinter as tk
from tkinter import messagebox
 
 # Classe que corresponde aos cubos que formam a "Cobra" e os "lanches"
class Cube(object):
    rows = 20
    w = 500
    
    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color 

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        
        # Desenha os olhos da cobra
        if eyes:
            centre = dis // 2 
            radius = 3 
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# Classe que representa a "Cobra" do jogo        
class Snake(object):
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        
    def move(self):
        
        for event in pygame.event.get():
            # Caso a aba seja fechada o programa encerra sem falhas
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            keys = pygame.key.get_pressed()
            
            # Capta as direções através do teclado
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            
            # Caso a cobra chegue a borda ela é transportada para a borda contraria
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirnx, c.dirny)
    
    # Reinicia a cobra para o menor tamanho possível
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        
    # Aumenta o tamanho da cobra
    def addCube(self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny
        
        # Verifica a direção da cobra
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))
            
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    # Desenha a cobra
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)  

# Desenha o campo de jogo
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    
    x = 0
    y = 0
    
    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn
        
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

# Atualiza o jogo constantemente
def redrawWindow(surface):
    global rows, width, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()
    
# Gera um lanche em um local aleatório do campo de jogo
def randomSnack(rows, snake):
    positions = snake.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # Verifica se a posição já está ocupada pela cobra
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return(x, y)
    
# Gera mensagem de encerramento
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main(): 
    global width, rows, snake, snack
    width = 500
    rows = 20
    
    window = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (10, 10))
    snack =  Cube(randomSnack(rows, snake), color=(0, 255, 0))
    flag = True
    
    clock = pygame.time.Clock() 
    while flag:
        pygame.time.delay(50)
        clock.tick(10)   
        snake.move()
        # Testa se a cabeça da cobra está na mesma posição que o lanche
        if snake.body[0].pos == snack.pos:
            snake.addCube()
            snack = Cube(randomSnack(rows, snake), color=(0, 255, 0))
        
        # Testa se a cobra colidiu consigo mesma
        for i in range(len(snake.body)):
            if snake.body[i].pos in list(map(lambda z:z.pos, snake.body[i+1:])):
                print('Score: ', len(snake.body))
                message_box('You Lost', 'Play Again...')
                snake.reset((10, 10))
                break 
            
        redrawWindow(window)

main()
