from os import pipe
import pygame as p
from pygame import font
import Tahta,bot,kaydet
from PyQt5 import QtCore, QtGui, QtWidgets
'''
x)bot sona taş getirince bir taş yok ETMİYOR çalışmıyor
x)son kalan taş sahsa berabere bitme eklemedim
5,75) piyon sona gelince seçebilicegi taşları renklendirme eklenicek 
7) bi ara bota biraz zeka ekle
8) movelog kaydediliyor ama oyun başlayınca kullanılmıyor
'''

tahta_WIDTH = tahta_HEIGHT = 700 
moveLogPanelWıdth = 300
moveLogPanelHeıght = tahta_HEIGHT
DIMENSION = 10 # tahtanın boyutu 10x10
SQ_SIZE = tahta_HEIGHT // DIMENSION
MAX_FPS = 15   # ANİMASYONLAR İÇİN 
IMAGES = {}
#taşların resimlerini almak için kullanıyoruz
def loadImage():
    pieces = ["bA","bF","bK","bP","bY","bS","bV","sA","sF","sK","sP","sS","sV","sY"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))

#programı çalıştırıcak olan bölüm
def main(taraf,renk,kayıtlıoyun,tahta,sırasayısı):
    p.init()
    screen = p.display.set_mode((tahta_WIDTH+moveLogPanelWıdth,tahta_HEIGHT))   #p.FULLSCREEN
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial",16,False,False)
    gs = Tahta.GameState()
    if sırasayısı == 1: #eğer sayı 1 se siyah oynar
            gs.changeturn()
    validMoves = gs.getValidMoves()
    moveMade = False #hamle sırasını belirlemek için kullanılan veriyi azaltmak için
    animate = False
    loadImage()  #bir kere yapmak yeterli
    running = True
    sqSelected = () #oyuncunun seçtigi kareyi kaydetmek için (col , row) / şuanda seçili değil
    playerClicks = []  #oyuncunun tıklamalarını kaydetmek için / 2 tıklama (6,4)/(4,4)
    gameOver = False
    if taraf==1:
        if renk == "1":
            playerOne = True
            playerTwo = False
        else:
            playerOne= False
            playerTwo = True
    else:
        playerOne = True
        playerTwo = True
    print(kayıtlıoyun)
    if kayıtlıoyun == 0:
        pass
    else:
        gs.board = tahta
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False
                #fare düzenleyicisi
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # location 2 değer alır (farenin x ve y değerlerini)
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if 620<= location[1] <=670 and 800 <= location[0] <= 950:
                        süre = "0"
                        if gs.whiteToMove:
                            sıra = "sıra beyazda"
                            sırasayı = 0
                            mainwindow = QtWidgets.QMainWindow()
                            ui = kaydet.kaydet()
                            ui.setupUi(mainwindow,sıra,sırasayı,süre,gs.moveLog,gs.board,taraf,renk)
                            mainwindow.show()
                            
                        else:
                            sıra = "sıra siyahta"
                            sırasayı = 1
                            mainwindow = QtWidgets.QMainWindow()
                            ui = kaydet.kaydet()
                            ui.setupUi(mainwindow,sıra,sırasayı,süre,gs.moveLog,gs.board,taraf,renk)
                            mainwindow.show()
                    elif sqSelected == (row,col) or col >=10: #oyuncunun aynı iki kareyi seçmemesi için
                        sqSelected = () # seçilen kareyi temizler
                        playerClicks = [] # oyuncunun seçtigi iki kareyi temizler
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)  #append birinci ve ikinci tıklamayı eklemek için
                    if len(playerClicks) == 2 and playerClicks[0] != (): #ikinci tıklamadan sonra
                        move = Tahta.Adım(playerClicks[0], playerClicks[1], gs.board)
                        for(i) in range(len(validMoves)):
                            if move == validMoves[i]:     #eğer hamle izin verilen hareketlerdense yapılabilir
                                gs.makeMove(validMoves[i])   #if içine almak için bir kere tab
                                if gs.isPawnPromot(validMoves[i]):
                                    gs.piyonson(SQ_SIZE,sqSelected,gs.hamlesayısı)
                                moveMade = True      #if içine almak için bir kere tab
                                animate = True
                                sqSelected = () # kullanıcı tıklamalarını silmek için
                                playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]    
            # geri alma tuşu
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                        gs = Tahta.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = True
                        animate = False
                        gs.checkMate = False
                        gs.staleMate = False
                        gameOver = False
                if e.key == p.K_q:
                    running=False

        if not gameOver and not humanTurn :
            AIMove = bot.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            '''
            if gs.isPawnPromot(AIMove):
                gs.whiteToMove = not gs.whiteToMove
                if gs.whiteToMove:
                    turn = "b"
                else:
                    turn = "s"
                sqSelected = bot.yoket(turn)
                gs.whiteToMove = not gs.whiteToMove
                gs.piyonson(SQ_SIZE,sqSelected,gs.hamlesayısı)'''
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs,validMoves,sqSelected,moveLogFont)

        if gs.checkMate or gs.staleMate:
            gameOver = True
            if gs.staleMate:
                gameOver = True
                text ="Stalemate"
            else:
                if gs.whiteToMove:
                    text ="Black wins by checkmate"
                else:
                    text ="white wins by checkmate" 
            drawEndGameText(screen,text)
                
        
        clock.tick(MAX_FPS)
        p.display.flip()


def drawPiyonSon(gs,screen):
    for r in range(0,10):
        for c in range(0,10):
            if gs.board[r][c][0] == ("b" if gs.whiteToMove else "s"):
                s = p.Surface((SQ_SIZE,SQ_SIZE))
                s.set_alpha(100)
                s.fill(p.Color("black"))
                screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))

def drawGameState(screen,gs,validMoves,sqSelected,moveLogFont):
    drawBoard(screen)  # oyunun karelerini çizmek için
    hinglightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen, gs.board) #oyunun taşlarını çizmek için
    drawMoveLog(screen,gs,moveLogFont)
    kaydetbuton(screen)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def hinglightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ("b" if gs.whiteToMove else "s"):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol,SQ_SIZE*move.endRow))
            
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #eğer boş değilse
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen,gs,font):
    moveLogRect = p.Rect(tahta_WIDTH,0,moveLogPanelWıdth,moveLogPanelHeıght)
    p.draw.rect(screen,p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0,len(moveLog),2):
        movestring = "  "+str(i//2 +1) + ". " +moveLog[i].getChessNotation()+ " "
        if i+1 <len(moveLog):
            movestring += moveLog[i+1].getChessNotation()
        moveTexts.append(movestring)

    movesPerRow = 3
    padding = 5
    lanespacing = 3
    textY = padding
    for i in range(0 , len(moveTexts),movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text,True,p.Color("white"))
        textLocation = moveLogRect.move(padding,textY)
        screen.blit(textObject,textLocation)
        textY += textObject.get_height() + lanespacing

def kaydetbuton(screen):
    p.draw.rect(screen, (255,255,255), p.Rect(800, 620, 150, 50),0)
    font=p.font.SysFont("Arial",16,True,False)
    Yazı = font.render("Oyunu Kaydet",0,(255,0,0))
    screen.blit(Yazı,(814,633))


def animateMove(move,screen,board,clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c = (move.startRow + dR*frame/frameCount,move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        color = colors[(move.endRow + move.endCol)% 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca",32,True,False)
    textObject = font.render(text,0,p.Color("Gray"))
    textLocation = p.Rect(0,0,tahta_WIDTH,tahta_HEIGHT).move(tahta_WIDTH/2-textObject.get_width()/2,tahta_HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color("Black"))
    screen.blit(textObject,textLocation.move(2,2))

if __name__ == "__main__":
    main(2,0,0,0,0)