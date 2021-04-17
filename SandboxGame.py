import pygame
import random
import time
import sys

from Particle import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

GAME_SPEED = 144

PARTICLE_SIZE = 4

current_time = pygame.time.get_ticks()

def main(w, h):
    pygame.init()

    holding_mouse = False
    sParticle = "Sand"
    
    #FPS stuff
    font = pygame.font.SysFont("Arial", 30)
    #

    #/timers
    timers = {
        "Sand": [0,2],
        "Dirt": [0,4],
        "Snowflake": [0,16],
        "Smoke": [0,8]
    }

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    #Initialize grid with black pixels
    screen, tiles = Reset(screen)

    while True:
        #Adding game loop structure for organization
        #input
        screen, holding_mouse, sParticle, tiles = Input(screen, holding_mouse, sParticle, tiles)
        #update
        tiles, timers = Update(holding_mouse, sParticle, tiles, timers)
        #render
        screen = Render(screen, tiles, font, clock)

        clock.tick(GAME_SPEED)

def Input(screen, holding_mouse, sParticle, tiles):

    # Handle inputs
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen, tiles = Reset(screen)
            elif event.key == pygame.K_1:
                sParticle = "Sand"
            elif event.key == pygame.K_2:
                sParticle = "Dirt"
            elif event.key == pygame.K_3:
                sParticle = "Snowflake"
            elif event.key == pygame.K_4:
                sParticle = "Smoke"
        if event.type == pygame.MOUSEBUTTONDOWN:
            holding_mouse = True
        elif event.type == pygame.MOUSEBUTTONUP:
            holding_mouse = False
        if event.type == pygame.QUIT:
            pygame.quit()

    return screen, holding_mouse, sParticle, tiles

def Update(holding_mouse, sParticle, tiles, timers):
    # Spawn particles
    if holding_mouse:
        tiles = spawn_particle(sParticle, tiles)

    tiles = update_particles(tiles, timers)

    #Update timers
    for key, val in timers.items():
        val[0] = (val[0]+1) % val[1]

    return tiles, timers

def Render(screen, tiles, font, clock):
    screen.fill(Color.BLACK.value)
    for row in range(0, len(tiles)):
        for val in range(0, len(tiles[row])):
            if(tiles[row][val]==None):
                pass
            else:
                rect = pygame.Rect(val*PARTICLE_SIZE, row*PARTICLE_SIZE, PARTICLE_SIZE, PARTICLE_SIZE)
                pygame.draw.rect(screen, tiles[row][val].color, rect)

    #FPS Stuff
    fps = font.render(str(int(clock.get_fps())), True, (255,255,255))
    screen.blit(fps, (0, 0))
    pygame.display.flip()
    return screen

def Reset(screen):
    tiles = init_grid()
    screen.fill(Color.BLACK.value)
    return screen, tiles

def spawn_particle(sParticle, tiles):
    x, y = pygame.mouse.get_pos()
    row = y // PARTICLE_SIZE
    col = x // PARTICLE_SIZE
        
    # If particle already on tile, do nothing
    if tiles[row][col] != None:
        pass
    else: # Spawn a particle
        tiles[row][col] = SelectedParticle(sParticle, row, col)
    
    return tiles

def update_particles(tiles, timers):
    #Keep track of which tiles have already been updated
    updatedTiles = [[False]*(WINDOW_WIDTH // PARTICLE_SIZE)]* (WINDOW_HEIGHT // PARTICLE_SIZE)

    for row in range(len(tiles)-1, -1, -1):
        for val in range(0, len(tiles[row])):
            if (tiles[row][val] != None and tiles[row][val].pType != "Smoke"):
                tiles, updatedTiles = tiles[row][val].Move(tiles, updatedTiles, timers)
    for row in range(len(tiles)):
        for val in range(0, len(tiles[row])):
            if (tiles[row][val] != None and tiles[row][val].pType == "Smoke"):
                tiles, updatedTiles = tiles[row][val].Move(tiles, updatedTiles, timers)
    return tiles
    

def init_grid():
    tileWidth = WINDOW_WIDTH // PARTICLE_SIZE
    tileHeight = WINDOW_HEIGHT // PARTICLE_SIZE
    tiles = []

    for x in range(0, tileHeight):
        tiles.append([])
        for y in range(0, tileWidth):
            tiles[x].append(None)

    return tiles

def SelectedParticle(pType, x, y):
    if(pType == "Sand"):
        return SandParticle(x, y)
    elif(pType == "Dirt"):
        return DirtParticle(x, y)
    elif(pType == "Snowflake"):
        return SnowflakeParticle(x, y)
    elif(pType == "Smoke"):
        return SmokeParticle(x, y)        
    return None

if __name__ == "__main__":
    main(WINDOW_WIDTH, WINDOW_HEIGHT)
