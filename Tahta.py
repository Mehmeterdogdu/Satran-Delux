class GameState():
    def __init__(self) :
        #tahta 10x10 ve bütün liste elemanları 2 karakterli
        #ilk harfleri rengi temsil ediyor b = beyaz , s = siyah
        #ikinci harfleri hangi taş olduklarını gösteriyor K = kale, A = at, F = fil, V = Vezir, S= Şah, P = piyon, Y = yeni eklenicek taş
        # "--" boş kareler oldugunu gösteriyor.
        self.board = [
            ["bK","bA","bY","bF","bV","bS","bF","bY","bA","bK"],
            ["bP","bP","bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--"],
            ["sP","sP","sP","sP","sP","sP","sP","sP","sP","sP"],
            ["sK","sA","sY","sF","sV","sS","sF","sY","sA","sK"],
                    ]
        self.whiteToMove = True
        self.moveLog = []