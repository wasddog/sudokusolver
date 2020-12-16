import pyautogui
from sys import exit
from keyboard import is_pressed

#### SETTINGS ####

board = [[0 for x in range(9)] for y in range(9)]
boardOnScreen = 294,261,883,851 # pyautogui.displayMousePosition() to get board pos on screen
WIDTH , HEIGHT = boardOnScreen[2]-boardOnScreen[0], boardOnScreen[3]-boardOnScreen[1]
cellSize = WIDTH // 9

##################

def click(x,y):
    pyautogui.click(x,y)



def fillBoard(number, x, y):
    board[y][x] = number
    return board


def posTranslate(x,y):
    c = cellSize
    ys = c
    xs = c
    for yid in range(9):
        if y > boardOnScreen[1] and y < boardOnScreen[1] + ys:
            for xid in range(9):
                if x > boardOnScreen[1] and x < boardOnScreen[1] + xs:
                    return (xid, yid)
                else: xs += c
        else: ys += c


def locateOnScreen():
    for n in range(1,10):
        data = list(pyautogui.locateAllOnScreen('data/'+str(n)+'.png', region=boardOnScreen, grayscale=True, confidence=0.85))
        if data != None:
            for d in data:
                fillBoard(n, posTranslate(d[0], d[1])[0], posTranslate(d[0], d[1])[1])
    return board


def solve(bo):
    find = empties(bo)
    if not find: return True
    else: row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo): return True
            bo[row][col] = 0
    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i: return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i: return False

    # Check box
    boxx = pos[1] // 3
    boxy = pos[0] // 3

    for i in range(boxy*3, boxy*3 + 3):
        for j in range(boxx * 3, boxx*3 + 3):
            if bo[i][j] == num and (i,j) != pos: return False
    return True


def empties(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0: return (i, j)  # row, col
    return None


def boardToScreen():
    stepy = boardOnScreen[1] + (cellSize // 2)
    for i in board:
        stepx = boardOnScreen[0] + (cellSize // 2)
        for j in i:
            if is_pressed('q') or is_pressed('esc'): exit()
            click(stepx, stepy)
            pyautogui.press(str(j))
            stepx += cellSize
        stepy += cellSize


if __name__ == '__main__':
    locateOnScreen()
    solve(board)
    boardToScreen()
    print('Done!')

