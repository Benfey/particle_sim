from colors import *

class Particle:
    def __init__(self, pType, row, col, pCol, speed):
        self.pType = pType
        self.pos = (row,col)
        self.color = pCol
        self.speed = speed
    
    def Move(self, tiles, upTiles, timers):
        if(timers[self.pType][0] != 0):
            return tiles, upTiles

        flag = False
        r = self.pos[0]
        c = self.pos[1]
        xMov = yMov = 0

        if(upTiles[r][c]):
            return tiles, upTiles

        if(r < len(tiles)-1):
            if(tiles[r+1][c]==None):
                yMov = 1
                flag = True

            elif(c > 0 and tiles[r+1][c-1]==None):
                yMov = 1
                xMov = -1
                flag = True

            elif(c < len(tiles[0])-1 and tiles[r+1][c+1]==None):
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


class SandParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Sand", x, y, (194, 178, 128), 2)

    def Move(self, tiles, upTiles, timers):
        return super().Move(tiles, upTiles, timers)

class DirtParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Dirt", x, y, (155, 118, 83), 4)

    def Move(self, tiles, upTiles, timers):
        return super().Move(tiles, upTiles, timers)

class SnowflakeParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Snowflake", x, y, (0, 200, 200), 16)

    def Move(self, tiles, upTiles, timers):
        return super().Move(tiles, upTiles, timers)

class SmokeParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Smoke", x, y, (130, 130, 130), 8)

    def Move(self, tiles, upTiles, timers):
        if(timers[self.pType][0] != 0):
            return tiles, upTiles

        flag = False
        r = self.pos[0]
        c = self.pos[1]
        xMov = yMov = 0

        if(upTiles[r][c]):
            return tiles, upTiles
        elif(r > 0):
            if(tiles[r-1][c]==None):
                yMov = -1
                flag = True
            else:
                for x in range(15):
                    if(c-x >= 0 and tiles[r-1][c-x]==None):
                        yMov = -1
                        xMov = -x
                        flag = True
                        break
                    elif(c+x < len(tiles[0]) and tiles[r-1][c+x]==None):
                        yMov = -1
                        xMov = x
                        flag = True
                        break

        if(flag):
            tiles[r+yMov][c+xMov] = self
            tiles[r][c] = None
            self.pos = (r+yMov, c+xMov)
            upTiles[r+yMov][c+xMov] = True
            upTiles[r][c] = False

        return tiles, upTiles