word_list = []
word = input("Enter your word: ")
word_list.append(word)

loc = input('Enter the location in row:col:direction format:')
(row, col, vh) = loc.split(':')
row = int(row)
col = int(col)
vh = str(vh)
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


def inOrNot(txt, List):
    for i in range(len(List)):
        if List[i] == txt:
            return True
    return False


def third_function(word):
    for i in range(len(word)):
        if not (inOrNot(word[i], alphabet)):
            return False
    return True


dictionaryfile = open('dictionary.txt', 'r')
wordlist = []


def check(word, dictionaryfile):
    for x in dictionaryfile:
        x = x[:-1]
        wordlist.append(x)
        if x == word:
            return True
    return False





def placeWord(Board, word, row, col, vh):
    if checkPlacement(Board, word, row, col, vh):
        for letter in word:
            Board[row][col] = letter
            if vh == 'V':
                row += 1
            else:
                col += 1


def checkPlacement(Board, word, row, col, vh):
    if row + len(word) > len(Board) and vh == "H":
        return False
    if row + len(word) > len(Board) and vh == "V":
        return False
    for letter in word:
        if Board[row][col] != "" and Board[row][col] != letter:
            return False
    return True


placeWord(Board, word, row, col, vh)
printBoard(Board)


def canBeMadeWithTiles(word, myTiles):
    # create a copy of the tiles as we do not want to change myTiles
    backupTiles = myTiles.copy()
    for letter in word:
        if letter not in backupTiles:
            return False
        else:
            backupTiles.remove(letter)
    return True


def useTiles(tiles, word):
    back_tiles = tiles.copy()
    for letter in word:
        if letter in back_tiles:
            back_tiles.remove(letter)
        else:
            return tiles
    return back_tiles


print(canBeMadeWithTiles(word, myTiles))
print(useTiles(myTiles, word))

getTiles(myTiles)
print(printTiles(myTiles))


# returns score of a word
def getWordScore(word):
    score = 0
    for letter in word:
        score += getScore(letter)
    return score
print(getWordScore(word))

# returns best word and its score
def getBestWord(word,my_Tiles):
    bestWord = ""
    bestScore = 0
    for word in myTiles:
        # word is valid only if it can be made using the tiles
        if canBeMadeWithTiles(word, myTiles):
            thisScore = getWordScore(word)
            # update the bestWord and its score if word is better than the current best word
            if thisScore > bestScore:
                bestWord = word
                bestScore = thisScore

    return bestWord, bestScore
print(getBestWord(word,myTiles))

valid=False
while word != "***"and valid==False:
    if third_function(word)==False:
        print("Invalid move!")
    elif check(word, dictionaryfile)==False:
        print("Invalid move!")
    elif (vh == "V" or vh == "H")==False:
        print("invalid move!")
    elif  (row >= 0 and col >= 0 and (row < BOARD_SIZE and col < BOARD_SIZE))==False:
        print("invalid move!")
    elif (row == len(Board) // 2 and col == len(Board) // 2)==False:
        print("Invalid move!")
    elif (row >= 0 and col >= 0 and (len(word) <= (len(Board) - row) and len(word) <= (len(Board) - col)))==False:
        print("The location in the first move must be 3:3:H or 3:3:V")
        print("Invalid move!")

    else:
        valid=True
        print("Your score in this move:"+str(getWordScore(word)))


    if valid==False:
        word = input("Enter your word: ")
        loc = input('Enter the location in row:col:direction format:')
        (row, col, vh) = loc.split(':')
        row = int(row)
        col = int(col)
        vh = str(vh)
