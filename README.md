# PythonBattleship
A simple python game of battleship.


## Gameplay
First, you will have to set your own board. To do this, enter a coordinate on the grid in the form capital letter and number (A10, C4, etc) 
which should range from A-J and 1-10. Then you will be prompted to enter a second coordinate which will be the end point of your ship 
(which should also be within the same bounds. Keep in mind that a ship can have length 1-5, but you can only have one ship of each length. 
In addition, your ships can only be horizontal or vertical and cannot intersect with another ship. Once you have entered 5 valid ships, 
the computer will generate its board randomly. A demonstration of setting your board:



https://user-images.githubusercontent.com/68386426/186020352-0f564440-5962-4856-b9f8-2a7b526418d0.mp4



You get the first turn, and so you enter a coordinate (on the board and one that has not already been guessed) which you want to attack in 
the typical letter-number form. The value (ship or ocean) at that spot will then be revealed. Then it is the computer’s turn. A coordinate on 
your board will be guessed and revealed. This cycle repeats until one of you has guessed all the other’s ships. A sped-up gameplay walkthrough:



https://user-images.githubusercontent.com/68386426/186020474-21e45020-4c30-4ab0-9704-99871803d973.mp4



## Symbols
For the player’s board, an asterisk will represent where a ship is, a blank space where it is not. A “O” will represent a spot where 
the computer has attacked where there was no ship, a “X” where there was. For the computer’s board, it will appear blank to the player, 
as the player will not know what is at each coordinate. A spot where the player has attacked that a ship is at will be indicated by 
an asterix, and a miss will be an “O”.


## Installing/Executing Program
In order to run this game:

-Click the green 'Code' button at the top right on the main page of the repository, and then download the zip file.

-Open the folder with all three files (Board.py, Ship.py, GameManager.py) in whichever IDE you use. Make sure all 3 files are in the same folder.

-Run the GameManager.py file and the game will appear (and take input) in the console window. 

You will now be playing against the computer in a game of battleship where your goal is to destroy all your enemy’s ships before they destroy yours. 

