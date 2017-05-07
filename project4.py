import tkinter as tk
import sys
import time
import argparse
import re
import copy

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

INFINITY = 100000
NEGATIVE_INFINITY = -100000

NUM_PIECES = {"8": 10, "10": 15, "16": 19}

class Board:
    def __init__(self, size, zone1, zone2, on_process_turn):
        self._view = tk.Frame()
        self._view.pack(fill=tk.BOTH, expand=1)
        self._size = size
        self.jump = False

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

    def remove_events(self):
        self._canvas.tag_unbind("piece", "<ButtonPress-1>")
        self._canvas.tag_unbind("piece", "<B1-Motion>")
        self._canvas.tag_unbind("piece", "<ButtonRelease-1>")

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
        return (x, y) not in self._player1 and (x, y) not in self._player2

    def findLegalMoves(self, piece):
        legalMoves = set()

        i = piece[0]
        j = piece[1]

        if self._is_tile_empty(i, j):
            return legalMoves

        # Find the jumps from the initial position
        current_jumps = set()
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                current_jumps |= self.findJump((i, j), (x, y))
        # Find new jumps from last used jump positions, until no more exist.
        last_jumps = current_jumps.copy()
        while last_jumps:
            # Add last jumps to all possible moves
            legalMoves |= last_jumps
            current_jumps = set()
            for move in last_jumps:
                for x in range(move[0] - 1, move[0] + 2):
                    for y in range(move[1] - 1, move[1] + 2):
                        # Add new jumps, but ignore the ones already found.
                        current_jumps |= self.findJump((move[0], move[1]), (x, y)) - legalMoves
            last_jumps = current_jumps.copy()

        if legalMoves:
            self.jump = True
        else:
            self.jump = False

        # Find regular moves
        self.findRegularMove((i, j), legalMoves)

        return legalMoves

    def findJump(self, current, transit):
        moves = set()
        # Bound checking
        if transit[0] < 0 or transit[0] >= self._size or transit[1] < 0 or transit[1] >= self._size:
            return moves

        if self._is_tile_empty(transit[0], transit[1]):
            return moves

        for i in range(transit[0] - 1, transit[0] + 2):
            for j in range(transit[1] - 1, transit[1] + 2):
                if (i - transit[0], j - transit[1]) == (transit[0] - current[0], transit[1] - current[1]) and\
                                (i, j) != transit and (i, j) != current:
                    if self._is_tile_empty(i, j) and 0 <= i < self._size and 0 <= j < self._size:
                        moves.add((i, j))

        return moves

    def findRegularMove(self, current, legalMoves):
        for i in range(current[0] - 1, current[0] + 2):
            for j in range(current[1] - 1, current[1] + 2):
                if (self._is_tile_empty(i, j)) and 0 <= i < self._size and 0 <= j < self._size and \
                        not(current[0] == i and current[1] == j):
                    legalMoves.add((i, j))


class Game:
    def __init__(self, size, t_limit, color, root):
        self._size = size
        self.status = [] # will be set to status widget when created

        self._status_frame = tk.Frame()
        self._status_frame.pack()

        self.zone1 = self._get_zone("SW")
        self.player1 = self.zone1[:]

        # Add player starting positions
        self.zone2 = self._get_zone("NE")
        self.player2 = self.zone2[:]

        self._board = Board(self._size, self.zone1, self.zone2, self._on_process_turn)
        self._board.update(self.player1, self.player2)

        if color == "Red":
            self._human_player = 0
        elif color == "Green":
            self._human_player = 1
        else:
            print(sys.stderr, "Invalid human player used for Game")
            sys.exit(1)

        self._player_turn = 1
        self.turn_counter = 0

        self._button_frame = tk.Frame()
        self._button_frame.pack()

        self._entry = tk.Entry(self._button_frame)
        self._entry.grid(row=0, column=0)
        self._entry.focus_set()
        self._entry.bind('<Return>', self._on_enter)

        self._entry_btn = tk.Button(self._button_frame, text="Enter", command=self._parse_command)
        self._entry_btn.grid(row=0, column=1)

        self._input_label = tk.Label(self._button_frame, text="Welcome to Halma!!!")
        self._input_label.grid(row=1, column=0)

        self._turn_text = tk.StringVar()
        self._turn_label = tk.Label(self._status_frame, textvariable=self._turn_text)
        self._turn_label.pack()

        self.update_status("Player {}".format("Red" if self._player_turn == 0 else "Green"))

        self._timer_text = tk.StringVar()
        self._timer_label = tk.Label(self._status_frame, textvariable=self._timer_text)
        self._timer_label.pack()

        self._root = root
        self._start_time = time.time()
        self.time_limit = t_limit
        self._root.after(1000, self.timer)
        self._pause = False
        self._best_move = []

        minutes, secs = divmod(self.time_limit, 60)
        self._timer_text.set("{:02d}:{:02d}".format(minutes, secs))

    def get_coord(self, pos):
        return "{}{}".format(chr(65 + pos[0]), self._size - pos[1])

    def get_tile_pos(self, coord):
        if not coord or len(coord) < 2 or len(coord) > 3:
            return None
        if ord(coord[0].upper()) - 65 < 0 or ord(coord[0].upper()) - 65 >= self._size:
            return None
        if int(coord[1:]) < 1 or int(coord[1:]) > self._size:
            return None

        return ord(coord[0].upper()) - 65, self._size - int(coord[1:])

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

    def _on_enter(self, event):
        self._parse_command()

    def _clear_input_label(self):
        self._input_label.config(text="")

    def _parse_command(self):
        cmd = self._entry.get()
        self._entry.delete(0, tk.END)
        error_delay = 2500
        if '->' not in cmd:
            print(cmd, "is not a valid command!", file=sys.stderr)
            self._input_label.config(text=cmd + " is not a valid command!")
            self._input_label.after(error_delay, self._clear_input_label)
            return
        old_coord, new_coord = re.split('->', cmd)

        old_pos = self.get_tile_pos(old_coord)
        new_pos = self.get_tile_pos(new_coord)

        if not old_pos:
            print(old_coord, "is not a valid coord!", file=sys.stderr)
            self._input_label.config(text=old_coord + " is not a valid coord!")
            self._input_label.after(error_delay, self._clear_input_label)
            return
        elif not new_pos:
            print(new_coord, "is not a valid coord!", file=sys.stderr)
            self._input_label.config(text=new_coord + " is not a valid coord!")
            self._input_label.after(error_delay, self._clear_input_label)
            return

        print(old_pos, new_pos)

        self.move(old_pos, new_pos)
        self._board.update(self.player1, self.player2)

    def _on_process_turn(self, event):
        # a way to figure out where should the piece be correctly placed at
        newX = (event.x - OFFSET_X) // TILE_SIZE
        newY = (event.y - OFFSET_Y) // TILE_SIZE

        dragged_piece = self._board.get_dragged_piece()

        self.move(dragged_piece[1], (newX, newY))
        self._board.update(self.player1, self.player2)

    def timer(self):
        delta = time.time() - self._start_time
        minutes, secs = divmod(round(self.time_limit - delta), 60)
        self._timer_text.set("{:02d}:{:02d}".format(minutes, secs))

        if delta >= self.time_limit:
            print("Time ended: next turn.")
            self.end_turn()
        elif not self._pause:
            self._root.after(1000, self.timer)

    def move(self, old, pos):
        print(self._board.findLegalMoves(old))
        error_delay = 2500
        # Not that player's turn
        if self._player_turn == 0:
            if old in self.player2:
                print("It's currently Red player's turn!", file=sys.stderr)
                self._input_label.config(text="It's currently Red player's turn!")
                self._input_label.after(error_delay, self._clear_input_label)
                return
            elif old not in self.player1:
                return
            elif old == pos:
                return
            elif pos not in self._board.findLegalMoves(old):
                print("Red Player: Illegal move.", file=sys.stderr)
                self._input_label.config(text="Red Player:s Illegal move.")
                self._input_label.after(error_delay, self._clear_input_label)
                return
            else:
                self.player1.remove(old)
                self.player1.append(pos)
        elif self._player_turn == 1:
            if old in self.player1:
                print("It's currently Green player's turn!", file=sys.stderr)
                self._input_label.config(text="It's currently Green player's turn!")
                self._input_label.after(error_delay, self._clear_input_label)
                return
            elif old not in self.player2:
                return
            elif old == pos:
                return
            elif pos not in self._board.findLegalMoves(old):
                print("Green Player: Illegal move.", file=sys.stderr)
                self._input_label.config(text="Green Player: Illegal move.")
                self._input_label.after(error_delay, self._clear_input_label)
                return
            else:
                self.player2.remove(old)
                self.player2.append(pos)

        print("Turn {:d}: Player {} {}->{}".format(self.turn_counter, "Red" if self._player_turn == 0 else "Green", self.get_coord(old), self.get_coord(pos)))
        self._input_label.config(text="Turn {:d}: Player {} {}->{}".format(self.turn_counter, "Red" if self._player_turn == 0 else "Green", self.get_coord(old), self.get_coord(pos)))
        self._input_label.after(error_delay, self._clear_input_label)
        print(self.player1)

        self.end_turn()

    def getScore(self, board, player):
        # needs to figure out a good way to get the score
        # my idea is to measure how close these pieces to the opponent region and
        # this just a simple idea
        pass

    def minimax(self, player, board, depth):
        availableMoves = set()

        # we want to first check if the node is a terminal node
        # if its a terminal node, we want to get the score
        # if depth is 0, then it's a terminal node
        if (depth == 0):
            return self.getScore(board, player)

        # since Green player plays first,,then Red player can be considered as an opponent
        # we want to minimize the value when opponent(Red player) plays
        # and maximize the value when Green player plays
        if (player == "Red"):
            beta = INFINITY

            # this part is not right, because we don't want to make change on the real player every time
            for piece in self.player1:
                availableMoves.add((piece, self._board.findLegalMoves(piece)))

            for position in availableMoves:
                oldPosition = position[0]
                newPosition = position[1]
                newBoard = deepcopy(board)

                # I think we don't want to move it on the real board every time
                # so I am leaving this part for now
                # todo
                # self.move(oldPosition, newPosition)

                temp = self.minimax("Green", newBoard, depth-1)
                if (temp < beta):
                    beta = temp

            return beta

        elif (player == "Green"):
            alpha = NEGATIVE_INFINITY

            # same as above, don't want to use self.player2
            for piece in self.player2:
                availableMoves.add((piece, self._board.findLegalMoves(piece)))

            for position in availableMoves:
                oldPosition = position[0]
                newPosition = position[1]
                newBoard = deepcopy(board)

                # todo
               # self.move(oldPosition, newPosition)

                temp = self.minimax("Red", newBoard, depth-1)
                if (temp < alpha):
                    alpha = temp

            return alpha


 #   def alphaBeta(self):
        # this one is really similar to the minimax, so I ll just leave this for now and
        # figure out the minimax first
        # todo

    def end_turn(self):
        if self._player_turn == 0:
            self._player_turn = 1
        elif self._player_turn == 1:
            self._player_turn = 0

        self.turn_counter += 1
        self._start_time = time.time()

        self.update_status("Player {}".format("Red" if self._player_turn == 0 else "Green"))

        if self.winning(self.zone2, self.player1):
            self._pause = True
            self._board.remove_events()
            self._timer_text.set("0:00")
            self.update_status("{} Player wins! {} Player loses!".format("Red", "Green"))
        elif self.winning(self.zone1, self.player2):
            self._pause = True
            self._board.remove_events()
            self._timer_text.set("0:00")
            self.update_status("{} Player wins! {} Player loses!".format("Green", "Red"))
        else:
            self._root.after(1000, self.timer)

        self._clear_input_label()
        self._entry.delete(0, tk.END)

    def winning(self, zone, player):
        if all(piece in zone for piece in player):
            return True
        return False
    
    def update_status(self, msg):
        self._turn_text.set("Turn {:d} - {}".format(self.turn_counter + 1, msg))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Halma!")
    parser.add_argument("--bsize", type=int, help="The board size (8, 10, 16)", choices=[8, 10, 12], dest="size")
    parser.add_argument("--t-limit", default=20, type=int, help="The time limit (in seconds)", dest="t_limit")
    parser.add_argument("--h-player", default="Green", help="The human player ('Red' or 'Green')", choices=["Red", "Green"], dest="color")
    parser.add_argument("--optional", type=open, help="An optional path to a board", dest="board_fp")

    args = parser.parse_args()

    root = tk.Tk()
    root.wm_title("Halma {0:d} x {0:d}".format(args.size))
    game = Game(args.size, args.t_limit, args.color, root)

    root.resizable(width=False, height=False)
    root.update()
    root.mainloop()
