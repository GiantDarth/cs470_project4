import tkinter as tk

NORMAL_SQUARE_COLOR = '#FFFB33'
AREA_SQUARE_COLOR = '#F3BBF1'

class BoardView(tk.Frame):
    def __init__(self, boardSize, master=None, initBoard=[]):
        tk.Frame.__init__(self, master)
        self.grid()
        print("Made a new board")
        self.boardGrid = []
        self.status = [] # will be set to status widget when created
        self.boardSize = boardSize

        self.blankTitle = tk.PhotoImage(file = '')
        self.redBall = tk.PhotoImage(file = 'redBall.png')
        self.blueBall = tk.PhotoImage(file = 'blueBall.png')
        self.moving = False
        self.createBoard(initBoard)

    def createBoard(self, theBoard):
        if not theBoard:
            theBoard.extend([[0]*self.boardSize]*self.boardSize)
        self.boardGrid.extend( [[0]*self.boardSize]* self.boardSize)

        def displayStatus(alabel, msg):
            alabel.config(bg= 'yellow', fg= 'red', text=msg)
            alabel.after(3000, lambda: theButton.config(image=newImage, text=newText))

        def changeButton(theButton, transImage, newImage, newText):
            theButton.config(image=transImage,text='empty')
            theButton.after(3000, lambda:theButton.config(image=newImage, text=newText))

        # create a restart button to restart the game
        resetButton = tk.Button(text="RESTART", command=lambda:self.restart())
        resetButton.grid(row=self.boardSize*2, columnspan=self.boardSize)

        # create a quit button to quit the game
        quitButton = tk.Button(text="QUIT", command=lambda:self.quit())
        quitButton.grid(row=self.boardSize+2, columnspan=self.boardSize)

    def restart(self):
        self.createBoard([])

    def move(self):
        # todo

board=BoardView(8)
board.mainloop()