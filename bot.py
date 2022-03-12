import random
import Tahta

gs = Tahta.GameState()

'''
1)önce kendi hamlelerini yapıcak yaptıgı hamlenin puan değeri olucak
2)rakip hamle yapıcak bu hamleye göre puan değeri azalıcak
3) tekrar hamle yapıcak tekrar puan kazanıcak
4)tekrar rakip hamle yapıcak tekrar puan kaybedicek
5)bu hamleler sonunda en iyi yola giden 1.hamleyi yapıcak
 
'''

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

'''
def yoket(turn):
    move= []
    if turn=="b":
        for r in range(0,10):
            for c in range(0,10):
                if gs.board[r][c][0] == "s" and gs.board[r][c][1] != "S":
                    sqselected = (r,c)
                    move.append(sqselected)
        return move[random.randint(0,len(move)-1)]

    else:
        for r in range(0,10):
            for c in range(0,10):
                if gs.board[r][c][0] == "b" and gs.board[r][c][1] != "S":
                    sqselected = (r,c)
                    move.append(sqselected)
        return move[random.randint(0,len(move)-1)]
                
'''
