
from Board import Board

class Ship:
    def init(self, length: int, dir: int, x: int, y:int, board: Board) :
        assert dir == 0, dir == 1
        if dir == 0:
            for i in range(length):
                board[x+i][y] = "--"
        else: 
            for i in range(length):
                board[x][y+i] = "|"


