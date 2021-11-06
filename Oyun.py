import pygame as p
import Tahta

WIDTH = HEIGHT = 512 #400 diğer seçenek
DIMENSION = 10 # tahtanın boyutu 8x8 
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15   # ANİMASYONLAR İÇİN 
IMAGES = {}
#taşların resimlerini almak için kullanıyoruz
def loadImage():
    pieces = ["bA","bF","bK","bP","bS","bV","sA","sF","sK","sP","sS","sV"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))

#programı çalıştırıcak olan bölüm

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Tahta.GameState()
    loadImage()  #bir kere yapmak yeterli
    running = True
    sqSelected = () #oyuncunun seçtigi kareyi kaydetmek için (col , row) / şuanda seçili değil
    playerClicks = []  #oyuncunun tıklamalarını kaydetmek için / 2 tıklama (6,4)/(4,4)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # location 2 değer alır (farenin x ve y değerlerini)
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #oyuncunun aynı iki kareyi seçmemesi için
                    sqSelected = () # seçilen kareyi temizler
                    playerClicks = [] # oyuncunun seçtigi iki kareyi temizler
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)  #append birinci ve ikinci tıklamayı eklemek için
                if len(playerClicks) == 2 : #ikinci tıklamadan sonra
                    move = Tahta.Adım(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () # kullanıcı tıklamalarını silmek için
                    playerClicks = []
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen,gs):
    drawBoard(screen)  # oyunun karelerini çizmek için
    drawPieces(screen, gs.board) #oyunun taşlarını çizmek için


def drawBoard(screen):
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



if __name__ == "__main__":
    main()