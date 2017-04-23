import tkinter as tk

NORMAL_SQUARE_COLOR = '#FFFB33'
AREA1_SQUARE_COLOR = '#F3BBF1'
AREA2_SQUARE_COLOR = '#7CFC00'


class Board:
    def __init__(self, size):
        self._view = tk.Frame()
        self._view.pack()
        self._size = size
        self._init_view()

    def _init_view(self):
        self._view.grid()
        self.winArea1 = [[0, self._size - 1], [0, self._size - 2], [0, self._size - 3],
                         [0, self._size - 4],
                         [1, self._size - 1], [1, self._size - 2], [1, self._size - 3],
                         [2, self._size - 1], [2, self._size - 2],
                         [3, self._size - 1]]
        self.winArea2 = [[self._size - 1, 0], [self._size - 1, 1], [self._size - 1, 2],
                         [self._size - 1, 3],
                         [self._size - 2, 0], [self._size - 2, 1], [self._size - 2, 2],
                         [self._size - 3, 0], [self._size - 3, 1],
                         [self._size - 4, 0]]

        self._blank_tile = tk.PhotoImage(file='')
        self._blue_ball = tk.PhotoImage(file='blueBall.png')
        self._red_ball = tk.PhotoImage(file='redBall.png')

        self._grid = self._init_grid()

    def _init_grid(self):
        grid = [[None] * self._size] * self._size

        for x in range(self._size):
            for y in range(self._size):
                if [x, y] not in self.winArea1 and [x, y] not in self.winArea2:
                    piece = tk.Button(bg=NORMAL_SQUARE_COLOR, width=40, height=40, text='empty', image=self._blank_tile,
                                      borderwidth=5)
                elif [x, y] in self.winArea1:
                    piece = tk.Button(bg=AREA1_SQUARE_COLOR, width=40, height=40, text='blue', image=self._blue_ball,
                                      borderwidth=5)
                else:
                    piece = tk.Button(bg=AREA2_SQUARE_COLOR, width=40, height=40, text='red', image=self._red_ball,
                                      borderwidth=5)
                grid[x][y] = piece
                piece.grid(row=x, column=y)

        return grid


class Game:
    def __init__(self, size, master=None):
        self._size = size
        self.status = [] # will be set to status widget when created

        self._board = Board(size)

        print("Hello world")

    def _add_reset_btn(self):
        # create a restart button to restart the game
        resetButton = tk.Button(text="RESTART", command=lambda:self.restart())
        resetButton.grid(row=self.boardSize+2, columnspan=self.boardSize)

    def _add_quit_btn(self):
        # create a quit button to quit the game
        quitButton = tk.Button(text="QUIT", command=lambda:self.quit())
        quitButton.grid(row=self.boardSize+4, columnspan=self.boardSize)

    def findLegalMoves(self, board):
        legalMoves = []

        # first, we want to find all jump moves
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.boardGrid[i][j].text != 'empty':
                    self.findJump(board, [i, j], [i, j-1], legalMoves)
                    self.findJump(board, [i, j], [i, j+1], legalMoves)
                    self.findJump(board, [i, j], [i-1, j], legalMoves)
                    self.findJump(board, [i, j], [i-1, j-1], legalMoves)
                    self.findJump(board, [i, j], [i-1, j+1], legalMoves)
                    self.findJump(board, [i, j], [i+1, j], legalMoves)
                    self.findJump(board, [i, j], [i+1, j-1], legalMoves)
                    self.findJump(board, [i, j], [i+1, j+1], legalMoves)

        # if no jump moves have been found, then find regular moves
        if legalMoves == []:
            for i in range(self.boardSize):
                for j in range(self.boardSize):
                    if (self.boardGrid[i][j].text != 'empty'):
                        self.findRegularMove(board, [i, j], legalMoves)

    def findJump(self, board, current, transit, legalMoves):
        if (transit[0] < 0 and transit >= self.boardSize):
            return
        for i in range(transit[0]-1, transit[0]+2):
            for j in range(transit[1]-1, transit[1]+2):
                if ((i - transit[0]) == (transit[0] - current[0]) and
                            (j - transit[1]) == (transit[1] - current[1]) and
                        (not (i == current[0] and j == current[1]))):
                    if (board[i][j].text != 'empty'):
                        legalMoves.append([i, j])


    def findRegularMove(self, board, current, legalMoves):
        for i in range(current[0]-1, current[0]+2):
            for j in range(current[1]-1, current[1]+2):
                if (i >= 0 and j >= 0 and i < self.boardSize and j < self.boardSize
                and (not(current[0] == i and current[1] == j))):
                    if (board[i][j].text != 'empty'):
                        legalMoves.append([i, j])


    def restart(self):
        self._board = Board(size)

    def move(self):
        #todo
        pass

if __name__ == "__main__":
    size = 8

    root = tk.Tk()
    root.wm_title("Halma {0:d} x {0:d}".format(size))
    game = Game(size, root)

    root.mainloop()
