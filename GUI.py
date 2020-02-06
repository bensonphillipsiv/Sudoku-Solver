import pygame
pygame.font.init()


class Grid:

    def __init__(self, rows, cols, width, height):

        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.originalBoard = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.exampleBoard = [
            [0, 0, 0, 0, 0, 5, 9, 6, 2],
            [1, 5, 9, 8, 6, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 9, 1, 8, 0],
            [2, 0, 0, 0, 9, 0, 6, 0, 3],
            [6, 7, 1, 3, 4, 8, 0, 0, 0],
            [0, 3, 0, 0, 2, 0, 8, 1, 4],
            [0, 1, 7, 0, 0, 0, 3, 9, 6],
            [5, 0, 2, 6, 8, 0, 0, 0, 0],
            [0, 0, 4, 9, 0, 7, 0, 2, 8]
        ]

        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                if self.originalBoard[i][j] == 0:
                    self.cubes[i][j].draw(win, False)
                else:
                    self.cubes[i][j].draw(win, True)

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, row, col, val):
        self.cubes[row][col].set(val)
        self.update_model()

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def select(self, row, col, using):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        if using:
            self.cubes[row][col].selected = True
            self.selected = (row, col)

    def returnSelected(self):
        return self.selected[0], self.selected[1]

    def setOriginal(self, row, col, val):
        self.board[row][col] = val
        self.originalBoard[row][col] = val
        board.place(row, col, val)

    def checkEmpty(self):
        for points in self.board:
            for point in points:
                if point != 0:
                    print(point)
                    return True
        for row in range(9):
            for col in range(9):
                self.setOriginal(row, col, self.exampleBoard[row][col])
                running(0)


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win, originalBoard):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if not(self.value == 0) and not originalBoard:
            text = fnt.render(str(self.value), 1, (0, 0, 255))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 4)

    def set(self, val):
        self.value = val


def redraw_window(win, board):
    win.fill((255, 255, 255))
    # Draw grid and board
    board.draw(win)


win = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Sudoku")
board = Grid(9, 9, 540, 540)


def placeNum(row, col, num):
    board.place(row, col, num)
    running(20)


def running(timeDelay):
    pygame.time.delay(timeDelay)
    key = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                key = 1
            if event.key == pygame.K_2:
                key = 2
            if event.key == pygame.K_3:
                key = 3
            if event.key == pygame.K_4:
                key = 4
            if event.key == pygame.K_5:
                key = 5
            if event.key == pygame.K_6:
                key = 6
            if event.key == pygame.K_7:
                key = 7
            if event.key == pygame.K_8:
                key = 8
            if event.key == pygame.K_9:
                key = 9
            if event.key == pygame.K_0:
                key = 0
            if event.key == pygame.K_DELETE:
                key = 0
            if event.key == pygame.K_BACKSPACE:
                key = 0
            if event.key == pygame.K_RETURN:
                board.select(0, 0, False)
                return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked = board.click(pos)
            if clicked:
                board.select(clicked[0], clicked[1], True)

    if board.selected and key != None:
        row, col = board.returnSelected()
        board.setOriginal(row, col, key)

    redraw_window(win, board)
    pygame.display.update()


def start():
    import SudokuSolver
    #
    while 1:
        if running(10):
            break

    board.checkEmpty()
    SudokuSolver.solve(board.board)
