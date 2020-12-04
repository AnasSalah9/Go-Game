import Stone
import Opponent
import Agent

class Board:
    'the Board class'

    def __init__(self, points = None, koPosition = (-1,-1), boardSize = 9):
        if(points == None):
            self.points = [[None for _ in range(boardSize)] for _ in range(boardSize)]
        else:
            self.points = points
        self.koPosition = koPosition
        self.boardSize = boardSize

    def inTheBoard(self, x, y):
        # check if the given point is inside the board
        return (x >= 0 and x < self.boardSize and y >= 0 and y < self.boardSize)


    def findNeighbours(self, stone):
        #find all the neighbours of the given stone
        posx, posy = stone.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return [(posx+x, posy+y) for x, y in directions if self.inTheBoard(posx+x, posy+y)]


    def findGroup(self, stoneX):
        # return a list of stones that represents the group of the given stone
        group = [stoneX]
        for stone in group:
            li = self.findNeighbours(stone)
            for x, y in li:
                if(self.points[x, y] != None and self.points[x, y].color == stoneX.color and self.points[x, y] not in group):
                    group.append(self.points[x, y])
        return group


    def countLiberty(self, stoneX):
        # find the total liberities of the given stone considering it's group
        liberty = {}
        for stone in self.findGroup(stoneX):
            li = self.findNeighbours(stone)
            for x, y in li:
                if(self.points[x, y] == None):
                    liberty.add((x,y))
        return len(liberty)


    def legal(self, stoneX):
        #check if stone position is legall
        x, y = stoneX.position
        return (self.inTheBoard(x, y) and self.points[x, y] == None and (x, y) != self.koPosition and self.countLiberty(stoneX) > 0)



    def checkKo(self, capturedStone, attackerStone):
        # check if the position of the captured stone is a ko Position
        return (len(self.findGroup(capturedStone)) == 1 and len(self.findGroup(attackerStone)) == 1 and self.countLiberty(attackerStone) == 0)



    def capture(self, attackerStone):
        # if attackerStone capture any opponent stones remove opponent stones from the board
        def removeFromBoard(group):
            # remove the given group of stones from the board
            for stone in group:
                x, y = stone.position
                self.points[x, y] = None

        totalCaptured = 0
        self.koPosition = (-1, -1)
        for x, y in self.findNeighbours(attackerStone):
            if(self.points[x, y] != None and self.points[x, y].color != attackerStone.color and self.countLiberty(self.points[x, y]) == 0):
                group = self.findGroup(self.points[x, y])
                totalCaptured += len(group)
                if(self.checkKo(self.points[x, y], attackerStone)):
                    self.koPosition = (x, y)
                removeFromBoard(group)
        if(totalCaptured > 1):
            self.koPosition = (-1, -1)


    def placeOnBoard(self, stone):
        # put the given stone on the board
        x, y = stone.position
        self.points[x, y] = stone
        self.capture(stone)

    def Print(self, stone):
        print("this is the current state of game . for empty b for Agent w for Opponent captelLetter for last game")
        for i in range(9):
            for j in range(9):
                if(self.points[i, j] == None):
                    print(".", end="")
                elif((i, j) == stone.position):
                    print(stone.color[0],end="")
                else:
                    print([stone.color[0]].lower(), end="")
            print("")


    def turn(self):
        # change turns between the human player and the Agent
        cur = 'B'
        passCount = 0
        human = Opponent.Opponent('White')
        AI = Agent.Agent('Black')
        while(passCount < 2):
            if(cur == 'B'):
                cur = 'W'
                stone = AI.nextMove(self.points)
                x, y = stone.position
                if(x == -1 and y == -1):
                    passCount += 1
                else:
                    self.placeOnBoard(stone)
                    passCount = 0
            else:
                cur = 'B'
                while(True):
                    stone = human.nextMove()
                    x, y = stone.position
                    if(x == -1 and y == -1):
                        passCount += 1
                    elif(self.legal(stone)):
                        self.placeOnBoard(stone)
                        passCount = 0
                    else:
                        print("this move not legal")
                        continue
                    break
            self.Print(stone)

        def calculateTerritory(self):
            #returns a tuble of (BTerritory, WTerritory)
            vis = [[0 for _ in range(9)] for _ in range(9)]
            Bterr = 0
            Wterr = 0

            def BFS(self , x, y):
                #clalculate territory for a single player
                stoneX = Stone('Black', (-1, -1))
                cnt = 0
                Bflage = False
                Wflage = False
                q = [(x, y)]
                for i, j in q:
                    nonlocal  Bterr
                    nonlocal  Wterr
                    if(vis[i][j] == 1):
                        continue
                    vis[i][j] = 1
                    if(self.points[i, j] == None):
                        ++cnt
                        stoneX.position = (i, j)
                        q += self.findNeighbours(stoneX)
                    elif(self.points[i, j].color == 'Black'):
                        Bflage = True
                    else:
                        Wflage = True
                    if(Bflage and Wflage):
                        cnt = 0
                        break
                if(Bflage):
                    Bterr += cnt
                else:
                    Wterr += cnt


            for x in range(9):
                for y in range(9):
                    if(self.points[x, y].color == 'Black'):
                        Bterr += 1
                    elif(self.points[x, y].color == 'White'):
                        Wterr += 1
                    else:
                        BFS(x, y)
            return (Bterr, Wterr)
