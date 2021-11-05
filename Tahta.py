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