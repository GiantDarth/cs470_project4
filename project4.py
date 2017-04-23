import tkinter as tk

NORMAL_SQUARE_COLOR = '#FFFB33'
AREA1_SQUARE_COLOR = '#F3BBF1'
AREA2_SQUARE_COLOR = '#7CFC00'

class BoardView(tk.Frame):
    def __init__(self, boardSize, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        print("Made a new board")
        self.boardGrid = []
        self.status = [] # will be set to status widget when created
        self.boardSize = boardSize
        self.winArea1 = [[0, self.boardSize-1], [0, self.boardSize-2], [0, self.boardSize-3], [0, self.boardSize-4],
                   [1, self.boardSize-1], [1, self.boardSize-2], [1, self.boardSize-3],
                   [2, self.boardSize-1], [2, self.boardSize-2],
                   [3, self.boardSize-1]]
        self.winArea2 = [[self.boardSize-1, 0], [self.boardSize-1, 1], [self.boardSize-1, 2], [self.boardSize-1, 3],
                    [self.boardSize-2, 0], [self.boardSize-2, 1], [self.boardSize-2, 2],
                    [self.boardSize-3, 0], [self.boardSize-3, 1],
                    [self.boardSize-4, 0]]
        self.blankTile = tk.PhotoImage(file='')
        self.redBall = tk.PhotoImage(file='redBall.png')
        rball = self.redBall.subsample(2, 2)
        self.blueBall = tk.PhotoImage(file='blueBall.png')
        self.moving = False
        self.createBoard()

    def createBoard(self):
        self.boardGrid.extend([[0]*self.boardSize]* self.boardSize)

        for x in range(self.boardSize):
            for y in range(self.boardSize):
                if ([x, y] not in self.winArea1 and [x, y] not in self.winArea2):
                    piece = tk.Button(bg=NORMAL_SQUARE_COLOR, width=40, height=40, text='empty', image=self.blankTile, borderwidth=5)
                elif ([x, y] in self.winArea1):
                    piece = tk.Button(bg=AREA1_SQUARE_COLOR, width=40, height=40, text='blue', image=self.blueBall, borderwidth=5)
                else:
                    piece = tk.Button(bg=AREA2_SQUARE_COLOR, width=40, height=40, text='red', image=self.redBall, borderwidth=5)
                self.boardGrid[x][y] = piece
                piece.grid(row=x, column=y)

        # create a restart button to restart the game
        resetButton = tk.Button(text="RESTART", command=lambda:self.restart())
        resetButton.grid(row=self.boardSize+2, columnspan=self.boardSize)

        # create a quit button to quit the game
        quitButton = tk.Button(text="QUIT", command=lambda:self.quit())
        quitButton.grid(row=self.boardSize+4, columnspan=self.boardSize)

    def restart(self):
        self.createBoard()

    def move(self):
        #todo
        pass

board=BoardView(8)
board.mainloop()