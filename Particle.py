from colors import *

class Particle:
    def __init__(self, pType, row, col, pCol, speed):
        self.pType = pType
        self.pos = (row,col)
        self.color = pCol
        self.speed = speed
    
    def MoveDown(self, tiles, upTiles, timer, spread):
        if(timer[0] != 0):
            return tiles, upTiles

        lFlag = False
        rFlag = False
        flag = False
        temp = None
        r = self.pos[0]
        c = self.pos[1]
        xMov = 0
        yMov = 0

        if(upTiles[r][c]):
            return tiles, upTiles
        elif(r < len(tiles)-1):
            if(tiles[r+1][c]==None):
                yMov = 1
                flag = True
            #If water swap
            elif(type(tiles[r+1][c])==WaterParticle):
                temp = tiles[r+1][c] 
                tiles[r+1][c].pos = (r,c)
                yMov = 1
                flag = True
            else:
                for x in range(1,spread):
                    if((not lFlag) and c-x >= 0):
                        if(tiles[r+1][c-x]==None):
                            yMov = 1
                            xMov = -x
                            flag = True
                            break
                        #If its water, swap
                        elif(type(tiles[r+1][c-x])==WaterParticle):
                            temp = tiles[r+1][c-x]
                            tiles[r+1][c-x].pos = (r,c)
                            flag = True
                            yMov = 1
                            xMov = -x
                            break
                        elif(type(tiles[r+1][c-x])!=type(self)):
                            lFlag = True

                    if((not rFlag) and c+x < len(tiles[0])):
                        if(tiles[r+1][c+x]==None):
                            yMov = 1
                            xMov = x
                            flag = True
                            break
                        #If its water, swap
                        elif(type(tiles[r+1][c+x])==WaterParticle):
                            temp = tiles[r+1][c+x] 
                            tiles[r+1][c+x].pos = (r,c)
                            flag = True
                            yMov = 1
                            xMov = x
                            break
                        elif(type(tiles[r+1][c+x])!=type(self)):
                            rFlag = True


        if(flag):
            tiles[r+yMov][c+xMov] = self
            tiles[r][c] = temp
            upTiles[r+yMov][c+xMov] = True
            self.pos = (r+yMov, c+xMov)

        return tiles, upTiles
    
    def MoveUp(self, tiles, upTiles, timer, spread):
        if(timer[0] != 0):
            return tiles, upTiles

        lFlag = rFlag = flag = False
        r = self.pos[0]
        c = self.pos[1]
        xMov = 0
        yMov = 0

        if(upTiles[r][c]):
            return tiles, upTiles
        elif(r > 0):
            if(tiles[r-1][c]==None):
                yMov = -1
                flag = True
            else:
                for x in range(1,spread):
                    if((not lFlag) and c-x >= 0):
                        if(tiles[r-1][c-x]==None):
                            yMov = -1
                            xMov = -x
                            flag = True
                            break
                        elif(type(tiles[r-1][c-x])!=type(self)):
                            lFlag = True
                    if((not rFlag) and c+x < len(tiles[0])):
                        if(tiles[r-1][c+x]==None):
                            yMov = -1
                            xMov = x
                            flag = True
                            break
                        elif(type(tiles[r-1][c+x])!=type(self)):
                            rFlag = True

        if(flag):
            tiles[r+yMov][c+xMov] = self
            tiles[r][c] = None
            upTiles[r+yMov][c+xMov] = True
            self.pos = (r+yMov, c+xMov)

        return tiles, upTiles


class SandParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Sand", x, y, (194, 178, 128), 2)

    def Move(self, tiles, upTiles, timers):
        return super().MoveDown(tiles, upTiles, timers[self.pType], 2)

class DirtParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Dirt", x, y, (155, 118, 83), 4)

    def Move(self, tiles, upTiles, timers):
        return super().MoveDown(tiles, upTiles, timers[self.pType], 1)

class SnowflakeParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Snowflake", x, y, (0, 200, 200), 8)

    def Move(self, tiles, upTiles, timers):
        return super().MoveDown(tiles, upTiles, timers[self.pType], 3)

class SmokeParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Smoke", x, y, (130, 130, 130), 4)

    def Move(self, tiles, upTiles, timers):
        return super().MoveUp(tiles, upTiles, timers[self.pType], 10)

class WaterParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Water", x, y, (0, 150, 255), 1)

    def Move(self, tiles, upTiles, timers):
        if(timers[self.pType][0] != 0):
            return tiles, upTiles

        lFlag = False
        rFlag = False
        flag = False
        r = self.pos[0]
        c = self.pos[1]
        xMov = 0
        yMov = 0

        if(upTiles[r][c]):
            return tiles, upTiles
        elif(r < len(tiles)-1):
            if(tiles[r+1][c]==None):
                yMov = 1
                flag = True
            else:
                for x in range(1,25):
                    if((not lFlag) and c-x >= 0):
                        if(tiles[r+1][c-x]==None):
                            yMov = 1
                            xMov = -x
                            flag = True
                            break
                        elif(type(tiles[r+1][c-x])!=type(self)):
                            lFlag = True

                    if((not rFlag) and c+x < len(tiles[0])):
                        if(tiles[r+1][c+x]==None):
                            yMov = 1
                            xMov = x
                            flag = True
                            break
                        elif(type(tiles[r+1][c+x])!=type(self)):
                            rFlag = True

        if(flag):
            tiles[r+yMov][c+xMov] = self
            tiles[r][c] = None
            upTiles[r+yMov][c+xMov] = True
            self.pos = (r+yMov, c+xMov)

        return tiles, upTiles

class StoneParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Stone", x, y, (70, 70, 70), 1)

    def Move(self, tiles, upTiles, timers):
        return tiles, upTiles

class FireParticle(Particle):
    def __init__(self, x, y):
        super().__init__("Fire", x, y, (255, 50, 0), 2)
        self.lifespan = 7

    def Move(self, tiles, upTiles, timers):
        self.LifeSpanTick()
        #Move with noise
        return tiles, upTiles

    def LifeSpanTick(self):
        self.lifespan -= 1
        if(self.lifespan < 6):
            self.color = (255, 104, 0)
        elif(self.lifespan < 4):
            self.color = (255, 154, 0)
        elif(self.lifespan < 2):
            self.color = (255, 204, 0)
        return

class ReverseSandParticle(Particle):
    def __init__(self, x, y):
        super().__init__("ReverseSand", x, y, (194, 178, 128), 2)

    def Move(self, tiles, upTiles, timers):
        return super().MoveUp(tiles, upTiles, timers[self.pType], 2)