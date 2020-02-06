import GUI

def findEmptySpaces(grid, current):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                current[0] = row
                current[1] = col
                return current, False
    return current, True


def checkRow(grid, row, num):
    for i in range(9):
        if grid[row][i] == num:
            return True
    return False


def checkCol(grid, col, num):
    for i in range(9):
        if grid[i][col] == num:
            return True
    return False


def checkBox(grid, row, col, num):
    for i in range(3):
        for j in range(3):
            if grid[i + (row - row % 3)][j + (col - col % 3)] == num:
                return True
    return False


def checkLocation(grid, row, col, num):
    return not checkRow(grid, row, num) and not checkCol(grid, col, num) and not checkBox(grid, row, col, num)


def solve(grid):

    current = [0, 0]
    current, fin = findEmptySpaces(grid, current)
    if fin:
        print(grid)
        return True

    row = current[0]
    col = current[1]

    for num in range(1, 10):
        if checkLocation(grid, row, col, num):
            grid[row][col] = num
            GUI.placeNum(row, col, num)

            if(solve(grid)):
                return True

            grid[row][col] = 0
            GUI.placeNum(row, col, 0)

    return False


GUI.start()
