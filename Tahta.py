class GameState():
    def __init__(self) :
        #tahta 10x10 ve bütün liste elemanları 2 karakterli
        #ilk harfleri rengi temsil ediyor b = beyaz , s = siyah
        #ikinci harfleri hangi taş olduklarını gösteriyor K = kale, A = at, F = fil, V = Vezir, S= Şah, P = piyon, Y = yeni eklenicek taş
        # "--" boş kareler oldugunu gösteriyor.
        self.board = [
            ["sK","sA","sA","sF","sV","sS","sF","sA","sA","sK"],
            ["sP","sP","sP","sP","sP","sP","sP","sP","sP","sP"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["bP","bP","bP","bP","bP","bP","bP","bP","bP","bP"],
            ["bK","bA","bA","bF","bV","bS","bF","bA","bA","bK"],
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol]= move.pieceMoved
        self.moveLog.append(move) #log the move şuanda boş 
        self.whiteToMove = not self.whiteToMove #oyuncu değişmek için
    
    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #turu diğer oyuncuya geçirmek için

# satrançtaki yapılması uygun bütün hamleler örnek : 
   # eğer bir taş şahı tehtit ederse bu tehtidi engellemek dışındaki bütün hamleler geçersin olur.
    
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    #satrançta yapılabilen tün hamleler
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "b" and self.whiteToMove) or (turn == "s" and not self.whiteToMove):
                    piece = self.board[r][c][1]
            #isimlerine göre taşların yapabiliceği hamleler
                    if piece == "P":
                        self.getPiyonMoves(r,c,moves) #piyon hamleleri
                    elif piece == "K":
                        self.getKaleMoves(r,c,moves) #Kale hareketleri
                    elif piece == "A":
                        self.getAtMoves(r,c,moves)  #At hareketleri
                    elif piece == "F":
                        self.getFilMoves(r,c,moves)
                    elif piece == "V":
                        self.getVezirMoves(r,c,moves)
                    elif piece == "S":
                        self.getSahMoves(r,c,moves)
        return moves
    #taş hareketleri

    def getPiyonMoves(self, r,c,moves): #piyon
        if self.whiteToMove: #eğer beyazın hamlesiyse
            if r-1 >= 0 and self.board[r-1][c]== "--": #eğer ilerisindeki kare boş ise
                moves.append(Adım((r,c),(r-1,c),self.board))
                if r == 8 and self.board[r-2][c] =="--": #2 adım ilerlemesi için
                    moves.append(Adım((r,c),(r-2,c),self.board)) 
            if r-1 >= 0 and c-1 >= 0 and self.board[r-1][c-1][0] == "s":  #soldaki taşı yemek için
                moves.append(Adım((r,c),(r-1,c-1),self.board)) 
            if r-1 >= 0 and c+1 <= 9 and self.board[r-1][c+1][0] == "s":  #sağdaki taşı yemek için
                moves.append(Adım((r,c),(r-1,c+1),self.board)) 
        
        else: #siyah hamlesi için
            if r+1 <= 9 and self.board[r+1][c]== "--": #eğer ilerisindeki kare boş ise
                moves.append(Adım((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] =="--": #2 adım ilerlemesi için
                    moves.append(Adım((r,c),(r+2,c),self.board)) 
            if r+1 <= 9 and c-1 >= 0 and self.board[r+1][c-1][0] == "b":  #sağdaki taşı yemek için
                moves.append(Adım((r,c),(r+1,c-1),self.board)) 
            if r+1 <= 9 and c+1 <= 9 and self.board[r+1][c+1][0] == "b":  #soldaki taşı yemek için
                moves.append(Adım((r,c),(r+1,c+1),self.board)) 


    def getKaleMoves(self,r,c,moves):   #kale
        ileris = 0 
        sols = 0
        sağs= 0
        geris = 0
        ilerib = 0
        solb= 0
        sağb=0
        gerib = 0  
        #beyaz karenin hareketleri
        if self.whiteToMove: #eğer beyazın hamlesiyse
            for x in range(len(self.board)):    
                if r-x >= 0 and (self.board[r-x][c]== "--"): #boş kareye ilerleme
                    if ileris == 0 and ilerib ==1:
                        moves.append(Adım((r,c),(r-x,c),self.board))
                if r-x >= 0 and self.board[r-x][c][0]=="s": # dolu kareye ilerleme
                    if ileris == 0 and ilerib ==1:
                        moves.append(Adım((r,c),(r-x,c),self.board)) 
                        ileris = 1
                if r-x >=0 and self.board[r-x][c][0]== "b" :
                    ilerib = ilerib+1

                if c-x >=0 and self.board[r][c-x]== "--": #boş kareye sola gitmek için
                    if sols == 0 and solb ==1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                if c-x >= 0 and self.board[r][c-x][0]=="s": #dolu kareye sola gitmek için
                    if sols == 0 and solb ==1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                        sols=1
                if c-x >=0 and self.board[r][c-x][0]== "b" :
                    solb = solb+1
                
                if r+x <=9 and (self.board[r+x][c]== "--") : # boş kareye geri gitmek için
                    if geris == 0 and gerib == 1:
                            moves.append(Adım((r,c),(r+x,c),self.board))
                if r+x <=9 and self.board[r+x][c][0]=="s": #dolu geri gitmek için
                    if geris == 0 and gerib == 1:
                        moves.append(Adım((r,c),(r+x,c),self.board))
                        geris=1
                if r+x <=9 and self.board[r+x][c][0]== "b" :
                    gerib = gerib+1

                if c+x <=9 and (self.board[r][c+x]== "--") : # boş kareye sağa gitmek için
                    if sağs == 0 and sağb == 1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                if c+x <=9 and self.board[r][c+x][0]=="s": # dolu kareye sağa gitmek için
                    if sağs == 0 and sağb == 1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                        sağs=1
                if c+x <=9 and self.board[r][c+x][0]== "b" :
                    sağb = sağb+1
        else :  #siyah karenin hamlesi için
            for x in range(len(self.board)):    
                if r+x <=9 and (self.board[r+x][c]== "--"): #boş kareye ilerleme 0 'dan 9'e
                    if ilerib == 0 and ileris ==1:
                        moves.append(Adım((r,c),(r+x,c),self.board))
                if r+x <=9 and self.board[r+x][c][0]=="b": # dolu kareye ilerleme 0 'dan 9'e
                    if ilerib == 0 and ileris ==1:
                        moves.append(Adım((r,c),(r+x,c),self.board)) 
                        ilerib = 1
                if r+x <=9 and self.board[r+x][c][0]== "s" :
                    ileris = ileris+1

                if c+x <=9 and self.board[r][c+x]== "--": #boş kareye sağa gitmek için a'dan h'ye
                    if sağb == 0 and sağs ==1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                if c+x <=9 and self.board[r][c+x][0]=="b": #dolu kareye sağa gitmek için a'den h'ya
                    if sağb == 0 and sağs ==1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                        sağb=1
                if c+x <=9 and self.board[r][c+x][0]== "s" :
                    sağs = sağs+1
                
                if r-x >=0 and (self.board[r-x][c]== "--") : # boş kareye geri gitmek için 9'den 0 a
                    if gerib == 0 and geris == 1:
                            moves.append(Adım((r,c),(r-x,c),self.board))
                if r-x >=0 and self.board[r-x][c][0]=="b": #dolu geri gitmek için  9'den 0 a
                    if gerib == 0 and geris == 1:
                        moves.append(Adım((r,c),(r-x,c),self.board))
                        gerib=1
                if r-x >=0 and self.board[r-x][c][0]== "s" :
                    geris = geris+1

                if c-x >=0 and (self.board[r][c-x]== "--") : # boş kareye sola gitmek için h'den a'ya
                    if solb == 0 and sols == 1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                if c-x >=0 and self.board[r][c-x][0]=="b": # dolu kareye sola gitmek için h'den a'ya
                    if solb == 0 and sols == 1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                        solb=1
                if c-x >=0 and self.board[r][c-x][0]== "s" :
                    sols = sols+1

    def getAtMoves(self,r,c,moves):  #At
        if self.whiteToMove: #eğer beyazın hamlesiyse
          #  r-1 c+2 / r-1 c-2 / r-2 c+1/ r-2 c-1 / r+1 c-2/r+1 c+2 /r+2 c-1/r+2 c+1
            if r-1 >= 0 and c+2 <=9 and (self.board[r-1][c+2]== "--" or self.board[r-1][c+2][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-1,c+2),self.board))
            if r-1 >= 0 and c-2 >=0 and (self.board[r-1][c-2]== "--" or self.board[r-1][c-2][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-1,c-2),self.board))
            if r-2 >= 0 and c+1 <=9 and (self.board[r-2][c+1]== "--" or self.board[r-2][c+1][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-2,c+1),self.board))
            if r-2 >= 0 and c-1 >= 0 and (self.board[r-2][c-1]== "--" or self.board[r-2][c-1][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-2,c-1),self.board))
            if r+1 <=9 and c-2 >= 0 and (self.board[r+1][c-2]== "--" or self.board[r+1][c-2][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+1,c-2),self.board))
            if r+1 <= 9 and c+2 <= 9 and (self.board[r+1][c+2]== "--" or self.board[r+1][c+2][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+1,c+2),self.board))
            if r+2 <= 9 and c+1 <=9 and (self.board[r+2][c+1]== "--" or self.board[r+2][c+1][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+2,c+1),self.board))
            if r+2 <= 9 and c-1 >= 0 and (self.board[r+2][c-1]== "--" or self.board[r+2][c-1][0]== "s"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+2,c-1),self.board))
        else:
            if r-1 >= 0 and c+2 <=9 and (self.board[r-1][c+2]== "--" or self.board[r-1][c+2][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-1,c+2),self.board))
            if r-1 >= 0 and c-2 >=0 and (self.board[r-1][c-2]== "--" or self.board[r-1][c-2][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-1,c-2),self.board))
            if r-2 >= 0 and c+1 <=9 and (self.board[r-2][c+1]== "--" or self.board[r-2][c+1][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-2,c+1),self.board))
            if r-2 >= 0 and c-1 >= 0 and (self.board[r-2][c-1]== "--" or self.board[r-2][c-1][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r-2,c-1),self.board))
            if r+1 <=9 and c-2 >= 0 and (self.board[r+1][c-2]== "--" or self.board[r+1][c-2][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+1,c-2),self.board))
            if r+1 <= 9 and c+2 <= 9 and (self.board[r+1][c+2]== "--" or self.board[r+1][c+2][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+1,c+2),self.board))
            if r+2 <= 9 and c+1 <=9 and (self.board[r+2][c+1]== "--" or self.board[r+2][c+1][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+2,c+1),self.board))
            if r+2 <= 9 and c-1 >= 0 and (self.board[r+2][c-1]== "--" or self.board[r+2][c-1][0]== "b"): #boş kare için / r-1 c+2
                moves.append(Adım((r,c),(r+2,c-1),self.board))

    def getFilMoves(self,r,c,moves):  #Fil
        solaltRakip=0
        solüstRakip=0
        sagüstRakip=0
        sagaltRakip=0
        solaltTakım=0
        solüstTakım=0
        sagüstTakım=0
        sagaltTakım=0
        if self.whiteToMove:
            for x in range(len(self.board)): #beyaz taşlar için
                #boş kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x]== "--"): # sağ alta gitmek için
                    if sagaltRakip == 0 and sagaltTakım <=1 :
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x]== "--"): # sağ üst gitmek için
                    if sagüstRakip == 0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x]== "--"): # sol alta gitmek için
                    if solaltRakip == 0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x]== "--"): # sol üst gitmek için
                    if solüstRakip == 0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))

                #dolu kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "s"): # sağ alta gitmek için
                    if sagaltRakip==0 and sagaltTakım <=1:    
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        sagaltRakip=1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "s"): # sağ üst gitmek için
                    if sagüstRakip==0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        sagüstRakip = 1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "s"): # sol alta gitmek için
                    if solaltRakip==0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        solaltRakip = 1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "s"): # sol üst gitmek için
                    if solüstRakip==0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                        solüstRakip = 1

                #kendi renginin üstünden adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "b"): # sağ alta gitmek için
                       sagaltTakım = sagaltTakım+1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "b"): # sağ üst gitmek için
                    sagüstTakım = sagüstTakım+1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "b"): # sol alta gitmek için
                    solaltTakım = solaltTakım+1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "b"): # sol üst gitmek için
                   solüstTakım = solüstTakım+1
        else:  # siyah taşlar için 
            for x in range(len(self.board)):
                #boş kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x]== "--"): # sağ alta gitmek için
                    if sagaltRakip == 0 and sagaltTakım <=1 :
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x]== "--"): # sağ üst gitmek için
                    if sagüstRakip == 0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x]== "--"): # sol alta gitmek için
                    if solaltRakip == 0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x]== "--"): # sol üst gitmek için
                    if solüstRakip == 0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))

                #dolu kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "b"): # sağ alta gitmek için
                    if sagaltRakip==0 and sagaltTakım <=1:    
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        sagaltRakip=1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "b"): # sağ üst gitmek için
                    if sagüstRakip==0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        sagüstRakip = 1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "b"): # sol alta gitmek için
                    if solaltRakip==0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        solaltRakip = 1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "b"): # sol üst gitmek için
                    if solüstRakip==0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                        solüstRakip = 1

                #kendi renginin üstünden adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "s"): # sağ alta gitmek için
                       sagaltTakım = sagaltTakım+1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "s"): # sağ üst gitmek için
                    sagüstTakım = sagüstTakım+1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "s"): # sol alta gitmek için
                    solaltTakım = solaltTakım+1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "s"): # sol üst gitmek için
                   solüstTakım = solüstTakım+1

    def getVezirMoves(self,r,c,moves):  #Vezir
        ileris = 0 
        sols = 0
        sağs= 0
        geris = 0
        ilerib = 0
        solb= 0
        sağb=0
        gerib = 0  
        solaltRakip=0
        solüstRakip=0
        sagüstRakip=0
        sagaltRakip=0
        solaltTakım=0
        solüstTakım=0
        sagüstTakım=0
        sagaltTakım=0
        #beyaz karenin hareketleri
        if self.whiteToMove: #beyaz vezir için
            #vezir düz gitme hamlesi

            for x in range(len(self.board)):    
                if r-x >= 0 and (self.board[r-x][c]== "--"): #boş kareye ilerleme
                    if ileris == 0 and ilerib ==1:
                        moves.append(Adım((r,c),(r-x,c),self.board))
                if r-x >= 0 and self.board[r-x][c][0]=="s": # dolu kareye ilerleme
                    if ileris == 0 and ilerib ==1:
                        moves.append(Adım((r,c),(r-x,c),self.board)) 
                        ileris = 1
                if r-x >=0 and self.board[r-x][c][0]== "b" :
                    ilerib = ilerib+1

                if c-x >=0 and self.board[r][c-x]== "--": #boş kareye sola gitmek için
                    if sols == 0 and solb ==1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                if c-x >= 0 and self.board[r][c-x][0]=="s": #dolu kareye sola gitmek için
                    if sols == 0 and solb ==1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                        sols=1
                if c-x >=0 and self.board[r][c-x][0]== "b" :
                    solb = solb+1
                
                if r+x <=9 and (self.board[r+x][c]== "--") : # boş kareye geri gitmek için
                    if geris == 0 and gerib == 1:
                            moves.append(Adım((r,c),(r+x,c),self.board))
                if r+x <=9 and self.board[r+x][c][0]=="s": #dolu geri gitmek için
                    if geris == 0 and gerib == 1:
                        moves.append(Adım((r,c),(r+x,c),self.board))
                        geris=1
                if r+x <=9 and self.board[r+x][c][0]== "b" :
                    gerib = gerib+1

                if c+x <=9 and (self.board[r][c+x]== "--") : # boş kareye sağa gitmek için
                    if sağs == 0 and sağb == 1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                if c+x <=9 and self.board[r][c+x][0]=="s": # dolu kareye sağa gitmek için
                    if sağs == 0 and sağb == 1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                        sağs=1
                if c+x <=9 and self.board[r][c+x][0]== "b" :
                    sağb = sağb+1

            #vezir çapraz gitme hamlesi 
            for x in range(len(self.board)): #beyaz taşlar için
                #boş kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x]== "--"): # sağ alta gitmek için
                    if sagaltRakip == 0 and sagaltTakım <=1 :
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x]== "--"): # sağ üst gitmek için
                    if sagüstRakip == 0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x]== "--"): # sol alta gitmek için
                    if solaltRakip == 0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x]== "--"): # sol üst gitmek için
                    if solüstRakip == 0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))

                #dolu kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "s"): # sağ alta gitmek için
                    if sagaltRakip==0 and sagaltTakım <=1:    
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        sagaltRakip=1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "s"): # sağ üst gitmek için
                    if sagüstRakip==0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        sagüstRakip = 1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "s"): # sol alta gitmek için
                    if solaltRakip==0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        solaltRakip = 1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "s"): # sol üst gitmek için
                    if solüstRakip==0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                        solüstRakip = 1

                #kendi renginin üstünden adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "b"): # sağ alta gitmek için
                       sagaltTakım = sagaltTakım+1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "b"): # sağ üst gitmek için
                    sagüstTakım = sagüstTakım+1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "b"): # sol alta gitmek için
                    solaltTakım = solaltTakım+1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "b"): # sol üst gitmek için
                   solüstTakım = solüstTakım+1
        else:
            #SİYAH VEZİRİN ÇAPRAZ İLERLEMESİ İÇİN
            for x in range(len(self.board)):
                #boş kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x]== "--"): # sağ alta gitmek için
                    if sagaltRakip == 0 and sagaltTakım <=1 :
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x]== "--"): # sağ üst gitmek için
                    if sagüstRakip == 0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x]== "--"): # sol alta gitmek için
                    if solaltRakip == 0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x]== "--"): # sol üst gitmek için
                    if solüstRakip == 0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))

                #dolu kareye adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "b"): # sağ alta gitmek için
                    if sagaltRakip==0 and sagaltTakım <=1:    
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        sagaltRakip=1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "b"): # sağ üst gitmek için
                    if sagüstRakip==0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        sagüstRakip = 1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "b"): # sol alta gitmek için
                    if solaltRakip==0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        solaltRakip = 1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "b"): # sol üst gitmek için
                    if solüstRakip==0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                        solüstRakip = 1

                #kendi renginin üstünden adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "s"): # sağ alta gitmek için
                       sagaltTakım = sagaltTakım+1
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "s"): # sağ üst gitmek için
                    sagüstTakım = sagüstTakım+1
                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "s"): # sol alta gitmek için
                    solaltTakım = solaltTakım+1
                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "s"): # sol üst gitmek için
                   solüstTakım = solüstTakım+1

            #SİYAH VEZİRİN DÜZ İLERLEMESİ İÇİN   
                if r+x <=9 and (self.board[r+x][c]== "--"): #boş kareye ilerleme 0 'dan 9'e
                    if ilerib == 0 and ileris ==1:
                        moves.append(Adım((r,c),(r+x,c),self.board))
                if r+x <=9 and self.board[r+x][c][0]=="b": # dolu kareye ilerleme 0 'dan 9'e
                    if ilerib == 0 and ileris ==1:
                        moves.append(Adım((r,c),(r+x,c),self.board)) 
                        ilerib = 1
                if r+x <=9 and self.board[r+x][c][0]== "s" :
                    ileris = ileris+1

                if c+x <=9 and self.board[r][c+x]== "--": #boş kareye sağa gitmek için a'dan h'ye
                    if sağb == 0 and sağs ==1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                if c+x <=9 and self.board[r][c+x][0]=="b": #dolu kareye sağa gitmek için a'den h'ya
                    if sağb == 0 and sağs ==1:
                        moves.append(Adım((r,c),(r,c+x),self.board))
                        sağb=1
                if c+x <=9 and self.board[r][c+x][0]== "s" :
                    sağs = sağs+1
                
                if r-x >=0 and (self.board[r-x][c]== "--") : # boş kareye geri gitmek için 9'den 0 a
                    if gerib == 0 and geris == 1:
                            moves.append(Adım((r,c),(r-x,c),self.board))
                if r-x >=0 and self.board[r-x][c][0]=="b": #dolu geri gitmek için  9'den 0 a
                    if gerib == 0 and geris == 1:
                        moves.append(Adım((r,c),(r-x,c),self.board))
                        gerib=1
                if r-x >=0 and self.board[r-x][c][0]== "s" :
                    geris = geris+1

                if c-x >=0 and (self.board[r][c-x]== "--") : # boş kareye sola gitmek için h'den a'ya
                    if solb == 0 and sols == 1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                if c-x >=0 and self.board[r][c-x][0]=="b": # dolu kareye sola gitmek için h'den a'ya
                    if solb == 0 and sols == 1:
                        moves.append(Adım((r,c),(r,c-x),self.board))
                        solb=1
                if c-x >=0 and self.board[r][c-x][0]== "s" :
                    sols = sols+1


    def getSahMoves(self,r,c,moves):  #Sah
        if self.whiteToMove: #eğer beyazın hamlesiyse
            if r+1 <= 9 and (self.board[r+1][c]== "--" or self.board[r+1][c][0]=="s"): #Şahın alta doğru ilerlemesi için
                moves.append(Adım((r,c),(r+1,c),self.board))
            if r+1 <= 9 and c+1 <=9 and (self.board[r+1][c+1]== "--" or self.board[r+1][c+1][0]=="s"): #Şahın sag alta 
                moves.append(Adım((r,c),(r+1,c+1),self.board))
            if r+1 <= 9 and c-1>= 0 and (self.board[r+1][c-1]== "--" or self.board[r+1][c-1][0]=="s"): #Şahın sol alta
                moves.append(Adım((r,c),(r+1,c-1),self.board))
            if r <= 9 and c-1 >=0 and (self.board[r][c-1]== "--" or self.board[r][c-1][0]=="s"): #sola 
                moves.append(Adım((r,c),(r,c-1),self.board))
            if r <= 9 and c+1 <=9 and (self.board[r][c+1]== "--" or self.board[r][c+1][0]=="s"): #sağa
                moves.append(Adım((r,c),(r,c+1),self.board))
            if r-1 >= 0 and (self.board[r-1][c]== "--" or self.board[r-1][c][0]=="s"): #Şahın düz ilerlerlemesi için
                moves.append(Adım((r,c),(r-1,c),self.board))
            if r-1 >= 0 and c-1 >=0 and (self.board[r-1][c-1]== "--" or self.board[r-1][c-1][0]=="s"): #Şahın ileri sola gitmesi için
                moves.append(Adım((r,c),(r-1,c-1),self.board))
            if r-1 >= 0 and c+1 <=9 and (self.board[r-1][c+1]== "--" or self.board[r-1][c+1][0]=="s"): #Şahın ileri sağa gitmesi için
                moves.append(Adım((r,c),(r-1,c+1),self.board))
                 
        
        else: #siyah hamlesi için
            if r+1 <= 9 and (self.board[r+1][c]== "--" or self.board[r+1][c][0]=="b"): #Şahın alta doğru ilerlemesi için
                moves.append(Adım((r,c),(r+1,c),self.board))
            if r+1 <= 9 and c+1 <=9 and (self.board[r+1][c+1]== "--" or self.board[r+1][c+1][0]=="b"): #Şahın sag alta 
                moves.append(Adım((r,c),(r+1,c+1),self.board))
            if r+1 <= 9 and c-1>= 0 and (self.board[r+1][c-1]== "--" or self.board[r+1][c-1][0]=="b"): #Şahın sol alta
                moves.append(Adım((r,c),(r+1,c-1),self.board))
            if r <= 9 and c-1 >=0 and (self.board[r][c-1]== "--" or self.board[r][c-1][0]=="b"): #sola 
                moves.append(Adım((r,c),(r,c-1),self.board))
            if r <= 9 and c+1 <=9 and (self.board[r][c+1]== "--" or self.board[r][c+1][0]=="b"): #sağa
                moves.append(Adım((r,c),(r,c+1),self.board))
            if r-1 >= 0 and (self.board[r-1][c]== "--" or self.board[r-1][c][0]=="b"): #Şahın düz ilerlerlemesi için
                moves.append(Adım((r,c),(r-1,c),self.board))
            if r-1 >= 0 and c-1 >=0 and (self.board[r-1][c-1]== "--" or self.board[r-1][c-1][0]=="b"): #Şahın ileri sola gitmesi için
                moves.append(Adım((r,c),(r-1,c-1),self.board))
            if r-1 >= 0 and c+1 <=9 and (self.board[r-1][c+1]== "--" or self.board[r-1][c+1][0]=="b"): #Şahın ileri sağa gitmesi için
                moves.append(Adım((r,c),(r-1,c+1),self.board))

                
class Adım():
    # Maps keys to values
    # key : values
    rankstoRows = {"1": 9, "2":8 , "3": 7, "4": 6, "5": 5, "6": 4, "7": 3, "8":2 , "9":1, "10":0}
    rowsToRanks = {v: k for k, v in rankstoRows.items()}
    rankstoCols = {"a": 0, "b": 1,"c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "j":8,"k":9}
    colsToFiles = {v: k for k, v in rankstoCols.items()} 

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000+self.startCol *100+self.endRow * 10+self.endCol #benzersiz hamle kodu elde etmek için
        print(self.moveID)
    
    def __eq__(self, other):
        if isinstance(other,Adım):
            return self.moveID == other.moveID
        return False 

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]