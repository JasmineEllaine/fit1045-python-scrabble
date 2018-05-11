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

## game data
turnNo = 1
totalScore = 0
pos = BOARD_SIZE // 2 

## functions here
def makeDictionary(dictionaryName):
    """ Creates a list out of a filename with each line being an item in 
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

def validFirstLocation(r,c, boardsize):
    """ Checks if location is valid for the first turn
    Args:
        r (int): row index   
        c (int): column index
        boardsize (int): size of the board
    Returns:
        True (bool): if move is valid for the first turn
        False (bool): if move is invalid for the first turn
    """
    # checks if r == c
    if r == c:
        # checks if centered
        if r == (boardsize // 2):
            return True
    return False

def wordFitsBoard(r, c, d, boardsize, word):
    """ Checks if word fits inside board 
    Args:
        r (int): row index   
        c (int): column index
        boardsize (int): size of the board
        word (str): user picked word
    Returns:
        True (bool): if word fits board
        False (bool): if word does not fit board
    """
    try:
        if d == 'H':
            if (c + len(word)) <= boardsize:
                return True
        if d == 'V':
            if (r + len(word)) <= boardsize:
                return True
    except Exception:
        return False

def removeLetters(word, tilesList):
    """ Removes first occurence of each letter of a word from a list
    Args:
        word (str): word all uppercase
        tilesList (list): list containing letters in uppercase
    Returns:
        newTilesList (list): same list as tilesList but with word
                             letters removed
    """    
    newTilesList = copy.deepcopy(tilesList)
    for letter in word:
        newTilesList.remove(letter)
    return newTilesList

def correctTiles(word, tiles):
    """Checks if a word can be made using the given tiles
    Args:   
        word (str): word in uppercase
        tiles (list): list containing tiles in uppercase
    Returns:
        True (bool): if word can be made using the given tiles
        False (bool): otherwise
    """
    tilesCopy = copy.deepcopy(tiles)
    validLetters = 0
    for letter in word:
        for tile in tilesCopy:
            # adds one to the tally of valid letters if tile is a letter in word
            # removes tile from tile list
            # breaks out of 2nd loop to compare next letter in word
            if tile == letter:
                validLetters += 1
                tilesCopy.remove(tile)
                break
    if validLetters == len(word):
        return True
    return False

def transpose(board):
    """ Transposes a matrix
    Args:   
        board (list): a list of lists
    Returns:
        list (list): transposed board
    """
    return list(map(list, list(zip(*board))))

def validMove(r, c, d, word, tiles):
    """ Checks if move changes tile on board
               if move uses at least one tile from board
               if word letters not in board can be made using tiles from myTiles
               removes tiles from tile rack if valid
    Args:
        r (int): row index   
        c (int): column index
        d (str): direction
        word (str): word all uppercase
        tiles (list): list containing tiles in uppercase
    Returns:
        1
        True (bool): if move is valid
        False (bool): if move is invalid
        2
        None: if move is invalid/no points scoring tiles
        scoringTiles (list): points scoring tiles
    """
    # creates a list out of the section of the board where word
    # is to be placed
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
                return False, None

    # makes list of word letters not in board
    scoringTiles = [letter for letter in word if letter not in boardSlice]
    # checks if uses at least one tile from board
    if len(scoringTiles) == len(word):
        return False, None

    # checks if myTiles can be used to make remaining letters
    remTiles = [tile for tile in scoringTiles if tile not in myTiles]

    if remTiles == []:
        return True, scoringTiles
    return False, None

def placeWordOnRow(word, c, row):
    """ Places word on a list starting at c
    Args:
        c (int): column index
        word (str): uppercase word
        row (list): row where word will be placed
    Returns: 
        row (list): updated row with word
                    ["", "", "C", "A", "T", "", ""]
    """
    for letterIndex in range(len(word)):
        row[letterIndex + c] = userWord[letterIndex]
    return row

def placeWordOnBoard(r, c, d, word, board):
    """ Places a word on board
    Args:
        r (int): row index   
        c (int): column index
        d (str): direction
        word (str): word all uppercase
        board (list): scrabble board
    Returns:
        board (list): updated scrabble board
    """
    # place normally on row r if H
    if d == "H":
        board[r] = placeWordOnRow(word, c, board[r])
    # transpose board first if V
    # then place on row c
    elif d == "V":
        board = list(map(list, list(zip(*board))))
        board[c] = placeWordOnRow(word, r, board[c])
        board = list(map(list, list(zip(*board))))
    return board

def getWordScore(word):
    """ Calculates the total score of a given word
    Args:   
        word (str): word to be calculated
    Returns:
        (int): total score of the word
    """
    try:
        return reduce((lambda x, y: x + y), [getScore(letter) for letter in word])
    except Exception:
        return 0

def bestFirstWord(dictionary, tilesList, boardsize):
    """ Finds best word for first turn
    Args:
        dictionary (list): list of words in dictionary
        tilesList (list): letters in tile rack
        boardsize (int): size of board
    Returns:
        (str): best word if word can be made
        None: if no word can be made
    """
    # makes list of words from dictionary that an be made using tilesList
    # and is less than half of boardsize
    validWords = [dictWord for dictWord in dictionary if len(dictWord) <= boardsize // 2 + 1 and correctTiles(dictWord, tilesList)]
    validScores = [getWordScore(word) for word in validWords]

    # tries to get index of highest score, then returns corresponding word
    try:
        return validWords[validScores.index(max(validScores))]
    except Exception:
        return None

def bestMove(dictionary, board, boardsize, tilesList):
    try:
        # initialise current best score
        currentBestScore = 0
        # horizontal placements
        # gets every word in dictionary
        for dictWord in dictionary:
            for r, row in enumerate(board):
                for c in range(len(row)):
                    # checks if word satisfies rules
                    d = "H"
                    if wordFitsBoard(r, c, d, boardsize, dictWord):
                        valid, scoringTiles = validMove(r, c, d, dictWord, tilesList)
                        # if all rules satisfied
                        if valid:
                            dictWordScore = getWordScore(scoringTiles) 
                            if dictWordScore >= currentBestScore:
                                currentBestlocation = "{}:{}:{}".format(r, c, d)
                                currentBestWord = dictWord
                    # vertical placements
                    d = "V"
                    if wordFitsBoard(r, c, d, boardsize, dictWord):
                        valid, scoringTiles = validMove(r, c, d, dictWord, tilesList)
                        if valid:
                            dictWordScore = getWordScore(scoringTiles) 
                            if dictWordScore >= currentBestScore:
                                currentBestlocation = "{}:{}:{}".format(r, c, d)
                                currentBestWord = dictWord

        return currentBestWord, currentBestScore, currentBestlocation
    except Exception:
        return None, None, None

## make dictionary
englishDict = makeDictionary("dictionary.txt")

## initialise userWord
userWord = ""
while userWord != "***":

    ## ask for word
    userWord = input("\nEnter a word: ")

    # end turn if word is ***
    if userWord == "***":
        continue

    # makes word uppercase if valid
    # asks for another if invalid
    if not inDictionary(userWord, englishDict):
        print("Invalid word.")
        continue
    userWord = userWord.upper()

    ## ask for location
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

    ## first turn conditions
    # checks if location is centered
    # asks for another location if word not centered
    if turnNo == 1:
        if not validFirstLocation(r, c, BOARD_SIZE):
            # prints suggested first locations if invalid
            print("The location in the first move must be {}:{}:H or {}:{}:V.".format(pos, pos, pos, pos))
            print("Invalid first move location.")
            continue

        # checks if myTiles can make userWord
        # asks for another if not
        if not correctTiles(userWord, myTiles):
            print("Word can't be made with given tiles.")
            continue

        # checks if word can fit the board
        # asks for another if not
        if not wordFitsBoard(r, c, d, BOARD_SIZE, userWord):
            print("Word outside board dimensions.")
            continue

        # set points scoring tiles
        scoringTiles = userWord

    ## all other turns
    else:
        # checks if word can fit the board
        # asks for another if not
        if not wordFitsBoard(r, c, d, BOARD_SIZE, userWord):
            print("Word outside board dimensions.")
            continue

        # checks if move is valid
        valid, scoringTiles = validMove(r, c, d, userWord, myTiles)
        if not valid:
            print("Invalid move.")
            continue

    ## gets best move
    # first turn
    if turnNo == 1:
        bestWord = bestFirstWord(englishDict, myTiles, BOARD_SIZE)
    # all other turns
    else:
        bestWord, bestScore, bestLocation = bestMove(englishDict, Board, BOARD_SIZE, myTiles)

    # if no move can be made   
    if bestWord == None:
        print("No move can be made.")    
    else:
        if turnNo == 1:
            print("Maximum possible score in this move was {} with word {} at {}:{}:H or {}:{}:V".format(getWordScore(bestWord), bestWord, pos, pos, pos, pos))
        else:
            print("Maximum possible score in this move was {} with word {} at {}".format(bestScore, bestWord, bestLocation))
    
    # place word on board
    Board = placeWordOnBoard(r, c, d, userWord, Board)
    # update tiles
    myTiles = removeLetters(scoringTiles, myTiles)
    # get turn scores
    wordScore = getWordScore(scoringTiles)
    totalScore += wordScore
    print("Your score in this move:", wordScore)
    print("Your total score:", totalScore)
    printBoard(Board)

    getTiles(myTiles)
    printTiles(myTiles)
    turnNo += 1

print("Thanks for playing!")