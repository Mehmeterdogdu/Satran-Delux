from os import X_OK, pipe


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
        self.checkMate = False
        self.staleMate = False
        self.pins = []
        self.checks = []


      

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol]= move.pieceMoved
        self.moveLog.append(move) #log the move şuanda boş 
        self.whiteToMove = not self.whiteToMove #oyuncu değişmek için
        if self.whiteToMove:
            print("sıra beyazda")
        else:
            print("sora siyahta")
        if move.pieceMoved == "bS":
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == "sS":
            self.blackKingLocation = (move.endRow,move.endCol)
            
        
    
    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #turu diğer oyuncuya geçirmek için
            if self.whiteToMove:
                print("sıra beyazda")
            else:
                print("sora siyahta")
            if move.pieceMoved == "bS":
                self.whiteKingLocation = (move.startRow,move.startCol)
            elif move.pieceMoved == "sS":
                self.blackKingLocation = (move.startRow,move.startCol)

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
                    for i in range(1,10):
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

        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
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
            for i in range(1,10):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 10 and 0<= endCol < 10:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1]!= "S":
                        if possiblePin == ():
                            possiblePin = (endRow,endCol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if(0 <=j <=3 and type == "K") or \
                            (4 <= j <= 7 and type == "F") or \
                            (i == 1 and type == "P" and ((enemyColor =="b" and 6<=j<=7) or (enemyColor== "s" and 4<= j <= 5))) or \
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
        vezirmove = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for v in vezirmove:
            endRow = startRow + v[0]
            endCol = startCol + v[1]
            if 0 <= endRow <10 and 0 <= endCol < 10:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "V":
                    inCheck = True
                    checks.append((endRow,endCol,v[0],v[1]))
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

    def getFilMoves(self,r,c,moves):  #Fil   #çarpma eklenicek yapamadım
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
            x = 2
            y = 2
            for i in range(1,10):
                endRow = r+d[0]*i   
                endCol = c+d[1]*i
                if endRow < 0 and 0<= endCol <10:
                    endRow = endRow*(-1)
                    if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                elif endRow >= 10 and 0<= endCol <10:
                    endRow = endRow-x
                    x=x+2
                    if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                elif 0 <= endRow <10 and endCol <0 :
                    endCol = endCol*(-1)
                    if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                elif 0 <= endRow <10 and endCol >=10 :
                    endCol = endCol-y
                    y = y+2
                    if not piecePinned or pinDirection== d or pinDirection ==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Adım((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                elif 0 <= endRow <10 and 0<= endCol <10:
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