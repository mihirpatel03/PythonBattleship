import string
from random import randint


class Board:

    def __init__(self, row, col, fill: str):
        #precondition, making sure we have a square board
        assert (row==col), "board must be a square (row = col)"

        self.row = row
        self.col = col

        #creating a 2d list with row+1 number of list objects so that they don't all change together (do not all refer to the same list)
        #using +1 elements so that the top row and leftmost column are letters/row for coordinate purposes
        self.x = [[fill for i in range(col+1)] for j in range(row+1)]

        #coordinate grid
        #making the top left element blank
        self.x[0][0] = " "
        #making the top row into letters
        for i in range(row):
            self.x[0][i+1] = string.ascii_uppercase[i]
        #making left most column into numbers
        for i in range(1,col+1):
            self.x[i][0] = i
        
        self.foundCount = 0 #how many ship spots have been discovered on this board
        self.ships = [] #stores the lengths of each ship on the board


    def printBoard(self):
        #function that will print the board in a readable form using loops. Only useful when we want to print just one board, 
        #but for the most part two boards will be printed at once using the game manager function printBoards()

        for row in self.x:
            if row[0] != 10:
                print(" ", end = "")
            for l in row:
                print(str(l), end = " | ")
            print("", end = "\n")
            print("-------------------------------------------")

    #change board function which will modify the board given a point and a value
    def changeBoard(self, a:int , b:int, c:string) :
        assert(c==" " or c=="O" or c=="*" or c == "X")
        self.x[b][a] = c

    #returns the value stored at a point
    def getValue(self, a:int, b:int) :
        return self.x[b][a]






        
        

    
