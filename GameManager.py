import math
import time
from random import randint
from Board import Board
import string
import sys
sys.path.append(".")

# Board will be blank to represent places where you do not knwo what is there
# O represents a miss, and * represents a boat, will turn to X when computer hits your ship's spot


class GameManager:

    def __init__(self):
        # constructor, board size to 10x10
        self.s = 10
        # setting the player's hidden board to blank (will change when players places ships and computer starts guessing)
        self.hidden = Board(self.s, self.s, " ")
        # setting the opponent's hidden board to misses (will add in ships later)
        self.op_hidden = Board(self.s, self.s, "O")
        # opponents shown board is blank (will change with guesses)
        self.op_shown = Board(self.s, self.s, " ")

    # checks if a valid coordinate is entered into the input
    def coordinateOnBoard(self, x: int, y: int):
        # booleans to keep track of if we have found the letter coordinate and number coordinate on the board
        foundLetter = False
        foundNumber = False
        # looping through the board
        for i in range(self.s):
            # if the index we are at is the same as the letter we need to find, found letter is true (same for number)
            if (x == i+1):
                foundLetter = True
            if (y == i+1):
                foundNumber = True
        # if either is false (we haven't found one of the necessary coordinates), the coordinate is not valid
        if (foundLetter == False or foundNumber == False):
            return False
        #otherwise, true
        return True

    # gets the number corresponding to a letter (useful for coordinates written as A1). A=1, B=2, etc.
    def getLetterIdx(self, x: string):
        # start at 0, loop through the string of upper case letters
        letter_idx = 0
        for i in range(len(string.ascii_uppercase)):
            # once we have found the letter, return the index it is at
            if (x == string.ascii_uppercase[i]):
                letter_idx = i
        return letter_idx+1

    # makes sure the ship we are trying to create is valid
    def validShip(self, x1: int, y1: int, x2: int, y2: int, board: Board):
        # checking that the input coordinates are valid
        if not self.coordinateOnBoard(x1, y1) or not self.coordinateOnBoard(x2, y2):
            return False

        # checking if length of the input ship is less than 1 or greater than 5, i.e. invalid
        if (y1 == y2):
            # when y1 and y2 are equal, the distance will be the distance between x1 and x2
            dist = abs(x1-x2)
            if (dist < 0 or dist > 4):
                return False
            # checking that there is not already a ship where we want to place the new one
            for i in range(x1, x2+1):
                if board.getValue(i, y1) == "*":
                    return False

        # same logic, but now for ships going N and S (vertical)
        if (x1 == x2):
            dist = abs(y1-y2)
            if (abs(y1-y2) < 0 or abs(y1-y2) > 4):
                return False
            for i in range(y1, y2+1):
                if board.getValue(x1, i) == "*":
                    return False

        # checking if y1 and y2 are different and x1 and x2 are different, i.e. the ship is diagonal
        if (y1 != y2 and x1 != x2):
            return False

        # checking that it the length of ship is not one that is already in use (so we have one of each length)
        if dist in board.ships:
            return False

        # if all of these conditions are met, it is a valid ship
        return True

    # converts coordinates from strings to ints
    def letterToNum(self, a: string, b: string):
        # given two coordinates as strings (e.g. A1, A3), create x1, x2, y1, y2 to store those coordinates as integer points
        x1 = self.getLetterIdx(a[0])
        y1 = int(a[1:])
        x2 = self.getLetterIdx(b[0])
        y2 = int(b[1:])
        # return as a list of ints
        return [x1, y1, x2, y2]

    # creates a ship on the board
    def createShip(self, x1: int, y1: int, x2: int, y2: int, board: Board):
        # precondition that the ship we are about to create is valid
        assert self.validShip(x1, y1, x2, y2, board)

        # If the ship is a vertical ship...
        if (x1 == x2):
            # calculate distance between the y values (length of the ship)
            dist = abs(y1-y2)
            # for every point on the ship, change the board to the ship ("*")
            # if the player for some reason entered the coordinate backwards...
            # ...(A3 as the start and A1 as the end, loop backwards to account for this)
            if (y2 < y1):
                for i in range(0, -dist-1, -1):
                    board.changeBoard(x1, y1+i, "*")
            else:
                for i in range(dist+1):
                    board.changeBoard(x1, y1+i, "*")
        # same thing as vertical ship but now adapted for horizontal
        elif (y1 == y2):
            dist = abs(x1-x2)
            if (x2 < x1):
                for i in range(0, -dist-1, -1):
                    board.changeBoard(x1+i, y1, "*")
            else:
                for i in range(dist+1):
                    board.changeBoard(x1+i, y1, "*")

        # add the distance of the ship we just made to the ships list so we can keep track of the length of
        # every ship on the board, so that we have one of each type
        board.ships.append(dist)

    # modifies the shown board when a player attacks a spot
    def strike(self, a: string, hiddenBoard: Board, shownBoard: Board):
        # given a string coordinate, create a point from it
        x = self.getLetterIdx(a[0])
        y = int(a[1:])
        # make sure the given coordinate is a valid coordinate
        assert self.coordinateOnBoard(
            x, y) == True, "please enter a valid coordinate"

        # get the value stored at the position on the hidden board
        z = hiddenBoard.getValue(x, y)
        # if that position we are about to attack is in fact a ship, add 1 to the count of...
        # ...how many spots we have attacked that are ships. This is how we know when the game is over.
        if z == "*":
            hiddenBoard.foundCount += 1
        # if the hidden board is the players board, we follow different rules than the opponent's board
        if hiddenBoard == self.hidden:
            # if the computer attacks an empty spot, show that they missed by making it an "O"
            if z == " ":
                hiddenBoard.changeBoard(x, y, "O")
            # if they attacked a place where we have a ship (which will already be displayed for the player)...
            # ...make that spot into an "X" to show that they successfully attacked
            elif z == "*":
                hiddenBoard.changeBoard(x, y, "X")
        # otherwise, when the player is attacking, just modify the shown board to match that value
        else:
            shownBoard.changeBoard(x, y, z)

    # creates random coordinates to generate the computer's board
    def randomCoordinates(self, board: Board):
        # ships list to keep track of the lengths of the ships on the board so far
        # (different from the one in createShip because if it were the same it would get modified twice)
        ships = []
        # performing this loop 5 times to create 5 ships
        for i in range(5):
            # found is True once we have created valid coordinates for a ship
            found = False
            while found == False:
                # initially just randomize the start and end coordinates of the ship on the board
                x1, y1, x2, y2 = randint(0, 10), randint(
                    0, 10), randint(0, 10), randint(0, 10)
                # p and q are just so that we can calculate the length of the ship using math.dist()
                p = [x1, y1]
                q = [x2, y2]
                # as long as we don't have a valid ship, keep randomizing the start and end point (will end once we have a valid ship)
                while not self.validShip(x1, y1, x2, y2, board):
                    x1, y1 = randint(0, 10), randint(0, 10)
                    x2, y2 = randint(0, 10), randint(0, 10)
                # recalculate p and q
                p = [x1, y1]
                q = [x2, y2]
                # if the new length is not already in use...
                if math.dist(p, q) not in ships:
                    # add it to the ships list
                    ships.append(math.dist(p, q))
                    # create a ship with these coordinates
                    self.createShip(x1, y1, x2, y2, board)
                    # break out of the big while loop
                    found = True
                # if this previous condition is not met (i.e. we have a valid ship but the length is already in use),
                # it will just start the whole process again until it finds new valid coordinates, checks length, etc.

    # prints two boards next too eachother for viewing purposes
    def printBoards(self, playerBoard: Board, enemyBoard: Board):
        # most of this stuff is just creating the board, changing if print goes to a new line or not, adding in column and row grids, etc.
        print("")
        print("                 YOUR BOARD                          |||                            ENEMY BOARD")
        print("------------------------------------------------------------------------------------------------------------")
        for row in range(playerBoard.row+1):
            if playerBoard.getValue(0, row) != 10:
                print(" ", end="")

            for i in range(playerBoard.col+1):
                print(str(playerBoard.getValue(i, row)), end=" | ")

            print("", end="        |||        ")

            if enemyBoard.getValue(0, row) != 10:
                print(" ", end="")

            for j in range(enemyBoard.col+1):
                print(str(enemyBoard.getValue(j, row)), end=" | ")
            print("", end="\n")
            print("--------------------------------------------         |||         -------------------------------------------")


# creating game manager class
g = GameManager()

# creating random coordinates for the computer's hidden board
g.randomCoordinates(g.op_hidden)

# this will tell you where the opponents ships are (mainly for testing, but could be used for cheating)
# g.op_hidden.printBoard()

# print the two boards side by side initially
g.printBoards(g.hidden, g.op_shown)

# player setting their board
print("set your board!")
# count ships the player has created on their board, so that they only make 5
shipCount = 0
while shipCount < 5:
    # inputting start and end coordinates of the ship
    s1 = str(input("select a beginning coordinate for your ship:  "))
    s2 = str(input("select an end coordinate for your ship:  "))
    # creating a list that is the int versions of these two coordinates
    newCoords = g.letterToNum(s1, s2)
    # as long as these coordinates do not form a valid ship, keep asking them to reinput the coordinates
    while not g.validShip(newCoords[0], newCoords[1], newCoords[2], newCoords[3], g.hidden):
        s1 = str(input("select a beginning coordinate for your ship:  "))
        s2 = str(input("select an end coordinate for your ship:  "))
        newCoords = g.letterToNum(s1, s2)
    # once the coordinates are valid, create a ship with these coordinates
    g.createShip(newCoords[0], newCoords[1],
                 newCoords[2], newCoords[3], g.hidden)
    # print the updated board
    g.printBoards(g.hidden, g.op_shown)
    # add one to the ship tally
    shipCount += 1

# as long as neither player has lost all their ships (15 because 1+2+3+4+5)
while (g.hidden.foundCount < 15 and g.op_hidden.foundCount < 15):
    # PLAYER TURN
    # ask the player for an input coordinate to attack
    s = str(input("Your turn -- select a coordinate to attack:  "))
    x = g.getLetterIdx(s[0])
    if s[1] in "1234567890":
        y = int(s[1])
    else:
        y = 11
    # keep asking for an input coordinate if the one given is not in the form of capital letter, int (e.g. A1), not on the board, or already attacked
    while (s[0] not in string.ascii_uppercase or not g.coordinateOnBoard(x, y) or g.op_shown.getValue(x, y) == "*" or g.op_shown.getValue(x, y) == "O"):
        s = str(input("Your turn -- select a coordinate to attack:  "))
        # splitting up the coordinate into two int coordinates
        x = g.getLetterIdx(s[0])
        if s[1] in "1234567890":
            y = int(s[1])
        else:
            y = 11

    #    s = str(input("Your turn -- select a coordinate to attack:  "))
    x = g.getLetterIdx(s[0])
    y = int(s[1])
    # after those two while loops, we should have a valid coordinate on the board that has not been attacked yet
    # now actually attack that coordinate, modifying the shown board to reflect what is at that position in the hidden board
    g.strike(s, g.op_hidden, g.op_shown)
    # formatting/readability
    print("-----------------------")
    # print the updated boards after this move
    g.printBoards(g.hidden, g.op_shown)

    # COMPUTER TURN
    print("Computer's turn")
    # add a delay so that it gives the player time to view updates/think, make it seem like the opponent is thinking
    time.sleep(3)
    # generate a random coordinate for the computer to attack the player's board with
    x = randint(0, 9)
    y = randint(1, 10)
    x = string.ascii_uppercase[x]
    s = x + str(y)
    # attack that coordinate
    g.strike(s, g.hidden, g.op_shown)
    # readability/formatting
    print("-----------------------")
    # print the updates to the board
    g.printBoards(g.hidden, g.op_shown)
    # this loop will keep going, alternating turns, until one player has found all the other's ships

# once we are out of that while loop someone has lost all their ships
# if the player has lost all their ships, print they lost
if g.hidden.foundCount == 15:
    print("Oh no, you lost! Better luck next time.")
# otherwise the player won!
else:
    print("Congratulations! You sunk all the enemy battleships")
