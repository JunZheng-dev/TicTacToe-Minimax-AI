import math
import copy
import time

def resetBoard(board):
    for row in range(n):
        for col in range(n):
            board[row][col] = " "
            
def printBoard(board):
    for row in range(n):
        for col in range(n):
            print(" " + board[row][col], end = " ")
            if (col + 1 != n):
                print('|', end = "")

        print()
        if (row + 1 != n):
            for x in range(n - 1):
                print(" - +", end = "")
            print(" -")

def move(row, col):
    global isX
    if board[row][col] == " ":
        if (isX):
            board[row][col] = "X"
        else:
            board[row][col] = "O"
        isX = not isX
    else:
        print("That move is invalid! Try Again!")
        getPlayerMove()

def isGameTied(board):          # can change to see if turns left = 0
    for row in range(n):        
        for col in range(n):
            if board[row][col] == " ":
                return False

    return True

def isGameWon(board):
    for i in range(n):
        if (identicalElements(board[i]) or  # check rows
            identicalElements([row[i] for row in board]) or # check columns
            identicalElements([board[a][a] for a in range(n)]) or # check diagonals
            identicalElements([board[n - a - 1][a] for a in range(n)])):
            return True;

    return False;

def identicalElements(array):
    for i in array:
        if i == " ":
            return False;
        if array[0] != i:
            return False;

    return True;

def getPlayerMove():
    printBoard(board)
    print("\nPlease Make a Move, Player " + ("X" if isX else "O"))
    move(int(input("Row: ")) - 1, int(input("Column: ")) - 1)

def aiMove(currentPosition, isMaximizingPlayer):
    if isMaximizingPlayer:
        maxEvaluation = -math.inf

        for row in range(n):
            for col in range(n):
                if currentPosition[row][col] == " ":
                    childPosition = copy.deepcopy(currentPosition)
                    childPosition[row][col] = "X"
                    evaluation = minimax(childPosition, not isMaximizingPlayer)
                    
                    if evaluation > maxEvaluation:
                        maxEvaluation = evaluation
                        bestMove = [row, col]    
    else:   
        minEvaluation = math.inf

        for row in range(n):
            for col in range(n):
                if currentPosition[row][col] == " ":
                    childPosition = copy.deepcopy(currentPosition)
                    childPosition[row][col] = "O"
                    evaluation = minimax(childPosition, not isMaximizingPlayer)
                    
                    if evaluation < minEvaluation:
                        minEvaluation = evaluation
                        bestMove = [row, col]

    return bestMove

def minimax(position, isMaximizingPlayer):  # no depth as tic tac toe does not
    if isGameWon(position):                 # take insanely long to calculate
        if isMaximizingPlayer:              # every possible tree
            return -1
        else: 
            return 1
    if isGameTied(position):
        return 0

    childPositions = getChildPositions(position, isMaximizingPlayer)

    if isMaximizingPlayer:
        maxEvaluation = -math.inf
        
        for child in childPositions:
            eval = minimax(child, False)
            maxEvaluation = max(maxEvaluation, eval)
        return maxEvaluation
    else:
        minEvaluation = math.inf
        
        for child in childPositions:
            eval = minimax(child, True)
            minEvaluation = min(minEvaluation, eval)
        return minEvaluation 

def getChildPositions(position, isMaximizingPlayer):
    childPositions = []
    if isMaximizingPlayer:
        sign = "X"
    else:
        sign = "O"

    for row in range(n):
        for col in range(n):
            if position[row][col] == " ":
                newPosition = copy.deepcopy(position)
                newPosition[row][col] = sign
                childPositions.append(newPosition)

    return childPositions

###############################################################################

n = 3                                   # n x n board
board = [[' '] * n for i in range(n)]   # board               
playGame = "yes"

while playGame.lower() == "yes":
    isX = True;  # alternates for x and o's turn
    goFirst = input("Would you like to go first? \'yes\' or \'no\'\n")

    if goFirst.lower() == "yes":
        getPlayerMove()

    while True:
        if isGameWon(board):
            if (isX):
                print("\nO Wins!")
            else:
                print("\nX Wins!")
            break

        if isGameTied(board):
            print("\nIt's a tie!")
            break

        print("The AI is calculating a move.")
        start_time = time.time()
        ai = aiMove(board, isX)
        print("Time to calculate: " + str(time.time() - start_time) + "s\n")
        move(ai[0], ai[1])

        if isGameWon(board):
            if (isX):
                print("\nO Wins!")
            else:
                print("\nX Wins!")
            break

        if isGameTied(board):
            print("\nIt's a tie!")
            break

        getPlayerMove()

    printBoard(board)
    playGame = input("Do you want to play again? Type either \'yes\' or \'no\': ")
    resetBoard(board)
