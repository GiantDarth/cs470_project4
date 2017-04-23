import tkinter as tk

NORMAL_SQUARE_COLOR = '#FFFB33'
AREA1_SQUARE_COLOR = '#F3BBF1'
AREA2_SQUARE_COLOR = '#7CFC00'


class Board:
    def __init__(self, size):
        self._view = tk.Frame()
        self._view.pack(fill=tk.BOTH, expand=1)
        self._size = size
        self._init_view()
        self.status = []

    def _init_view(self):
        self.player1 = self.zone1 = [[0, self._size - 1], [0, self._size - 2], [0, self._size - 3],
                         [0, self._size - 4],
                         [1, self._size - 1], [1, self._size - 2], [1, self._size - 3],
                         [2, self._size - 1], [2, self._size - 2],
                         [3, self._size - 1]]
        self.player2 = self.zone2 = [[self._size - 1, 0], [self._size - 1, 1], [self._size - 1, 2],
                         [self._size - 1, 3],
                         [self._size - 2, 0], [self._size - 2, 1], [self._size - 2, 2],
                         [self._size - 3, 0], [self._size - 3, 1],
                         [self._size - 4, 0]]

        canvas = tk.Canvas(self._view, bg="#477D92")

        self._grid = [[None] * self._size] * self._size
        self._pieces = [[None] * self._size] * self._size

        for x in range(self._size):
            for y in range(self._size):
                # self._grid[x][y] = canvas.create_rectangle(x * 50 + 40, y * 50 + 30, x * 50 + 90, y * 50 + 80, outline="#fff",
                #                                            fill="#477D92", tags="bg")

                BLACK = "#000"
                fill = tag = ""
                if x % 2 == 0:
                    if y % 2 == 0:
                        fill = BLACK
                        tag = "black"
                    else:
                        fill = NORMAL_SQUARE_COLOR
                        tag = "yellow"
                else:
                    if y % 2 == 0:
                        fill = NORMAL_SQUARE_COLOR
                        tag = "yellow"
                    else:
                        fill = BLACK
                        tag = "black"
                self._grid[x][y] = canvas.create_rectangle(x * 50 + 40, y * 50 + 30, x * 50 + 90, y * 50 + 80, outline="#fff", fill=fill, tags=tag)

                if [x, y] in self.zone1:
                    self._pieces[x][y] = self._pieces[x][y] = canvas.create_oval(x * 50 + 45, y * 50 + 35, x * 50 + 85, y * 50 + 75, fill="#BB578F", tag="oval")
                elif [x, y] in self.zone2:
                    self._pieces[x][y] = self._pieces[x][y] = canvas.create_oval(x * 50 + 45, y * 50 + 35, x * 50 + 85, y * 50 + 75, fill="#B2D965", tag="oval")

        canvas.pack(fill=tk.BOTH, expand=1)

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

    def winning(self):
        if all(piece in self.zone2 for piece in self.player1):
            displayStatus(mystatus, "Pink player aka player 1 wins!")
        if all(piece in self.zone1 for piece in self.player2):
            displayStatus(mystatus, "Green player aka player 2 wins!")
    
    def displayStatus(alabel, msg):
        alabel.config(bg='yellow', fg='red', text=msg)
        alabel.after(3000, lambda: theButton.config(image=newImage, text=newText))

if __name__ == "__main__":
    size = 8

    root = tk.Tk()
    root.wm_title("Halma {0:d} x {0:d}".format(size))
    game = Game(size, root)

    root.mainloop()
