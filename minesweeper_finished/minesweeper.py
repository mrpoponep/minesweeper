import random
import pygame as py

WHITE=(255,255,255)
BLACK=(0,0,0)
YELLOW=(255,255,100)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
WIDTH, HEIGHT = 800, 900
PLANTED=0

TILE=50
CONER=100,100

BLANKPIECE=py.image.load("mine_rs/piece.png")
BLANKPIECE=py.transform.scale(BLANKPIECE,(TILE,TILE))
BOMBPIECE=py.image.load('mine_rs/bomb.png')
BOMBPIECE=py.transform.scale(BOMBPIECE,(TILE,TILE))
EXPLBOMBPIECE=py.image.load('mine_rs/bomb_exp.png')
EXPLBOMBPIECE=py.transform.scale(EXPLBOMBPIECE,(TILE,TILE))
FLAGPIECE=py.image.load('mine_rs/red_flag.png')
FLAGPIECE=py.transform.scale(FLAGPIECE,(TILE,TILE))
MINE_1=py.image.load('mine_rs/mine_1.png')
MINE_1=py.transform.scale(MINE_1,(TILE,TILE))
MINE_2=py.image.load('mine_rs/mine_2.png')
MINE_2=py.transform.scale(MINE_2,(TILE,TILE))
MINE_3=py.image.load('mine_rs/mine_3.png')
MINE_3=py.transform.scale(MINE_3,(TILE,TILE))
MINE_4=py.image.load('mine_rs/mine_4.png')
MINE_4=py.transform.scale(MINE_4,(TILE,TILE))
MINE_5=py.image.load('mine_rs/mine_5.png')
MINE_5=py.transform.scale(MINE_5,(TILE,TILE))
MINE_6=py.image.load('mine_rs/mine_6.png')
MINE_6=py.transform.scale(MINE_6,(TILE,TILE))
MINE_7=py.image.load('mine_rs/mine_7.png')
MINE_7=py.transform.scale(MINE_7,(TILE,TILE))
MINE_8=py.image.load('mine_rs/mine_8.png')
MINE_8=py.transform.scale(MINE_8,(TILE,TILE))
MINE_0=py.image.load('mine_rs/emptypiece.png')
MINE_0=py.transform.scale(MINE_0,(TILE,TILE))

pic_list={0:MINE_0,1:MINE_1,2:MINE_2,3:MINE_3,4:MINE_4,5:MINE_5,6:MINE_6,7:MINE_7,8:MINE_8}

WIN=py.display.set_mode((WIDTH,HEIGHT))
py.init()
py.display.set_caption("Minesweeper")

class Piece:
    def __init__(self,hasbomb,x,y):
        self.x=x
        self.y=y
        self.hasbomb=hasbomb
        self.flag=False
        self.falseclick=False
        self.clicked=False
        self.clear=False
        self.collide = WIN.blit(BLANKPIECE,(self.x*TILE+50,self.y*TILE+50))
        
        self.number=0
        
        self.neighbour=[]
        self.neighbourpiece=[]
    
    def checkWon(self):
        if self.flag == True and self.hasbomb==True and self.falseclick == False or self.clicked==True:
            return True
        else: return False

    def dig(self):
        if self.number==0 and self.clicked==True and self.hasbomb==False:
            for p in self.neighbourpiece:
                p.clicked=True

    def setNumAround(self):
        num = 0
        for neighbor in set(self.neighbourpiece):
            if neighbor.hasbomb==True:
                num += 1
        self.number = num 
        self.pic=pic_list[self.number]
    
    def setFlag(self):
        global PLANTED
        if self.flag==False:
            self.flag=True
            PLANTED+=1
        elif self.flag==True:
            self.flag=False
            PLANTED-=1
        print(PLANTED)

    def draw(self):
        if self.hasbomb==False:
            self.setNumAround()
        elif self.falseclick==True:
            self.pic=EXPLBOMBPIECE
        elif self.hasbomb==True and self.falseclick==False:
            self.pic=BOMBPIECE
        
        if self.clicked or self.clear==True:
            self.collide = WIN.blit(self.pic,(self.x*TILE+50,self.y*TILE+150))
        elif self.flag==True:
            self.collide = WIN.blit(FLAGPIECE,(self.x*TILE+50,self.y*TILE+150))
        else:
            self.collide = WIN.blit(BLANKPIECE,(self.x*TILE+50,self.y*TILE+150))
        self.dig()
        self.checkWon()

class Board:
    def __init__(self,prob,size):
        self.board=[]
        self.prob=prob
        self.size=size
        bomb_planted = 0

        self.win=False
        self.lose=False
        for row in range(self.size):
            r=[]
            for col in range (self.size):
                piece = Piece(False,row,col)
                r.append(piece)
            self.board.append(r)
        while bomb_planted < prob:
            r = random.randrange(1,self.size+1)
            c = random.randrange(1,self.size+1)
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                continue
            elif self.board[r][c].hasbomb == True :
                continue
            else:
                self.board[r][c].hasbomb=True
                bomb_planted+=1

    def draw(self):
        self.addNeighbour()
        for r in range(self.size):
            for c in range(self.size):
                self.board[r][c].draw()

    def setNeighbours(self,piece):
        for u in range(piece.x-1,piece.x+2):
            for c in range(piece.y-1,piece.y+2):
                if u == piece.x and c == piece.y:
                    continue
                if u <0 or u >= self.size or c <0 or c>=self.size:
                    continue
                if (u,c) not in piece.neighbour:
                    piece.neighbour.append((u,c))
                    piece.neighbourpiece.append(self.board[u][c])
    
    def addNeighbour(self):
        for row in self.board:
            for piece in row:
                self.setNeighbours(piece)
    
    def solver(self):
        for row in self.board:
            for piece in row:
                piece.clear=True

    def updateBomb(self):
        global PLANTED
        bomb_remain=self.prob-PLANTED
        font = py.font.SysFont("comicsans", 25)
        text_bomb=font.render(f'BOMB REMAIN {bomb_remain}',1,WHITE)
        WIN.blit(text_bomb,(50,25))

    def checkWon(self):
        for row in self.board:
            for piece in row:
                if piece.checkWon()== False:
                    return False
        return True

def main():
    running=True
    paused=False
    FPS=60
    clock=py.time.Clock()
    boards=Board(25,14)
    counter,text=0,'0'

    while running:
        WIN.fill(BLACK)
        clock.tick(FPS)
        if paused == False:    
            for event in py.event.get():
                if event.type == py.QUIT:
                    running=False
                elif ( event.type == py.MOUSEBUTTONDOWN ):
                    mouse_position = py.mouse.get_pos()
                    mouse_buttons = py.mouse.get_pressed()
                    for r in boards.board:    
                        for piece in r:
                            if ( piece.collide.collidepoint(mouse_position) ) and mouse_buttons[0] and piece.flag==False:
                                piece.clicked=True
                                if piece.hasbomb==True:
                                    piece.falseclick=True
                                    paused=True
                                    boards.lose=True

                            elif ( piece.collide.collidepoint(mouse_position) ) and mouse_buttons[2]:
                                piece.setFlag() 
            counter += 1/60
        text = str(round(counter)).ljust(4)
        font = py.font.SysFont("comicsans", 25)
        text_bomb=font.render(f'TIMER: {text}',1,WHITE)
        WIN.blit(text_bomb,(45,80))
        
        boards.draw()
        boards.updateBomb()
        
        if boards.checkWon():
            paused=True
            boards.win=True
        if boards.lose==True:
            font = py.font.SysFont("comicsans", 50)
            font1 = py.font.SysFont("comicsans", 20)
            text_bomb=font.render('YOU LOSE!',1,RED)
            text_retry=font1.render('Press Enter to retry',1,RED)
            WIN.blit(text_retry,(430,100))
            WIN.blit(text_bomb,(400,30))        
        
        if boards.win==True:    
            font = py.font.SysFont("comicsans", 50)
            text_win=font.render('YOU WIN!',1,RED)
            WIN.blit(text_win,(400,30))

        if paused == True :    
            boards.solver()
            for event in py.event.get():
                if event.type == py.QUIT:
                    running=False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RETURN:
                        boards=Board(25,14)
                        paused=False
                        counter=0
            
        py.display.flip()
    py.quit()

main()
