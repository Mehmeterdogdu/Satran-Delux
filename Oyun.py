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
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False
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