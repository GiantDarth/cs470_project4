import argparse
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARD = ['gameBoard']
MARGIN = 10
SIDE = 10
WIDTH = HEIGHT = MARGIN*2+ SIDE * 5

class gameError(Exception):
    pass

class gameBoard(object):
    def __init__(self,board_game):
        self.board = __create_board(board_game)

    def __start_board(self,board_game):
        board = []
        for line in board_game:
            #line = line.strip()

            #if len(line) != 5:
                #board = []
                #raise gameError(
                    #"The lines in the game board must be 5 chars long"
                #)
        board.append([])
        return board

class checkersGame(object):
    def __init__(self,board_game):
        self.board_game=board_game
        self.start_game = gameBoard(board_game).board

    def start(self):
        self.game_end = False
        self.game = []
        for i in xrange(5):
            self.game.append([])
            for j in xrange(5):
                self.game[i].append(self.start_game[i][j])

    #def win_condition(selfself):
        #for row in xrange(5):
            #if not self.__check_row(row):
                #return False
        #for column in xrange(5):
            #if not self.__check_column(column):
                #return False
        #for row in xrange()

class gameUI(Frame):
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = 0,0
        self.__inituser()

    def __inituser(selfself):
        self.parent.title("Chinese checkers")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text="clear the board", command=self,__clear_board)
        clear_button.pack(fill=BOTH, side=BUTTOM)

        self._make_grid()
        self._make_game()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pushed)


    def __make_grid(self):

    def __make_game(self):
