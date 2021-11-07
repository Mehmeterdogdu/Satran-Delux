class GameState():
    def __init__(self) :
        #tahta 10x10 ve bütün liste elemanları 2 karakterli
        #ilk harfleri rengi temsil ediyor b = beyaz , s = siyah
        #ikinci harfleri hangi taş olduklarını gösteriyor K = kale, A = at, F = fil, V = Vezir, S= Şah, P = piyon, Y = yeni eklenicek taş
        # "--" boş kareler oldugunu gösteriyor.
        self.board = [
            ["bK","bA","bA","bF","bV","bS","bF","bA","bA","bK"],
            ["bP","bP","bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["sP","sP","sP","sP","sP","sP","sP","sP","sP","sP"],
            ["sK","sA","sA","sF","sV","sS","sF","sA","sA","sK"],
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
    
   # def getValidMoves(self):
    #    return self.getAllPossibleMoves()

    #satrançta yapılabilen tün hamleler
    '''
    def getAllPossibleMoves(self):
        moves = [Adım((8,4),(6,4),self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "b" and self.whiteToMove) and (turn == "s" and not self.whiteToMove):
                    piece = self.board[r][c][1]
            #isimlerine göre taşların yapabiliceği hamleler
                    if piece == "P":
                        self.getPiyonMoves(r,c,moves) #piyon hamleleri
                    elif piece == "K":
                        self.getKaleMoves(r,c,moves) #Kale hareketleri
            return moves
    #taş hareketleri

    def getPiyonMoves(self, r,c,moves): #piyon
        pass

    def getKaleMoves(self,r,c,moves):   #kale
        pass
        '''
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