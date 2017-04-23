import tkinter as tk

NORMAL_SQUARE_COLOR = '#FFFB33'
AREA1_SQUARE_COLOR = '#F3BBF1'
AREA2_SQUARE_COLOR = '#7CFC00'


class Board:
    def __init__(self, size):
        self._view = tk.Frame()
        self._size = size
        self._init_view()

    def _init_view(self,):
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
        self.blankTile = tk.PhotoImage(file='')
        self.redBall = tk.PhotoImage(file='redBall.png')
        rball = self.redBall.subsample(2, 2)
        self.blueBall = tk.PhotoImage(file='blueBall.png')
        self._grid = self._init_grid()


    def _init_grid(self):
        grid = []
        grid.extend([[0] * self._size] * self._size)

        for x, y in zip(range(self._size), range(self._size)):
            if [x, y] not in self.winArea1 and [x, y] not in self.winArea2:
                piece = tk.Button(bg=NORMAL_SQUARE_COLOR, width=40, height=40, text='empty', image=self.blankTile,
                                  borderwidth=5)
            elif ([x, y] in self.winArea1):
                piece = tk.Button(bg=AREA1_SQUARE_COLOR, width=40, height=40, text='blue', image=self.blueBall,
                                  borderwidth=5)
            else:
                piece = tk.Button(bg=AREA2_SQUARE_COLOR, width=40, height=40, text='red', image=self.redBall,
                                  borderwidth=5)
            self.boardGrid[x][y] = piece
            piece.grid(row=x, column=y)

        return grid


class Game:
    def __init__(self, size, ):
        self._size = size
        self.status = [] # will be set to status widget when created

        self._board = Board(size)

        print("Hello world")

    def _add_reset_btn(self):
        # create a restart button to restart the game
        resetButton = tk.Button(text="RESTART", command=lambda: self.restart())
        resetButton.grid(row=self._size + 2, columnspan=self._size)

    def _add_quit_btn(self):
        # create a quit button to quit the game
        quitButton = tk.Button(text="QUIT", command=lambda: self.quit())
        quitButton.grid(row=self._size + 4, columnspan=self._size)

    def quit(self):
        pass

    def restart(self):
        pass

    def move(self, board, move_obj):
        pass

if __name__ == "__main__":
    size = 8
    game = Game(size)

    root = tk.Tk()
    root.title = "Halma {0:d}x{0:d}".format(size)

    _root.mainloop()
