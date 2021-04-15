import pygame
import random
import time
import sys

from colors import Color

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

GAME_SPEED = 144

GREEN_RATE = 8
BLUE_RATE = 16
RED_RATE = 32

block_size = 4
known_particles = []
particle_color = Color.BLUE.value
current_time = pygame.time.get_ticks()

def main(w, h):
    global GAME_SPEED, screen, particle_color, blue_timer, green_timer, red_timer
    holding_mouse = False

    pygame.init()
    init_grid()

    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    blue_timer = green_timer = red_timer = pygame.time.get_ticks()

    screen.fill(Color.BLACK.value)

    while True:

        # Handle inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    init_grid()
                    screen.fill(Color.BLACK.value)
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
        clock.tick(GAME_SPEED)

def spawn_particle():
    global particle_color, known_particles
    x, y = pygame.mouse.get_pos()
    row = y // block_size
    col = x // block_size

    def spawn_helper(r=row, c=col):
        tiles[r][c][1] = particle_color
        tiles[r][c][2] = True
        rect = pygame.Rect(tiles[r][c][0][0], tiles[r][c][0][1], block_size, block_size)
        pygame.draw.rect(screen, tiles[r][c][1], rect)
        known_particles.append([r, c, particle_color])

    # If particle already on tile, do nothing
    if [row, col] in known_particles:
        pass
    else: # Spawn a particle
        if tiles[row+1][col][2] == False:
            spawn_helper()
        else:
            if particle_color == Color.BLUE.value:
                if pygame.time.get_ticks() - blue_timer > BLUE_RATE:
                    spawn_helper()
            elif particle_color == Color.GREEN.value:
                if pygame.time.get_ticks() - green_timer > GREEN_RATE:
                    spawn_helper()
            elif particle_color == Color.RED.value:
                if pygame.time.get_ticks() - red_timer > RED_RATE:
                    spawn_helper()

def update_particles():

    global red_timer, blue_timer, green_timer, particle_color, current_time, known_particles

    to_remove = []
    to_append = []

    def update_helper(row, col, row_mod, col_mod):
        to_remove.append([row, col, tiles[row][col][1]])
        to_append.append([row+row_mod, col+col_mod, tiles[row][col][1]])

        tiles[row+row_mod][col+col_mod][1] = tiles[row][col][1]
        tiles[row][col][2] = False
        tiles[row+row_mod][col+col_mod][2] = True

        rect = pygame.Rect(tiles[row][col][0][0], tiles[row][col][0][1], block_size, block_size)
        pygame.draw.rect(screen, Color.BLACK.value, rect)
        rect = pygame.Rect(tiles[row+row_mod][col+col_mod][0][0], tiles[row+row_mod][col+col_mod][0][1], block_size, block_size)
        pygame.draw.rect(screen, tiles[row+row_mod][col+col_mod][1], rect)

    def particle_helper(i, j):
        if i == rows-1:
            return
        if tiles[i+1][j][2] == False:
            update_helper(i, j, 1, 0)
            return
        else:
            if j > 0:
                if tiles[i+1][j-1][2] == False: # Is there a particle below to the left?
                    update_helper(i, j, 1, -1)
                    return
            if j < cols-1:
                if tiles[i+1][j+1][2] == False: # Is there a particle below to the right?
                    update_helper(i, j, 1, 1)
                    return

    rows = WINDOW_HEIGHT // block_size
    cols = WINDOW_WIDTH // block_size
    reset_blue = False
    reset_green = False
    reset_red = False

    for particle in known_particles:
        if particle[2] == Color.BLUE.value:
            if pygame.time.get_ticks() - blue_timer > BLUE_RATE:
                reset_blue = True
                particle_helper(particle[0], particle[1])
        elif particle[2] == Color.GREEN.value:
            if pygame.time.get_ticks() - green_timer > GREEN_RATE:
                reset_green = True
                particle_helper(particle[0], particle[1])
        elif particle[2] == Color.RED.value:
            if pygame.time.get_ticks() - red_timer > RED_RATE:
                reset_red = True
                particle_helper(particle[0], particle[1])

    if reset_blue:
        blue_timer = pygame.time.get_ticks()
    if reset_green:
        green_timer = pygame.time.get_ticks()
    if reset_red:
        red_timer = pygame.time.get_ticks()

    for appender in to_append:
        known_particles.append(appender)

    for remover in to_remove:
        known_particles.remove(remover)

def init_grid():
    global tiles, block_size, particle_color
    tiles = [[]]
    row = 0
    for x in range(0, WINDOW_HEIGHT, block_size):
        for y in range(0, WINDOW_WIDTH, block_size):
            tiles[row].append([(y, x), particle_color, False])
        row += 1
        if x < WINDOW_HEIGHT - block_size:
            tiles.append([])

if __name__ == "__main__":
    main(WINDOW_WIDTH, WINDOW_HEIGHT)
