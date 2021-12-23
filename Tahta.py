from os import pipe


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
            ["bK","bA","bA","bF","bV","bS","bF","bA","bA","bK"]]
       # self.moveFunctions = {"P": self.getPiyonMoves,"K": self.getKaleMoves,"A":self.getAtMoves,"F":self.getFilMoves,"V": self.getVezirMoves,"S": self.getSahMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (9,5)
        self.blackKingLocation = (0,5)
        self.inCheck = False
        self.pins = []
        self.checks = []


      

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol]= move.pieceMoved
        self.moveLog.append(move) #log the move şuanda boş 
        self.whiteToMove = not self.whiteToMove #oyuncu değişmek için
        if move.pieceMoved == "bS":
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == "sS":
            self.whiteKingLocation = (move.endRow,move.endCol)

        
    
    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #turu diğer oyuncuya geçirmek için
            if move.pieceMoved == "bS":
                self.whiteKingLocation = (move.startRow,move.startCol)
            elif move.pieceMoved == "sS":
                self.whiteKingLocation = (move.startRow,move.startCol)

# satrançtaki yapılması uygun bütün hamleler örnek : 
   # eğer bir taş şahı tehtit ederse bu tehtidi engellemek dışındaki bütün hamleler geçersin olur.
    
    def getValidMoves(self):
        moves = []
        self.inCheck,self.pins,self.checks = self.checkForPinsAndChecks() 
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == "A":
                    validSquares = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]* i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1]== checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != "S":
                        if not (moves[i].endRow,moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getSahMoves(kingRow,kingCol,moves)
        else:
            moves = self.getAllPossibleMoves()

        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "s"
            allyColor = "b"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "b"
            allyColor = "s"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 10 and 0<= endCol < 10:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin== () :
                            possiblePin = (endRow,endCol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if(0 <=j <=3 and type == "K") or \
                            (4 <= j <= 7 and type == "F") or \
                            (i == 1 and type == "P" and ((enemyColor =="b" and 6<=j<=7) or (enemyColor== "s" and 4<=j <= 5))) or \
                            (type == "V") or (i == 1 and type == "S"):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
                # (r-2 c+3 / r-2 c-3 / r-3 c+2/ r-3 c-2 / r+2 c-3/r+2 c+3 /r+3 c-2/r+3 c+2)
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1),(-3,-2),(-3,2),(-2,-3),(-2,3),(2,-3),(2,3),(3,-2),(3,2))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow <10 and 0 <= endCol < 10:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "A":
                    inCheck = True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck,pins,checks
  
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
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection= (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: #eğer beyazın hamlesiyse
            if r-1 >= 0 and self.board[r-1][c]== "--": #eğer ilerisindeki kare boş ise
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Adım((r,c),(r-1,c),self.board))
                    if r-2>=0 and self.board[r-2][c]=="--":
                        moves.append(Adım((r,c),(r-2,c),self.board))
                        if r == 8 and self.board[r-3][c] =="--": #2 adım ilerlemesi için
                            moves.append(Adım((r,c),(r-3,c),self.board)) 

            if r-1 >= 0 and c-1 >= 0 and self.board[r-1][c-1][0] == "s":  #soldaki taşı yemek için
                if not piecePinned or pinDirection == (-1,-1):
                    moves.append(Adım((r,c),(r-1,c-1),self.board)) 
            if r-1 >= 0 and c+1 <= 7 and self.board[r-1][c+1][0] == "s":  #sağdaki taşı yemek için
                if not piecePinned or pinDirection == (-1,1):
                    moves.append(Adım((r,c),(r-1,c+1),self.board)) 
        
        else: #siyah hamlesi için
            if r+1 <= 9 and self.board[r+1][c]== "--": #eğer ilerisindeki kare boş ise
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Adım((r,c),(r+1,c),self.board))
                    if r+2<=9 and self.board[r+2][c]=="--":
                        moves.append(Adım((r,c),(r+2,c),self.board))
                        if r == 1 and self.board[r+3][c] =="--": #2 adım ilerlemesi için
                            moves.append(Adım((r,c),(r+3,c),self.board)) 
            if r+1 <= 9 and c-1 >= 0 and self.board[r+1][c-1][0] == "b":  #sağdaki taşı yemek için
                if not piecePinned or pinDirection == (1,-1):
                    moves.append(Adım((r,c),(r+1,c-1),self.board)) 
            if r+1 <= 9 and c+1 <= 7 and self.board[r+1][c+1][0] == "b":  #soldaki taşı yemek için
                if not piecePinned or pinDirection == (1,1):
                    moves.append(Adım((r,c),(r+1,c+1),self.board)) 

    def getKaleMoves(self,r,c,moves):   #kale     #1 adet kendi birimini yiyerek yoluna devam edebilir / zayıf kalırsa uygula
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection= (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != "V":
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "s" if self.whiteToMove else "b"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 10 and 0 <= endCol < 10 :
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getAtMoves(self,r,c,moves):  #At
        piecePinned = False
        pinDirection = ()
        #  r-1 c+2 / r-1 c-2 / r-2 c+1/ r-2 c-1 / r+1 c-2/r+1 c+2 /r+2 c-1/r+2 c+1
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1),(-3,-2),(-3,2),(-2,-3),(-2,3),(2,-3),(2,3),(3,-2),(3,2))
        allyColor = "b" if self.whiteToMove else "s"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c +m[1]
            if 0 <= endRow <10 and 0<= endCol <10:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: 
                        moves.append(Adım((r,c),(endRow,endCol),self.board))

    def getFilMoves(self,r,c,moves):  #Fil  
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))   #(sol üst) (sag üst) (sol alt)(sag alt)
        enemyColor = "s" if self.whiteToMove else "b"
        for d in directions:
            for i in range(1,10):
                endRow = r+d[0]*i   
                endCol = c+d[1]*i
                if 0 <= endRow <10 and 0<= endCol <10:
                    if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                elif endRow == -1 or endRow == 10:
                    t = d[0]*(-1)
                    for i in range(1,10):
                        endRow = endRow+t*i   
                        endCol = endCol+d[1]*i
                        if 0 <= endRow <10 and 0<= endCol <10:
                            if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                                endPiece = self.board[endRow][endCol]
                            if endPiece == "--":
                                moves.append(Adım((r,c),(endRow,endCol),self.board))
                            else:
                                break
                elif endCol == -1 or endCol == 10:
                    t = d[1]*(-1)
                    for i in range(1,10):
                        endRow = endRow+d[0]*i   
                        endCol = endCol+t*i
                        if 0 <= endRow <10 and 0<= endCol <10:
                            if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                                endPiece = self.board[endRow][endCol]
                            if endPiece == "--":
                                moves.append(Adım((r,c),(endRow,endCol),self.board))
                            elif endPiece[0] == enemyColor:
                                moves.append(Adım((r,c),(endRow,endCol),self.board))
                                break
                            else:
                                break

                else:
                    break






        
        solaltRakip=0
        solüstRakip=0
        sagüstRakip=0
        sagaltRakip=0
        solaltTakım=0
        solüstTakım=0
        sagüstTakım=0
        sagaltTakım=0
        #çarpma durumları için "çarpma(gittigiyön)(çarptıgıtaraf)(yeniyön)"  "sağ = 1" "sol = 2" "üst =3" "alt=4"
                #örnek çarpma13123 = sağüste giderken sağa çarparsa sol üste gider.
        carpma14413 = 0
        carpma14124 = 0
        carpma13314 = 0
        carpma13123 = 0
        carpma24423 = 0
        carpma24214 = 0
        carpma23324 = 0
        carpma23213 = 0
        karesayısı = len(self.board)
        if self.whiteToMove:
            for x in range(len(self.board)): #beyaz taşlar için

                #çarpma durumları için "çarpma(gittigiyön)(çarptıgıtaraf)(yeniyön)"  "sağ = 1" "sol = 2" "üst =3" "alt=4"
                #örnek çarpma13123
                #boş kareye adımlama            

               #SAĞ ALTA GİDERKEN ÇARPMA / SAĞ ÜSTE GİDER YADAR SOL ALTA GİDER
                        #çarptıgı kareyi iki kere eklememek için x ve azalma ve artma değerleri 1 arttırıldı. 
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x]== "--"): # sağ alta gitmek için  
                    if sagaltRakip == 0 and sagaltTakım <=1 :
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        #alta çarparsa
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)):
                        if karesayısı-azalma >= 0 and c+y <=9 and (self.board[karesayısı-azalma][c+y]== "--"): # sağ üst gitmek için (carpma14413)
                            if sagaltRakip == 0 and sagaltTakım <=1 and carpma14413 == 0:
                                moves.append(Adım((r,c),(karesayısı-azalma,c+y),self.board))
                                azalma = azalma+1
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)): 
                            if r+y <= 9 and karesayısı-azalma >=0 and (self.board[r+y][karesayısı-azalma]== "--"): # sol alta gitmek için
                                if sagaltRakip == 0 and sagaltTakım <=1 and carpma14124==0:                                    # carpma14124
                                    moves.append(Adım((r,c),(r+y,karesayısı-azalma),self.board))
                                    azalma = azalma+1
                        
                    #SAĞ ÜSTE GİDERKEN ÇARPMA / SAĞ ALTA DÖNER YADA SOL ÜSTE GİDER
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x]== "--"): # sağ üst gitmek için
                    if sagüstRakip == 0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        #üste çarparsa
                if r-x == 0:
                    artma = 1
                    for y in range(x+1,len(self.board)):
                        if 0+artma <= 9 and c+y <=9 and (self.board[0+artma][c+y]== "--"): # sağ alta gitmek için
                            if sagüstRakip == 0 and sagüstTakım <=1 and carpma13314==0 :
                                moves.append(Adım((r,c),(0+artma,c+y),self.board))              #carpma13314
                                artma = artma+1
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 2    
                    for y in range(x+1,karesayısı):
                        if r-y>=0 and karesayısı-azalma >=0 and (self.board[r-y][karesayısı-azalma]== "--"):
                            if sagüstRakip == 0 and sagüstTakım <=1 and carpma13123==0:
                                moves.append(Adım((r,c),(r-y,karesayısı-azalma),self.board))  #sol üste devam  #carpma13123
                                azalma = azalma+1
                        

                        #sola alta giderken çarpma durumu

                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x]== "--"): # sol alta gitmek için
                    if solaltRakip == 0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        #alta çarparsa
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,karesayısı):
                        if karesayısı-azalma>=0 and c-y>=0 and (self.board[karesayısı-azalma][c-y]=="--"):
                            if solaltRakip == 0 and solaltTakım <=1 and carpma24423==0:
                                moves.append(Adım((r,c),(karesayısı-azalma,c-y),self.board))       # sol üst gitmek için
                                azalma= azalma+1                                                    #carpma24423
                        #sola çarparsa
                if c-x == 0:
                    arttırma = 1
                    for y in range(x+1,karesayısı):
                        if r+y <= 9 and 0+arttırma <=9 and (self.board[r+y][0+arttırma]== "--"): # sağ alta gitmek için
                            if solaltRakip == 0 and solaltTakım <=1 and carpma24214==0:
                                moves.append(Adım((r,c),(r+y,0+arttırma),self.board))                   #carpma24214
                                arttırma = arttırma +1

                #SOl üste giderken çarpma durumu

                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x]== "--"): # sol üst gitmek için
                    if solüstRakip == 0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                #üste çarpma durumu
                if r-x== 0:
                    artma = 1               #sol alta gider
                    for y in range(x+1,karesayısı):
                        if 0+artma <= 9 and c-y >=0 and (self.board[0+artma][c-y]== "--"):      #carpma23324
                            if solüstRakip == 0 and solüstTakım <=1 and carpma23324 == 0:
                                moves.append(Adım((r,c),(0+artma,c-y),self.board))
                                artma = artma+1
                #sola çarpma durumu        
                if c-x == 0:
                    artma=1
                    for y in range(x+1,karesayısı):
                        if r-y >= 0 and 0+artma <=9 and (self.board[r-y][0+artma]== "--"): # sağ üst gitmek için
                            if solüstRakip == 0 and solüstTakım <=1 and carpma23213 == 0:
                                moves.append(Adım((r,c),(r-y,0+artma),self.board))              #carpma23213
                                artma = artma+1                


                #dolu kareye adımlama

                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "s"): # sağ alta gitmek için
                    if sagaltRakip==0 and sagaltTakım <=1:    
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        sagaltRakip=1
                        '''
                #Alta çarparsa
                if r+x == 9:
                    azalma = 1
                    for y in range(x,len(self.board)):
                        if karesayısı-azalma >= 0 and c+y <=9 and (self.board[karesayısı-azalma][c+y][0]== "s"): # sağ üst gitmek için
                            if sagüstRakip == 0 and sagüstTakım <=1:
                                moves.append(Adım((r,c),(karesayısı-azalma,c+y),self.board))
                                azalma = azalma+1
                               
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 1
                    for y in range(x,len(self.board)): 
                        if r+y <= 9 and karesayısı-azalma >=0 and (self.board[r+y][karesayısı-azalma][0]== "s"): # sol alta gitmek için
                            if solaltRakip == 0 and solaltTakım <=1:
                                moves.append(Adım((r,c),(r+y,karesayısı-azalma),self.board))
                                azalma = azalma+1
                                 '''


                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "s"): # sağ üst gitmek için
                    if sagüstRakip==0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        sagüstRakip = 1
                #üste çarparsa
                '''
                if r-x == 0:
                    artma = 0
                    for y in range(x,len(self.board)):
                        if 0+artma <= 9 and c+y <=9 and (self.board[0+artma][c+y]==[0] == "s"): # sağ alta gitmek için
                            if sagaltRakip == 0 and sagaltTakım <=1 :
                                moves.append(Adım((r,c),(0+artma,c+y),self.board))
                                artma = artma+1
                                
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 1
                    for y in range(x,karesayısı):
                        if r-y>=0 and karesayısı-azalma >=0 and (self.board[r-y][karesayısı-azalma][0]== "s"):
                            if solüstRakip == 0 and solüstTakım <=1:
                                moves.append(Adım((r,c),(r-y,karesayısı-azalma),self.board))  #sol üste devam
                                azalma = azalma+1
                                
                '''


                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "s"): # sol alta gitmek için
                    if solaltRakip==0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        solaltRakip = 1
                '''
                if r+x == 9:
                    azalma = 1
                    for y in range(x,karesayısı):
                        if karesayısı-azalma>=0 and c-y>=0 and (self.board[karesayısı-azalma][c-y][0]=="s"):
                            if solüstRakip == 0 and solüstTakım <=1:
                                moves.append(Adım((r,c),(karesayısı-azalma,c-y),self.board))       # sol üst gitmek için
                                azalma= azalma+1 

                        #sola çarparsa
                if c-x == 0:
                    arttırma = 0
                    for y in range(x,karesayısı):
                        if r+y <= 9 and 0+arttırma <=9 and (self.board[r+y][0+arttırma][0]== "s"): # sağ alta gitmek için
                            if sagaltRakip == 0 and sagaltTakım <=1 :
                                moves.append(Adım((r,c),(r+y,0+arttırma),self.board))
                                arttırma = arttırma +1
                '''

                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "s"): # sol üst gitmek için
                    if solüstRakip==0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                        solüstRakip = 1
                        '''
                #üste çarpma durumu 
                if r-x== 0:
                    artma = 0                                                   #sol alta gider
                    for y in range(x,karesayısı):
                        if 0+artma <= 9 and c-y >=0 and (self.board[0+artma][c-y][0]== "s"):
                            if solaltRakip == 0 and solaltTakım <=1:
                                moves.append(Adım((r,c),(0+artma,c-y),self.board))
                                artma = artma+1
                #sola çarpma durumu        
                if c-x == 0:
                    artma=0
                    for y in range(x,karesayısı):
                        if r-y >= 0 and 0+artma <=9 and (self.board[r-y][0+artma][0]== "s"): # sağ üst gitmek için
                            if sagüstRakip == 0 and sagüstTakım <=1:
                                moves.append(Adım((r,c),(r-y,0+artma),self.board))
                                artma = artma+1                
                '''

                #kendi renginin üstünden adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "b"): # sağ alta gitmek için
                       sagaltTakım = sagaltTakım+1
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)):
                        if karesayısı-azalma >= 0 and c+y <=9 and (self.board[karesayısı-azalma][c+y][0]== "b" or self.board[karesayısı-azalma][c+y][0]== "s"): # sağ üst gitmek için
                            azalma = azalma+1
                            carpma14413 = 1
                if c+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)): 
                        if r+y <= 9 and karesayısı-azalma >=0 and (self.board[r+y][karesayısı-azalma][0]== "b" or self.board[r+y][karesayısı-azalma][0]== "s"): # sol alta gitmek için
                            azalma = azalma+1
                            carpma14124=1


                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "b"): # sağ üst gitmek için
                    sagüstTakım = sagüstTakım+1
                if r-x == 0:
                    artma = 1
                    for y in range(x+1,len(self.board)):
                        if 0+artma <= 9 and c+y <=9 and (self.board[0+artma][c+y][0]== "b" and self.board[0+artma][c+y][0]== "s"): # sağ alta gitmek için
                            carpma13314=1                                       #carpma13314
                            artma = artma+1
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 2    
                    for y in range(x+1,karesayısı):
                        if r-y>=0 and karesayısı-azalma >=0 and (self.board[r-y][karesayısı-azalma][0]== "b" or self.board[r-y][karesayısı-azalma][0]== "s"):
                            carpma13123= 1
                            azalma = azalma+1

                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "b"): # sol alta gitmek için
                    solaltTakım = solaltTakım+1
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,karesayısı):
                        if karesayısı-azalma>=0 and c-y>=0 and (self.board[karesayısı-azalma][c-y][0]=="b" or self.board[karesayısı-azalma][c-y][0]=="s"):
                            carpma24423=1      # sol üst gitmek için
                            azalma= azalma+1                                                    #carpma24423
                        #sola çarparsa
                if c-x == 0:
                    arttırma = 1
                    for y in range(x+1,karesayısı):
                        if r+y <= 9 and 0+arttırma <=9 and (self.board[r+y][0+arttırma][0]== "b" or self.board[r+y][0+arttırma][0]== "s"): # sağ alta gitmek için
                            carpma24214=1               #carpma24214
                            arttırma = arttırma +1

                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "b"): # sol üst gitmek için
                   solüstTakım = solüstTakım+1
                if r-x== 0:
                    artma = 1               #sol alta gider
                    for y in range(x+1,karesayısı):
                        if 0+artma <= 9 and c-y >=0 and (self.board[0+artma][c-y][0]== "b" or self.board[0+artma][c-y][0]== "s"):      #carpma23324
                            carpma23324 = 1
                            artma = artma+1
                #sola çarpma durumu        
                if c-x == 0:
                    artma=1
                    for y in range(x+1,karesayısı):
                        if r-y >= 0 and 0+artma <=9 and (self.board[r-y][0+artma][0]== "b" or self.board[r-y][0+artma][0]== "s"): # sağ üst gitmek için
                            carpma23213 = 1             #carpma23213
                            artma = artma+1  



        else:  # siyah taşlar için 
            for x in range(len(self.board)): #

                #çarpma durumları için "çarpma(gittigiyön)(çarptıgıtaraf)(yeniyön)"  "sağ = 1" "sol = 2" "üst =3" "alt=4"
                #örnek çarpma13123
                #boş kareye adımlama            

               #SAĞ ALTA GİDERKEN ÇARPMA / SAĞ ÜSTE GİDER YADAR SOL ALTA GİDER
                        #çarptıgı kareyi iki kere eklememek için x ve azalma ve artma değerleri 1 arttırıldı. 
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x]== "--"): # sağ alta gitmek için  
                    if sagaltRakip == 0 and sagaltTakım <=1 :
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        #alta çarparsa
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)):
                        if karesayısı-azalma >= 0 and c+y <=9 and (self.board[karesayısı-azalma][c+y]== "--"): # sağ üst gitmek için (carpma14413)
                            if sagaltRakip == 0 and sagaltTakım <=1 and carpma14413 == 0:
                                moves.append(Adım((r,c),(karesayısı-azalma,c+y),self.board))
                                azalma = azalma+1
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)): 
                            if r+y <= 9 and karesayısı-azalma >=0 and (self.board[r+y][karesayısı-azalma]== "--"): # sol alta gitmek için
                                if sagaltRakip == 0 and sagaltTakım <=1 and carpma14124==0:                                    # carpma14124
                                    moves.append(Adım((r,c),(r+y,karesayısı-azalma),self.board))
                                    azalma = azalma+1
                        
                    #SAĞ ÜSTE GİDERKEN ÇARPMA / SAĞ ALTA DÖNER YADA SOL ÜSTE GİDER
                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x]== "--"): # sağ üst gitmek için
                    if sagüstRakip == 0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        #üste çarparsa
                if r-x == 0:
                    artma = 1
                    for y in range(x+1,len(self.board)):
                        if 0+artma <= 9 and c+y <=9 and (self.board[0+artma][c+y]== "--"): # sağ alta gitmek için
                            if sagüstRakip == 0 and sagüstTakım <=1 and carpma13314==0 :
                                moves.append(Adım((r,c),(0+artma,c+y),self.board))              #carpma13314
                                artma = artma+1
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 2    
                    for y in range(x+1,karesayısı):
                        if r-y>=0 and karesayısı-azalma >=0 and (self.board[r-y][karesayısı-azalma]== "--"):
                            if sagüstRakip == 0 and sagüstTakım <=1 and carpma13123==0:
                                moves.append(Adım((r,c),(r-y,karesayısı-azalma),self.board))  #sol üste devam  #carpma13123
                                azalma = azalma+1
                        

                        #sola alta giderken çarpma durumu

                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x]== "--"): # sol alta gitmek için
                    if solaltRakip == 0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        #alta çarparsa
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,karesayısı):
                        if karesayısı-azalma>=0 and c-y>=0 and (self.board[karesayısı-azalma][c-y]=="--"):
                            if solaltRakip == 0 and solaltTakım <=1 and carpma24423==0:
                                moves.append(Adım((r,c),(karesayısı-azalma,c-y),self.board))       # sol üst gitmek için
                                azalma= azalma+1                                                    #carpma24423
                        #sola çarparsa
                if c-x == 0:
                    arttırma = 1
                    for y in range(x+1,karesayısı):
                        if r+y <= 9 and 0+arttırma <=9 and (self.board[r+y][0+arttırma]== "--"): # sağ alta gitmek için
                            if solaltRakip == 0 and solaltTakım <=1 and carpma24214==0:
                                moves.append(Adım((r,c),(r+y,0+arttırma),self.board))                   #carpma24214
                                arttırma = arttırma +1

                #SOl üste giderken çarpma durumu

                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x]== "--"): # sol üst gitmek için
                    if solüstRakip == 0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                #üste çarpma durumu
                if r-x== 0:
                    artma = 1               #sol alta gider
                    for y in range(x+1,karesayısı):
                        if 0+artma <= 9 and c-y >=0 and (self.board[0+artma][c-y]== "--"):      #carpma23324
                            if solüstRakip == 0 and solüstTakım <=1 and carpma23324 == 0:
                                moves.append(Adım((r,c),(0+artma,c-y),self.board))
                                artma = artma+1
                #sola çarpma durumu        
                if c-x == 0:
                    artma=1
                    for y in range(x+1,karesayısı):
                        if r-y >= 0 and 0+artma <=9 and (self.board[r-y][0+artma]== "--"): # sağ üst gitmek için
                            if solüstRakip == 0 and solüstTakım <=1 and carpma23213 == 0:
                                moves.append(Adım((r,c),(r-y,0+artma),self.board))              #carpma23213
                                artma = artma+1                


                #dolu kareye adımlama

                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "b"): # sağ alta gitmek için
                    if sagaltRakip==0 and sagaltTakım <=1:    
                        moves.append(Adım((r,c),(r+x,c+x),self.board))
                        sagaltRakip=1
                        '''
                #Alta çarparsa
                if r+x == 9:
                    azalma = 1
                    for y in range(x,len(self.board)):
                        if karesayısı-azalma >= 0 and c+y <=9 and (self.board[karesayısı-azalma][c+y][0]== "b"): # sağ üst gitmek için
                            if sagüstRakip == 0 and sagüstTakım <=1:
                                moves.append(Adım((r,c),(karesayısı-azalma,c+y),self.board))
                                azalma = azalma+1
                               
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 1
                    for y in range(x,len(self.board)): 
                        if r+y <= 9 and karesayısı-azalma >=0 and (self.board[r+y][karesayısı-azalma][0]== "b"): # sol alta gitmek için
                            if solaltRakip == 0 and solaltTakım <=1:
                                moves.append(Adım((r,c),(r+y,karesayısı-azalma),self.board))
                                azalma = azalma+1
                                 '''


                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "b"): # sağ üst gitmek için
                    if sagüstRakip==0 and sagüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c+x),self.board))
                        sagüstRakip = 1
                #üste çarparsa
                '''
                if r-x == 0:
                    artma = 0
                    for y in range(x,len(self.board)):
                        if 0+artma <= 9 and c+y <=9 and (self.board[0+artma][c+y]==[0] == "b"): # sağ alta gitmek için
                            if sagaltRakip == 0 and sagaltTakım <=1 :
                                moves.append(Adım((r,c),(0+artma,c+y),self.board))
                                artma = artma+1
                                
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 1
                    for y in range(x,karesayısı):
                        if r-y>=0 and karesayısı-azalma >=0 and (self.board[r-y][karesayısı-azalma][0]== "b"):
                            if solüstRakip == 0 and solüstTakım <=1:
                                moves.append(Adım((r,c),(r-y,karesayısı-azalma),self.board))  #sol üste devam
                                azalma = azalma+1
                                
                '''


                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "b"): # sol alta gitmek için
                    if solaltRakip==0 and solaltTakım <=1:
                        moves.append(Adım((r,c),(r+x,c-x),self.board))
                        solaltRakip = 1
                '''
                if r+x == 9:
                    azalma = 1
                    for y in range(x,karesayısı):
                        if karesayısı-azalma>=0 and c-y>=0 and (self.board[karesayısı-azalma][c-y][0]=="b"):
                            if solüstRakip == 0 and solüstTakım <=1:
                                moves.append(Adım((r,c),(karesayısı-azalma,c-y),self.board))       # sol üst gitmek için
                                azalma= azalma+1 

                        #sola çarparsa
                if c-x == 0:
                    arttırma = 0
                    for y in range(x,karesayısı):
                        if r+y <= 9 and 0+arttırma <=9 and (self.board[r+y][0+arttırma][0]== "b"): # sağ alta gitmek için
                            if sagaltRakip == 0 and sagaltTakım <=1 :
                                moves.append(Adım((r,c),(r+y,0+arttırma),self.board))
                                arttırma = arttırma +1
                '''

                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "b"): # sol üst gitmek için
                    if solüstRakip==0 and solüstTakım <=1:
                        moves.append(Adım((r,c),(r-x,c-x),self.board))
                        solüstRakip = 1
                        '''
                #üste çarpma durumu 
                if r-x== 0:
                    artma = 0                                                   #sol alta gider
                    for y in range(x,karesayısı):
                        if 0+artma <= 9 and c-y >=0 and (self.board[0+artma][c-y][0]== "b"):
                            if solaltRakip == 0 and solaltTakım <=1:
                                moves.append(Adım((r,c),(0+artma,c-y),self.board))
                                artma = artma+1
                #sola çarpma durumu        
                if c-x == 0:
                    artma=0
                    for y in range(x,karesayısı):
                        if r-y >= 0 and 0+artma <=9 and (self.board[r-y][0+artma][0]== "b"): # sağ üst gitmek için
                            if sagüstRakip == 0 and sagüstTakım <=1:
                                moves.append(Adım((r,c),(r-y,0+artma),self.board))
                                artma = artma+1                
                '''

                #kendi renginin üstünden adımlama
                if r+x <= 9 and c+x <=9 and (self.board[r+x][c+x][0]== "s"): # sağ alta gitmek için
                       sagaltTakım = sagaltTakım+1
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)):
                        if karesayısı-azalma >= 0 and c+y <=9 and (self.board[karesayısı-azalma][c+y][0]== "b" or self.board[karesayısı-azalma][c+y][0]== "s"): # sağ üst gitmek için
                            azalma = azalma+1
                            carpma14413 = 1
                if c+x == 9:
                    azalma = 2
                    for y in range(x+1,len(self.board)): 
                        if r+y <= 9 and karesayısı-azalma >=0 and (self.board[r+y][karesayısı-azalma][0]== "b" or self.board[r+y][karesayısı-azalma][0]== "s"): # sol alta gitmek için
                            azalma = azalma+1
                            carpma14124=1


                if r-x >= 0 and c+x <=9 and (self.board[r-x][c+x][0]== "s"): # sağ üst gitmek için
                    sagüstTakım = sagüstTakım+1
                if r-x == 0:
                    artma = 1
                    for y in range(x+1,len(self.board)):
                        if 0+artma <= 9 and c+y <=9 and (self.board[0+artma][c+y][0]== "b" and self.board[0+artma][c+y][0]== "s"): # sağ alta gitmek için
                            carpma13314=1                                       #carpma13314
                            artma = artma+1
                        #sağa çarparsa
                if c+x == 9:
                    azalma = 2    
                    for y in range(x+1,karesayısı):
                        if r-y>=0 and karesayısı-azalma >=0 and (self.board[r-y][karesayısı-azalma][0]== "b" or self.board[r-y][karesayısı-azalma][0]== "s"):
                            carpma13123= 1
                            azalma = azalma+1

                if r+x <= 9 and c-x >=0 and (self.board[r+x][c-x][0]== "s"): # sol alta gitmek için
                    solaltTakım = solaltTakım+1
                if r+x == 9:
                    azalma = 2
                    for y in range(x+1,karesayısı):
                        if karesayısı-azalma>=0 and c-y>=0 and (self.board[karesayısı-azalma][c-y][0]=="b" or self.board[karesayısı-azalma][c-y][0]=="s"):
                            carpma24423=1      # sol üst gitmek için
                            azalma= azalma+1                                                    #carpma24423
                        #sola çarparsa
                if c-x == 0:
                    arttırma = 1
                    for y in range(x+1,karesayısı):
                        if r+y <= 9 and 0+arttırma <=9 and (self.board[r+y][0+arttırma][0]== "b" or self.board[r+y][0+arttırma][0]== "s"): # sağ alta gitmek için
                            carpma24214=1               #carpma24214
                            arttırma = arttırma +1

                if r-x >= 0 and c-x >=0  and (self.board[r-x][c-x][0]== "s"): # sol üst gitmek için
                   solüstTakım = solüstTakım+1
                if r-x== 0:
                    artma = 1               #sol alta gider
                    for y in range(x+1,karesayısı):
                        if 0+artma <= 9 and c-y >=0 and (self.board[0+artma][c-y][0]== "b" or self.board[0+artma][c-y][0]== "s"):      #carpma23324
                            carpma23324 = 1
                            artma = artma+1
                #sola çarpma durumu        
                if c-x == 0:
                    artma=1
                    for y in range(x+1,karesayısı):
                        if r-y >= 0 and 0+artma <=9 and (self.board[r-y][0+artma][0]== "b" or self.board[r-y][0+artma][0]== "s"): # sağ üst gitmek için
                            carpma23213 = 1             #carpma23213
                            artma = artma+1  

    def defaultAt(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        #  r-1 c+2 / r-1 c-2 / r-2 c+1/ r-2 c-1 / r+1 c-2/r+1 c+2 /r+2 c-1/r+2 c+1
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "b" if self.whiteToMove else "s"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c +m[1]
            if 0 <= endRow <10 and 0<= endCol <10:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: 
                        moves.append(Adım((r,c),(endRow,endCol),self.board))
    def defaultFil(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "s" if self.whiteToMove else "b"
        for d in directions:
            for i in range(1,10):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow <10 and 0<= endCol <10:
                    if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break
    def getVezirMoves(self,r,c,moves):  #Vezir
        self.getKaleMoves(r,c,moves)
        self.defaultAt(r,c,moves)
        self.defaultFil(r,c,moves)
        

    def getSahMoves(self,r,c,moves):  #Sah
        rowMoves = (-1 ,-1 ,-1 , 0 , 0 , 1 , 1 , 1 )
        colMoves = (-1 , 0 , 1 , 1 , -1 ,-1 , 0 ,1 )
        allyColor = "b" if self.whiteToMove else "s"       
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 10 and 0<= endCol <10:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == "b":
                        self.whiteKingLocation= (endRow,endCol)
                    else :
                        self.blackKingLocation = (endRow,endCol)
                    inCheck,pins,checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Adım((r,c),(endRow,endCol),self.board))
                    if allyColor == "b":
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)

                
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
        self.moveID = self.startRow*1000+self.startCol *100+self.endRow * 10+self.endCol
      
    
    def __eq__(self, other):
        if isinstance(other,Adım):
            return self.moveID == other.moveID
        return False 

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]