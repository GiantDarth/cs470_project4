import Tkinter as tk

class BoardView(tk.Frame):
    def __init__(self, boardSize, master=None, initBoard=[]):
        tk.Frame.__init__(self, master)
        self.grid()
        print("Made a new board")
        self.boardGrid = []
        self.status = [] # will be set to status widget when created
        self.boardSize = boardSize

        self.blankTitle = tk.PhotoImage(file = '')
        self.redPiece = tk.PhotoImage(file = '')
        self.redGo = tk.PhotoImage(file = '')
        self.redGone = tk.PhotoImage(file = '')
        self.moving = False
        self.createBoard(initBoard)

    def createBoard(self, theBoard):
        if not theBoard:
            theBoard.extend([[0]*self.boardSize]*self.boardSize)
        self.boardGrid.extend( [[0]*self.boardSize]* self.boardSize)

        def displayStatus(label, msg):
            alabel.config(bg= 'yellow', fg= 'red', text=msg)
            alabel.after(3000, lambda: theButton.config(image=newImage, text=newText))

        def changeButton(theButton,transImage,newImage,newText):
            theButton.config(image=TransImage,text='empty')
            theButton.after(3000, lambda:theButton.config(image=newImage, text=newtext))




board=BoardView()
