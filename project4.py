import tkinter as tk
import sys
import time

LIGHT_SQUARE_COLOR = '#CCC'
DARK_SQUARE_COLOR = "#222"

PLAYER_1_COLOR = "#BB578F"
PLAYER_2_COLOR = "#B2D965"

PLAYER_1_DARK_ZONE = "#D583B1"
PLAYER_1_LIGHT_ZONE = "#E7AFCF"

PLAYER_2_DARK_ZONE = "#D2F195"
PLAYER_2_LIGHT_ZONE = "#E3F7BC"

OFFSET_X = 40
OFFSET_Y = 30

TILE_SIZE = 45
PIECE_SIZE_DIFF = 5

NUM_PIECES = {"8": 10, "10": 15, "16": 19}

class Board:
    def __init__(self, size, zone1, zone2, on_process_turn):
        self._view = tk.Frame()
        self._view.pack(fill=tk.BOTH, expand=1)
        self._size = size

        self._zone1 = zone1[:]
        self._zone2 = zone2[:]

        self._on_process_turn = on_process_turn
        self._init_view()

    def _init_view(self):
        self._canvas = tk.Canvas(self._view, bg="#477D92",
                                 width=OFFSET_X * 2 + TILE_SIZE * self._size,
                                 height=OFFSET_Y * 2 + TILE_SIZE * self._size)
        self._canvas.pack(expand=1)

        self._grid = [[None] * self._size] * self._size
        self._player1 = []
        self._player1_pieces = []
        self._player2 = []
        self._player2_pieces = []

        for x in range(self._size):
            self._canvas.create_text(int((x + 0.5) * TILE_SIZE) + OFFSET_X, OFFSET_Y // 2, text=chr(65 + x), fill="white")
            self._canvas.create_text(int((x + 0.5) * TILE_SIZE) + OFFSET_X, self._size * TILE_SIZE + int(1.5 * OFFSET_Y), text=chr(65 + x), fill="white")

        for y in range(self._size):
            self._canvas.create_text(OFFSET_X // 2, int((self._size - 1 - y + 0.5) * TILE_SIZE) + OFFSET_Y, text=y + 1, fill="white")
            self._canvas.create_text(self._size * TILE_SIZE + int(1.5 * OFFSET_X), int((self._size - 1 - y + 0.5) * TILE_SIZE) + OFFSET_Y, text=y + 1, fill="white")

        for x in range(self._size):
            for y in range(self._size):
                fill = tag = ""
                if x % 2 == 0:
                    if y % 2 == 0:
                        if (x, y) in self._zone1:
                            fill = PLAYER_1_LIGHT_ZONE
                            tag = ("light", "zone1")
                        elif (x, y) in self._zone2:
                            fill = PLAYER_2_LIGHT_ZONE
                            tag = ("light", "zone2")
                        else:
                            fill = LIGHT_SQUARE_COLOR
                            tag = "light"
                    else:
                        if (x, y) in self._zone1:
                            fill = PLAYER_1_DARK_ZONE
                            tag = ("dark", "zone1")
                        elif (x, y) in self._zone2:
                            fill = PLAYER_2_DARK_ZONE
                            tag = ("dark", "zone2")
                        else:
                            fill = DARK_SQUARE_COLOR
                            tag = "dark"
                else:
                    if y % 2 == 0:
                        if (x, y) in self._zone1:
                            fill = PLAYER_1_DARK_ZONE
                            tag = ("dark", "zone1")
                        elif (x, y) in self._zone2:
                            fill = PLAYER_2_DARK_ZONE
                            tag = ("dark", "zone2")
                        else:
                            fill = DARK_SQUARE_COLOR
                            tag = "dark"
                    else:
                        if (x, y) in self._zone1:
                            fill = PLAYER_1_LIGHT_ZONE
                            tag = ("light", "zone1")
                        elif (x, y) in self._zone2:
                            fill = PLAYER_2_LIGHT_ZONE
                            tag = ("light", "zone2")
                        else:
                            fill = LIGHT_SQUARE_COLOR
                            tag = "light"
                self._grid[x][y] = self._canvas.create_rectangle(x * TILE_SIZE + OFFSET_X, y * TILE_SIZE + OFFSET_Y,
                                                                 (x + 1) * TILE_SIZE + OFFSET_X, (y + 1) * TILE_SIZE + OFFSET_Y,
                                                                 outline="#fff", fill=fill, tags=tag)

        self._canvas.tag_bind("piece", "<ButtonPress-1>", self._onPressDown)
        self._canvas.tag_bind("piece", "<B1-Motion>", self._onMove)
        self._canvas.tag_bind("piece", "<ButtonRelease-1>", self._on_process_turn)

    def _onPressDown(self, event):
        piece = self._canvas.find_closest(event.x, event.y)
        while "piece" not in self._canvas.gettags(piece):
            piece = self._canvas.find_closest(event.x, event.y, start=piece)

        oldX = (event.x - OFFSET_X) // TILE_SIZE
        oldY = (event.y - OFFSET_Y) // TILE_SIZE

        self._dragged_piece = (piece, (oldX, oldY))
        self._current_drag_pos = [event.x, event.y]

    def _onMove(self, event):
        delta = [event.x - self._current_drag_pos[0], event.y - self._current_drag_pos[1]]
        self._canvas.move(self._dragged_piece[0], delta[0], delta[1])
        self._current_drag_pos = (event.x, event.y)

    def update(self, player1, player2):
        self._player1 = player1[:]
        self._player2 = player2[:]

        for piece in self._player1_pieces:
            self._canvas.delete(piece)
        for piece in self._player2_pieces:
            self._canvas.delete(piece)

        self._player1_pieces = [self._canvas.create_oval(x * TILE_SIZE + OFFSET_X + PIECE_SIZE_DIFF,
                                                         y * TILE_SIZE + OFFSET_Y + PIECE_SIZE_DIFF,
                                                         (x + 1) * TILE_SIZE + OFFSET_X - PIECE_SIZE_DIFF,
                                                         (y + 1) * TILE_SIZE + OFFSET_Y - PIECE_SIZE_DIFF,
                                                         fill=PLAYER_1_COLOR, tag=("piece", "player1")) for (x, y) in player1]
        self._player2_pieces = [self._canvas.create_oval(x * TILE_SIZE + OFFSET_X + PIECE_SIZE_DIFF,
                                                         y * TILE_SIZE + OFFSET_Y + PIECE_SIZE_DIFF,
                                                         (x + 1) * TILE_SIZE + OFFSET_X - PIECE_SIZE_DIFF,
                                                         (y + 1) * TILE_SIZE + OFFSET_Y - PIECE_SIZE_DIFF,
                                                         fill=PLAYER_2_COLOR, tag=("piece", "player2")) for (x, y) in player2]

    def get_dragged_piece(self):
        return self._dragged_piece

    def _is_tile_empty(self, x, y):
        return (x, y) in self._player1 or (x, y) in self._player2

    def findLegalMoves(self, player):
        legalMoves = []

        # first, we want to find all jump moves
        for i in range(self._size):
            for j in range(self._size):
                if self._is_tile_empty(i, j):
                    self.findJump((i, j), (i, j - 1), legalMoves)
                    self.findJump((i, j), (i, j + 1), legalMoves)
                    self.findJump((i, j), (i - 1, j), legalMoves)
                    self.findJump((i, j), (i - 1, j - 1), legalMoves)
                    self.findJump((i, j), (i - 1, j + 1), legalMoves)
                    self.findJump((i, j), (i + 1, j), legalMoves)
                    self.findJump((i, j), (i + 1, j - 1), legalMoves)
                    self.findJump((i, j), (i + 1, j + 1), legalMoves)

        # Find regular moves
        for i in range(self._size):
            for j in range(self._size):
                if self._is_tile_empty(i, j):
                    self.findRegularMove((i, j), legalMoves)

        return legalMoves

    def findJump(self, current, transit, legalMoves):
        if transit[0] < 0 or transit[0] >= self._size or transit[1] < 0 or transit[1] >= self._size:
            return

        if (self._is_tile_empty(transit[0], transit[1])):
            return

        for i in range(transit[0] - 1, transit[0] + 2):
            for j in range(transit[1] - 1, transit[1] + 2):
                if ((i - transit[0]) == (transit[0] - current[0]) and
                            (j - transit[1]) == (transit[1] - current[1]) and
                        (not (i == current[0] and j == current[1]))):
                    if self._is_tile_empty(i, j):
                        legalMoves.append((i, j))

    def findRegularMove(self, current, legalMoves):
        for i in range(current[0] - 1, current[0] + 2):
            for j in range(current[1] - 1, current[1] + 2):
                if self._is_tile_empty(i, j) and 0 <= i < self._size and 0 <= j < self._size and \
                        not(current[0] == i and current[1] == j):
                    legalMoves.append((i, j))


class Game:
    def __init__(self, size, root):
        self._size = size
        self.status = [] # will be set to status widget when created

        self._status_frame = tk.Frame()
        self._status_frame.pack()

        self.zone1 = self._get_zone("SW")
        self.player1 = self.zone1[:]

        # Add player starting positions
        self.zone2 = self._get_zone("NE")
        self.player2 = self.zone2[:]

        self._board = Board(size, self.zone1, self.zone2, self._on_process_turn)
        self._board.update(self.player1, self.player2)

        self._player_turn = 0
        self.turn_counter = 0

        self._button_frame = tk.Frame()
        self._button_frame.pack(fill=tk.BOTH, expand=1)
        self._button_quit = tk.Button(self._button_frame, text="OKAY")
        self._button_quit.pack()

        self._turn_text = tk.StringVar()
        self._turn_label = tk.Label(self._status_frame, textvariable=self._turn_text)
        self._turn_label.pack()

        self._turn_text.set("Turn {:d} - Player {:d}".format(self.turn_counter + 1, self._player_turn + 1))

        self._timer_text = tk.StringVar()
        self._timer_label = tk.Label(self._status_frame, textvariable=self._timer_text)
        self._timer_label.pack()

        self._root = root
        self._start_time = time.time()
        self._root.after(1000, self.timer)
        self.time_limit = 120
        self._pause = False

        minutes, secs = divmod(self.time_limit, 60)
        self._timer_text.set("{:02d}:{:02d}".format(minutes, secs))

    def _get_zone(self, corner):
        zone = []
        offset_x = 0
        offset_y = 0

        if corner == "SW":
            zone.append((0, self._size - 1))
            offset_x = 1
            offset_y = -1
        elif corner == "NE":
            zone.append((self._size - 1, 0))
            offset_x = -1
            offset_y = 1
        elif corner == "NW":
            zone.append((0, 0))
            offset_x = 1
            offset_y = 1
        elif corner == "SE":
            zone.append((self._size - 1, self._size - 1))
            offset_x = -1
            offset_y = -1


        last_row = zone[:]
        while len(zone) < self._size * self._size - 1:
            row = []
            for piece in last_row:
                if (piece[0] + offset_x, piece[1]) not in row:
                    row.append((piece[0] + offset_x, piece[1]))
                if (piece[0], piece[1] + offset_y) not in row:
                    row.append((piece[0], piece[1] + offset_y))
            # Make sure the pieces start from the middle of the diagonal
            middle = (row[0][0] + row[-1][0]) / 2
            row = sorted(row, key=lambda pos: abs(pos[0] - middle))

            zone.extend(row)
            last_row = row[:]

        return zone[:NUM_PIECES[str(self._size)]]

    def _on_process_turn(self, event):
        # a way to figure out where should the piece be correctly placed at
        newX = (event.x - OFFSET_X) // TILE_SIZE
        newY = (event.y - OFFSET_Y) // TILE_SIZE

        dragged_piece = self._board.get_dragged_piece()

        print(newX, newY)
        self.move(dragged_piece[1], (newX, newY))
        self._board.update(self.player1, self.player2)

    def timer(self):
        delta = time.time() - self._start_time
        minutes, secs = divmod(round(self.time_limit - delta), 60)
        self._timer_text.set("{:02d}:{:02d}".format(minutes, secs))

        if delta >= self.time_limit:
            print("Time ended: next turn.")
            self.end_turn()
        else:
            self._root.after(1000, self.timer)

    def move(self, old, pos):
        # Not that player's turn
        if self._player_turn == 0:
            if old in self.player2:
                print(sys.stderr, "Not player 2's turn!")
                return
            elif old not in self.player1:
                return
            # elif pos not in self._board.findLegalMoves(self.player1):
            #     print(sys.stderr, "Player 1: Illegal move.")
            #     return
            else:
                self.player1.remove(old)
                self.player1.append(pos)

        elif self._player_turn == 1:
            if old in self.player1:
                print(sys.stderr, "Not player 1's turn!")
                return
            elif old not in self.player2:
                return
            # elif pos not in self._board.findLegalMoves(self.player2):
            #     print(sys.stderr, "Player 2: Illegal move.")
            #     return
            else:
                self.player2.remove(old)
                self.player2.append(pos)

        print("Turn {:d}: Player {:d} {}->{}".format(self.turn_counter, self._player_turn + 1, old, pos))

        self.end_turn()

    def end_turn(self):
        if self._player_turn == 0:
            self._player_turn = 1
        elif self._player_turn == 1:
            self._player_turn = 0

        self.turn_counter += 1
        self._start_time = time.time()

        self._turn_text.set("Turn {:d} - Player {:d}".format(self.turn_counter + 1, self._player_turn + 1))

        if self.winning():
            self._pause = True
        else:
            self._root.after(1000, self.timer)

    # def _add_reset_btn(self):
    #     # create a restart button to restart the game
    #     resetButton = tk.Button(text="RESTART", command=lambda: self.restart())
    #     resetButton.grid(row=self.boardSize+2, columnspan=self.boardSize)
    #
    # def _add_quit_btn(self):
    #     # create a quit button to quit the game
    #     quitButton = tk.Button(text="QUIT", command=lambda: self.quit())
    #     quitButton.grid(row=self.boardSize+4, columnspan=self.boardSize)

    def restart(self):
        self._board = Board(size, self._on_process_turn)

    def winning(self):
        if all(piece in self.zone2 for piece in self.player1):
            self.displayStatus(mystatus, "Pink player aka player 1 wins!")
        if all(piece in self.zone1 for piece in self.player2):
            self.displayStatus(mystatus, "Green player aka player 2 wins!")
    
    def displayStatus(alabel, msg):
        alabel.config(bg='yellow', fg='red', text=msg)
        alabel.after(3000, lambda: theButton.config(image=newImage, text=newText))

if __name__ == "__main__":
    size = 8

    root = tk.Tk()
    root.wm_title("Halma {0:d} x {0:d}".format(size))
    game = Game(size, root)

    root.resizable(width=False, height=False)
    root.update()
    root.mainloop()
