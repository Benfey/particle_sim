from colors import *

class Particle:
    def __init__(self, pType, row, col, pCol, speed):
        self.pType = pType
        self.pos = (row,col)
        self.color = pCol
        self.speed = speed
        self.timer = 0


class SandParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Sand", x, y, (194, 178, 128), 8)

    def Move(self, tiles, upTiles):
        flag = False
        r = self.pos[0]
        c = self.pos[1]
        xMov = yMov = 0

        if(upTiles[r][c] or r == len(tiles)-1):
            return tiles, upTiles
        
        elif(tiles[r+1][c]==None):
            yMov = 1
            flag = True

        elif(tiles[r+1][c-1]==None):
            yMov = 1
            xMov = -1
            flag = True

        elif(tiles[r+1][c+1]==None):
            yMov = 1
            xMov = 1
            flag = True

        if(flag):
            tiles[r+yMov][c+xMov] = self
            tiles[r][c] = None
            self.pos = (r+yMov, c+xMov)
            upTiles[r+yMov][c+xMov] = True
            upTiles[r][c] = False

        return tiles, upTiles

class DirtParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Dirt", x, y, (155, 118, 83), 20)

    def Move(self, tiles):
        return

class SnowflakeParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Snowflake", x, y, (0, 200, 200), 40)

    def Move(self, tiles):
        return

class SmokeParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Snowflake", x, y, (130, 130, 130), 40)

    def Move(self, tiles):
        return