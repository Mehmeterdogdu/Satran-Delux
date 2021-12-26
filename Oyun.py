from os import pipe
import pygame as p
import Tahta,bot

'''
x)bot sona taş getirince bir taş yok ediyor mu bilmiyorum deneyemiyorum
x.2)botlar oynarken log.move'u yazdıramıyorum
5,5) yeni taş ekle
5,75) piyon sona gelince seçebilicegi taşları renklendirme eklenicek
6) data base eklenicek
7)rok eklenebilir çok sanmıyorum ama
'''

WIDTH = HEIGHT = 800 #400 diğer seçenek
DIMENSION = 10 # tahtanın boyutu 10x10
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15   # ANİMASYONLAR İÇİN 
IMAGES = {}
#taşların resimlerini almak için kullanıyoruz
def loadImage():
    pieces = ["bA","bF","bK","bP","bS","bV","sA","sF","sK","sP","sS","sV"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))

#programı çalıştırıcak olan bölüm

def main(taraf):
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))   #p.FULLSCREEN
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Tahta.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #hamle sırasını belirlemek için kullanılan veriyi azaltmak için
    animate = False
    loadImage()  #bir kere yapmak yeterli
    running = True
    sqSelected = () #oyuncunun seçtigi kareyi kaydetmek için (col , row) / şuanda seçili değil
    playerClicks = []  #oyuncunun tıklamalarını kaydetmek için / 2 tıklama (6,4)/(4,4)
    gameOver = False
    if taraf==1:
        playerOne = False
        playerTwo = True
    else:
        playerOne = True
        playerTwo = True
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
                    if sqSelected == (row,col): #oyuncunun aynı iki kareyi seçmemesi için
                        sqSelected = () # seçilen kareyi temizler
                        playerClicks = [] # oyuncunun seçtigi iki kareyi temizler
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)  #append birinci ve ikinci tıklamayı eklemek için
                    if len(playerClicks) == 2 and playerClicks[0] != (): #ikinci tıklamadan sonra
                        move = Tahta.Adım(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
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
            if gs.isPawnPromot(AIMove):
                gs.whiteToMove = not gs.whiteToMove
                if gs.whiteToMove:
                    turn = "b"
                else:
                    turn = "s"
                sqSelected = bot.yoket(turn)
                gs.whiteToMove = not gs.whiteToMove
                gs.piyonson(SQ_SIZE,sqSelected,gs.hamlesayısı)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs,validMoves,sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen,"Black wins by checkmate")
            else:
                drawText(screen,"white wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen,"Stalemate")
                
        
        clock.tick(MAX_FPS)
        p.display.flip()


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


def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)  # oyunun karelerini çizmek için
    hinglightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen, gs.board) #oyunun taşlarını çizmek için


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

            
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #eğer boş değilse
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

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

def drawText(screen, text):
    font = p.font.SysFont("Helvitca",32,True,False)
    textObject = font.render(text,0,p.Color("Gray"))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color("Black"))
    screen.blit(textObject,textLocation.move(2,2))

if __name__ == "__main__":
    main(2)