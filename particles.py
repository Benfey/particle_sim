import pygame
import random
import time
import sys

from colors import Color

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
block_size = 4
sand_speed = 12
particle_color = Color.BLUE.value

def main(w, h):
    global SCREEN, particle_color, timer
    holding_mouse = False

    pygame.init()
    init_grid()

    SCREEN = pygame.display.set_mode((w, h))
    timer = pygame.time.get_ticks()
    SCREEN.fill(Color.BLACK.value)

    while True:

        # Handle inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    init_grid()
                    SCREEN.fill(Color.BLACK.value)
                if event.key == pygame.K_1:
                    particle_color = Color.RED.value
                if event.key == pygame.K_2:
                    particle_color = Color.GREEN.value
                if event.key == pygame.K_3:
                    particle_color = Color.BLUE.value
            if event.type == pygame.MOUSEBUTTONDOWN:
                holding_mouse = True
            if event.type == pygame.MOUSEBUTTONUP:
                holding_mouse = False
            if event.type == pygame.QUIT:
                pygame.quit()

        # Spawn particles
        if holding_mouse:
            spawn_particle()

        update_particles()
        pygame.display.update()

def spawn_particle():
    global particle_color
    x, y = pygame.mouse.get_pos()
    row = y // block_size
    col = x // block_size

    # If particle already on tile, do nothing
    if tiles[row][col][1]:
        pass
    else: # Spawn a particle
        tiles[row][col][1] = True
        tiles[row][col][3] = particle_color
        rect = pygame.Rect(tiles[row][col][0][0], tiles[row][col][0][1], block_size, block_size)
        pygame.draw.rect(SCREEN, tiles[row][col][3], rect)

def update_particles():

    global timer, sand_speed, particle_color

    def update_helper(row, col, row_mod = 1, col_mod = 0):
        tiles[row][col][1] = False
        tiles[row+row_mod][col+col_mod][1] = True
        tiles[row][col][2] = True
        tiles[row+row_mod][col+col_mod][2] = False
        tiles[row+row_mod][col+col_mod][3] = tiles[row][col][3]
        to_reset.append([row+row_mod, col+col_mod])
        rect = pygame.Rect(tiles[row][col][0][0], tiles[row][col][0][1], block_size, block_size)
        pygame.draw.rect(SCREEN, Color.BLACK.value, rect)
        rect = pygame.Rect(tiles[row+row_mod][col+col_mod][0][0], tiles[row+row_mod][col+col_mod][0][1], block_size, block_size)
        pygame.draw.rect(SCREEN, tiles[row+row_mod][col+col_mod][3], rect)
        return [row+row_mod, col+col_mod]

    to_reset = []

    rows = WINDOW_HEIGHT // block_size
    cols = WINDOW_WIDTH // block_size

    if pygame.time.get_ticks()-timer > sand_speed:
        for i in range(rows-1, 0, -1):
            for j in range(cols-1, -1, -1):
                if tiles[i][j][1] and tiles[i][j][2]: # We have a particle that we have not already updated
                    # Are we at border?
                    if i == rows-1:
                        continue
                    if tiles[i+1][j][1] == False: # Is there a particle below?
                        # If not, move the particle down
                        to_reset.append(update_helper(i, j, 1, 0))
                        continue
                    else:
                        if j > 0:
                            if tiles[i+1][j-1][1] == False: # Is there a particle below to the left?
                                to_reset.append(update_helper(i, j, 1, -1))
                                continue
                        if j < cols-1:
                            if tiles[i+1][j+1][1] == False: # Is there a particle below to the right?
                                to_reset.append(update_helper(i, j, 1, 1))
                                continue
        for reset in to_reset:
            tiles[reset[0]][reset[1]][2] = True
        timer = pygame.time.get_ticks()

def init_grid():
    global tiles, block_size, particle_color
    tiles = [[]]
    row = 0
    for x in range(0, WINDOW_HEIGHT, block_size):
        for y in range(0, WINDOW_WIDTH, block_size):
            tiles[row].append([(y, x), False, True, particle_color])
        row += 1
        if x < WINDOW_HEIGHT - block_size:
            tiles.append([])

if __name__ == "__main__":
    main(WINDOW_WIDTH, WINDOW_HEIGHT)
