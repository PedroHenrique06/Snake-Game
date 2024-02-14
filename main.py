import pygame
import random
from cube import Cube
from snake import Snake
import tkinter as tk
from tkinter import messagebox

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