import random
import Tahta

gs = Tahta.GameState()


def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

def findBestMove():
    return

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
                
        
