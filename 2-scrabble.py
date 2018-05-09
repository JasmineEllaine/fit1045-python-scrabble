from sys import stdin
from functools import reduce
import math
import sys
import random
import copy

TILES_USED = 0  # records how many tiles have been returned to user
CELL_WIDTH = 3  # cell width of the scrabble board
SHUFFLE = False  # records whether to shuffle the tiles or not
# inserts tiles into myTiles

def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7 and TILES_USED < len(Tiles):
        myTiles.append(Tiles[TILES_USED])
        TILES_USED += 1
# prints tiles and their scores

def printTiles(myTiles):
    tiles = ""
    scores = ""
    for letter in myTiles:
        tiles += letter + "  "
        thisScore = getScore(letter)
        if thisScore > 9:
            scores += str(thisScore) + " "
        else:
            scores += str(thisScore) + "  "
    print("\nTiles : " + tiles)
    print("Scores: " + scores)
# gets the score of a letter

def getScore(letter):
    for item in Scores:
        if item[0] == letter:
            return item[1]
# initialize n x n Board with empty strings

def initializeBoard(n):
    Board = []
    for _ in range(n):
        row = []
        for _ in range(n):
            row.append("")
        Board.append(row)
    return Board
# put character t before and after the string s such that the total length
# of the string s is CELL_WIDTH.

def getString(s, t):
    global CELL_WIDTH
    s = str(s)
    rem = CELL_WIDTH - len(s)
    rem = rem // 2
    s = t * rem + s
    rem = CELL_WIDTH - len(s)
    s = s + t * rem
    return s
# print the Board on screen

def printBoard(Board):
    global CELL_WIDTH
    print("\nBoard:")
    #spaces = CELL_WIDTH * " "
    board_str = "  |" + "|".join(getString(item, " ")
                                 for item in range(len(Board))) + "|"
    line1 = "--|" + "|".join(getString("", "-")
                             for item in range(len(Board))) + "|"
    print(board_str)
    print(line1)
    for i in range(len(Board)):
        row = str(i) + " " * (2 - len(str(i))) + "|"
        for j in range(len(Board)):
            row += getString(Board[i][j], " ") + "|"
        print(row)
        print(line1)
    print()

scoresFile = open('scores.txt')
tilesFile = open('tiles.txt')
# read scores from scores.txt and insert in the list Scores
Scores = []
for line in scoresFile:
    line = line.split()
    letter = line[0]
    score = int(line[1])
    Scores.append([letter, score])
scoresFile.close()
# read tiles from tiles.txt and insert in the list Tiles
Tiles = []
for line in tilesFile:
    line = line.strip()
    Tiles.append(line)
tilesFile.close()
# decide whether to return random tiles
# rand = input("Do you want to use random tiles (enter Y or N): ")
rand = "N"
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
if SHUFFLE:
    random.shuffle(Tiles)
# validBoardSize = False
# while not validBoardSize:
#     BOARD_SIZE = input("Enter board size (a number between 5 to 15): ")
#     if BOARD_SIZE.isdigit():
#         BOARD_SIZE = int(BOARD_SIZE)
#         if BOARD_SIZE >= 5 and BOARD_SIZE <= 15:
#             validBoardSize = True
#         else:
#             print("Your number is not within the range.\n")
#     else:
#         print("Are you a little tipsy? I asked you to enter a number.\n")
BOARD_SIZE = 7
Board = initializeBoard(BOARD_SIZE)
printBoard(Board)
myTiles = []
getTiles(myTiles)
printTiles(myTiles)
########################################################################
# Write your code below this
########################################################################
# functions here

def makeDictionary(dictionaryName):
    """ Creates a list out of a file with each line being an item in 
       the list.
    Args:   
        dictionaryName (str): name of the file to be turned into a list
                              must contain file extension
    Returns:
        (list): list containing all each line of a file
    """
    dictionaryFile = open(dictionaryName)
    return [dictionaryWord.strip() for dictionaryWord in dictionaryFile]

def inDictionary(word, dictionary):
    """ Checks if a word is in a given dictionary
    Args:   
        word (str): any string of characters
        dictionary (list): list of dictionary words
    Returns:
        True (bool): if userWord can be found in dictionary
        False (bool): otherwise
    """
    try:
        word = word.upper()
        return word in dictionary
    except Exception:
        return False

def validLocationFormat(location):
    """ Checks if the format of the location is valid
    Args:   
        location (str): location to be checked
    Returns:
        True (bool): if format is valid
        False (bool): if format is invalid
    """
    # checks if location is in r:c:d format
    location = location.split(":")
    if len(location) == 3:
        # checks if d is either H or V
        d = ["H", "V"]
        
        if location[2] in d:
            # checks if r and c are integers
            try:
                rc = [number for number in location[:2] if int(
                    number) >= 0 and int(number) < BOARD_SIZE]
            except Exception:
                return False
            else:
                if len(rc) == 2:
                    return True
    return False

def validFirstLocation(location, boardsize):
    """ Checks if location is valid for the first turn
    Args:   
        location (list): valid location
        boardsize (int): size of the board
    Returns:
        True (bool): if move is valid for the first turn
        False (bool): if move is invalid for the first turn
    """
    # checks if r == c
    if location[0] == location[1]:
        # checks if centered
        if location[0] == boardsize // 2:
            return True
    return False

def validLocation(r, c, d, boardsize, word):
    """ Checks if location is valid 
    Args:   
        location (list): valid location
        boardsize (int): size of the board
        word (str): user picked word
    Returns:
        True (bool): if move is valid 
        False (bool): if move is invalid 
    """
    try:
        if d == 'H':
            if (c + len(word)) < boardsize:
                return True
        if d == 'V':
            if (r + len(word)) < boardsize:
                return True
    except Exception:
        return False
def removeLetters():
    for tile in userWord:
        myTiles.remove(tile)
def correctTiles(word, tiles):
    """Checks if a word can be made using the a set of tile
    Args:   
        word (str): word all uppercase
        tiles (list): list containing tiles in uppercase
    Returns:
        True (bool): if word can be made using the given tiles
        False (bool): otherwise
    """    
    return set(word).issubset(set(myTiles))

def transpose(board):
    return list(map(list, list(zip(*board))))

def validMove(r, c, d, word, tiles):
    """Checks if a word can be made using the a set of tile
    Args:   
        word (str): word all uppercase
        tiles (list): list containing tiles in uppercase
    Returns:
        True (bool): if word can be made using the given tilzes
        False (bool): otherwise
    """
  
    if d == 'H':
        boardSlice = Board[r][c:c + len(word)]
    elif d == 'V':
        board = transpose(Board)
        boardSlice = board[c][r:r + len(word)]
        
    word = list(word)

    # checks if moves/changes a tile on board
    for i, v in enumerate(boardSlice):
        if v != "":
            if v != word[i]:
                return False
    # checks if boardtiles can be used to make word
    usedTiles = [tile for tile in word if tile not in boardSlice]

    # checks if uses at least one tile from board
    if len(usedTiles) == len(word):
        return False

    # eat some letterDonuts
    for tile in usedTiles:
        myTiles.remove(tile)

    # checks if myTiles can be used to make remaining words
    usedTiles = [tile for tile in usedTiles if tile not in myTiles]
    if usedTiles == []:
        return True
    return False

def placeWordOnRow(word, columnIndex, row):
    """ Places word on a list starting at index columnIndex
    Args:   
        word (str): uppercase word
        columnIndex (int): index where first letter of word is to be put
        row (list): row where word will be put
    Returns: 
        row (list): list where each item is a letter
            ["", "", "C", "A", "T", "", ""]
    """
    for letterIndex in range(len(word)):
        row[letterIndex + columnIndex] = userWord[letterIndex]
    return row

def placeWordOnBoard(r, c, d, word, board):
    # place normally if H
    if d == "H":
        board[r] = placeWordOnRow(word, c, board[r])
    # transpose board first if V
    elif d == "V":
        board = list(map(list, list(zip(*board))))
        board[c] = placeWordOnRow(word, r, board[c])
        board = list(map(list, list(zip(*board))))
    return board

def getWordScore(word):
    """Calculates the total score of a given word
    Args:   
        word (str): word to be ccalculated
    Returns:
        (int): total score of the word
    """
    return reduce((lambda x, y: x + y), [getScore(letter) for letter in userWord])

# scrabble code
englishDict = makeDictionary("dictionary.txt")

# game data
turnNo = 1
totalScore = 0

# keeps asking for move while game isnt finished
endGame = False
while not endGame:
    # ask for word
    userWord = input("\nEnter a word: ")

    # makes word uppercase if valid
    # asks for another if invalid
    if not inDictionary(userWord, englishDict):
        print("Invalid word.")
        continue

    userWord = userWord.upper()

    # ask for location
    location = input("Enter a location: ")

    # formats location if valid
    # asks for another if invalid
    if not validLocationFormat(location):
        print("Invalid location.")
        continue

    location = location.split(":")
    location = list(map(int, location[:2])) + [location[2]]

    r = location[0]
    c = location[1]
    d = location[2]

    # copies necessary data for finding best move later
    boardCopy = copy.deepcopy(Board)
    myTilesCopy = copy.deepcopy(myTiles)
    # first turn conditions
    # checks if location is centered
    # asks for another location if word not centered
    if turnNo == 1:
        if not validFirstLocation(location, BOARD_SIZE):
            print("Invalid first move location.")
            continue

        # checks if myTiles can make userWord
        # asks for another if not
        if not correctTiles(userWord, myTiles):
            print("Word can't be made with given tiles.")
            continue

        # checks if word can fit the board
        # asks for another if not
        if len(userWord) > BOARD_SIZE // 2 + 1:
            print("Word outside board dimensions.")
            continue

        # places word on board
        Board = placeWordOnBoard(r, c, d, userWord, Board)
        removeLetters()

    # all other turns
    else:
        # checks if word can fit the board
        # asks for another if not
        if not validLocation(r, c, d, BOARD_SIZE, userWord):
            print("Word outside board dimensions.")
            continue

        # checks if move is valid
        if not validMove(r, c, d, userWord, myTiles):
            print("Invalid move.")
            continue

        # places word on board
        Board = placeWordOnBoard(r, c, d, userWord, Board)

    wordScore = getWordScore(userWord)
    totalScore += wordScore

    print("Your score in this move:", wordScore)
    print("Your total score:", totalScore)
    printBoard(Board)

    #updateTiles(r, c, d, userWord)
    getTiles(myTiles)
    printTiles(myTiles)
    turnNo += 1

"""
4. The move must not change or relocate any
    existing tile on the board.
make dictionary
while game is not finished
    ask for word (MAKE UPPERCASE)
    check if valid word
    ask for location
    check if valid location
    check if valid move
    print score
    find best possible move
    print best possible word, score, location
    update board
    print board
    update tiles
    print tiles/scores
"""

