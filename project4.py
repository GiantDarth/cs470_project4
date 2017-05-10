import tkinter as tk
from tkinter import messagebox
import sys
import time
import argparse
import math
from copy import deepcopy

LIGHT_SQUARE_COLOR = '#CCC'
DARK_SQUARE_COLOR = "#222"

RED_COLOR = "#BB578F"
GREEN_COLOR = "#B2D965"

RED_PLAYER_DARK_ZONE = "#D583B1"
RED_PLAYER_LIGHT_ZONE = "#E7AFCF"

GREEN_PLAYER_DARK_ZONE = "#D2F195"
GREEN_PLAYER_LIGHT_ZONE = "#E3F7BC"

GREEN_PLAYER = 1
RED_PLAYER = 0

OFFSET_X = 40
OFFSET_Y = 30

TILE_SIZE = 45
PIECE_SIZE_DIFF = 5

NUM_PIECES = {"8": 10, "10": 15, "16": 19}

class Board:
    def __init__(self, size, red_player_zone, green_player_zone, human_player, on_process_turn, on_non_human):
        self._view = tk.Frame()
        self._view.pack(fill=tk.BOTH, expand=1)
        self._size = size

        self._red_player_zone = red_player_zone[:]
        self._green_player_zone = green_player_zone[:]

        self._on_process_turn = on_process_turn
        self._on_non_human = on_non_human
        self._human_player = human_player
        self._init_view()
        self.add_events()

    def _init_view(self):
        self._canvas = tk.Canvas(self._view, bg="#477D92",
                                 width=OFFSET_X * 2 + TILE_SIZE * self._size,
                                 height=OFFSET_Y * 2 + TILE_SIZE * self._size)
        self._canvas.pack(expand=1)

        self._grid = [[None] * self._size] * self._size
        self._red_player = []
        self._red_player_pieces = []
        self._green_player = []
        self._green_player_pieces = []

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
                        if (x, y) in self._red_player_zone:
                            fill = RED_PLAYER_LIGHT_ZONE
                            tag = ("light", "zone1")
                        elif (x, y) in self._green_player_zone:
                            fill = GREEN_PLAYER_LIGHT_ZONE
                            tag = ("light", "zone2")
                        else:
                            fill = LIGHT_SQUARE_COLOR
                            tag = "light"
                    else:
                        if (x, y) in self._red_player_zone:
                            fill = RED_PLAYER_DARK_ZONE
                            tag = ("dark", "zone1")
                        elif (x, y) in self._green_player_zone:
                            fill = GREEN_PLAYER_DARK_ZONE
                            tag = ("dark", "zone2")
                        else:
                            fill = DARK_SQUARE_COLOR
                            tag = "dark"
                else:
                    if y % 2 == 0:
                        if (x, y) in self._red_player_zone:
                            fill = RED_PLAYER_DARK_ZONE
                            tag = ("dark", "zone1")
                        elif (x, y) in self._green_player_zone:
                            fill = GREEN_PLAYER_DARK_ZONE
                            tag = ("dark", "zone2")
                        else:
                            fill = DARK_SQUARE_COLOR
                            tag = "dark"
                    else:
                        if (x, y) in self._red_player_zone:
                            fill = RED_PLAYER_LIGHT_ZONE
                            tag = ("light", "zone1")
                        elif (x, y) in self._green_player_zone:
                            fill = GREEN_PLAYER_LIGHT_ZONE
                            tag = ("light", "zone2")
                        else:
                            fill = LIGHT_SQUARE_COLOR
                            tag = "light"
                self._grid[x][y] = self._canvas.create_rectangle(x * TILE_SIZE + OFFSET_X, y * TILE_SIZE + OFFSET_Y,
                                                                 (x + 1) * TILE_SIZE + OFFSET_X, (y + 1) * TILE_SIZE + OFFSET_Y,
                                                                 outline="#fff", fill=fill, tags=tag)

    def add_events(self):
        human_tag = "player1" if self._human_player == RED_PLAYER else "player2"
        non_human_tag = "player2" if self._human_player == RED_PLAYER else "player1"

        self._canvas.tag_bind(human_tag, "<ButtonPress-1>", self._onPressDown)
        self._canvas.tag_bind(human_tag, "<B1-Motion>", self._onMove)
        self._canvas.tag_bind(human_tag, "<ButtonRelease-1>", self._on_process_turn)

        self._canvas.tag_bind(non_human_tag, "<ButtonPress-1>", self._on_non_human)

    def remove_events(self):
        for tag in ["player1", "player2"]:
            self._canvas.tag_unbind(tag, "<ButtonPress-1>")
            self._canvas.tag_unbind(tag, "<B1-Motion>")
            self._canvas.tag_unbind(tag, "<ButtonRelease-1>")

    def _onPressDown(self, event):
        piece = self._canvas.find_closest(event.x, event.y)
        if "piece" not in self._canvas.gettags(piece):
            return

        oldX = (event.x - OFFSET_X) // TILE_SIZE
        oldY = (event.y - OFFSET_Y) // TILE_SIZE

        self._dragged_piece = (piece, (oldX, oldY))
        self._current_drag_pos = [event.x, event.y]

    def _onMove(self, event):
        delta = [event.x - self._current_drag_pos[0], event.y - self._current_drag_pos[1]]
        self._canvas.move(self._dragged_piece[0], delta[0], delta[1])
        self._current_drag_pos = (event.x, event.y)

    def update(self, red_player, green_player):
        self._red_player = red_player[:]
        self._green_player = green_player[:]

        for piece in self._red_player_pieces:
            self._canvas.delete(piece)
        for piece in self._green_player_pieces:
            self._canvas.delete(piece)

        self._red_player_pieces = [self._canvas.create_oval(x * TILE_SIZE + OFFSET_X + PIECE_SIZE_DIFF,
                                                            y * TILE_SIZE + OFFSET_Y + PIECE_SIZE_DIFF,
                                                            (x + 1) * TILE_SIZE + OFFSET_X - PIECE_SIZE_DIFF,
                                                            (y + 1) * TILE_SIZE + OFFSET_Y - PIECE_SIZE_DIFF,
                                                            fill=RED_COLOR, tag=("piece", "player1")) for (x, y) in red_player]
        self._green_player_pieces = [self._canvas.create_oval(x * TILE_SIZE + OFFSET_X + PIECE_SIZE_DIFF,
                                                              y * TILE_SIZE + OFFSET_Y + PIECE_SIZE_DIFF,
                                                              (x + 1) * TILE_SIZE + OFFSET_X - PIECE_SIZE_DIFF,
                                                              (y + 1) * TILE_SIZE + OFFSET_Y - PIECE_SIZE_DIFF,
                                                              fill=GREEN_COLOR, tag=("piece", "player2")) for (x, y) in green_player]

    def get_dragged_piece(self):
        return self._dragged_piece

    def _is_tile_empty(self, x, y):
        return (x, y) not in self._red_player and (x, y) not in self._green_player

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
    def __init__(self, size, t_limit, color, root, strategy, depth):
        self._size = size
        self.status = [] # will be set to status widget when created

        self._status_frame = tk.Frame()
        self._status_frame.pack()

        self.red_player_zone = self._get_zone("SW")
        self.red_player = self.red_player_zone[:]

        # Add player starting positions
        self.green_player_zone = self._get_zone("NE")
        self.green_player = self.green_player_zone[:]

        if color == "Red":
            self._human_player = RED_PLAYER
            self._non_human_player = GREEN_PLAYER
        elif color == "Green":
            self._human_player = GREEN_PLAYER
            self._non_human_player = RED_PLAYER
        else:
            print(sys.stderr, "Invalid human player used for Game")
            sys.exit(1)

        self._board = Board(self._size, self.red_player_zone, self.green_player_zone, self._human_player, self._on_process_turn, self._on_non_human)
        self._board.update(self.red_player, self.green_player)

        self._player_turn = GREEN_PLAYER
        self.ply_counter = 0

        self._button_frame = tk.Frame()
        self._button_frame.pack()

        self._pause_btn = tk.Button(self._button_frame, text="Pause", command=self._toggle_pause)
        self._pause_btn.grid(row=0, column=0)

        self._next_turn_btn = tk.Button(self._button_frame, text="Skip Turn", command=self.end_turn)
        self._next_turn_btn.grid(row=0, column=2)

        self._input_label = tk.Label(self._button_frame, text="Welcome to Halma!!!")
        self._input_label.grid(row=1, column=1)

        self._turn_text = tk.StringVar()
        self._turn_label = tk.Label(self._status_frame, textvariable=self._turn_text)
        self._turn_label.pack()

        self.update_status("Player {}".format("Red" if self._player_turn == RED_PLAYER else "Green"))

        self._timer_text = tk.StringVar()
        self._timer_label = tk.Label(self._status_frame, textvariable=self._timer_text)
        self._timer_label.pack()

        self._score_text = tk.StringVar()
        self._score_label = tk.Label(self._status_frame, textvariable=self._score_text)
        self._score_label.pack()

        self.update_score(self.get_final_score(0), self.get_final_score(1))

        self._root = root
        self._start_time = time.time()
        self._pause_time = self._start_time
        self.time_limit = t_limit
        self._pause = False
        self._timer_job = None
        self._clear_job = None
        self.timer()
        self._best_move = ()
        self._depth = depth
        self._strategy = strategy

        minutes, secs = divmod(self.time_limit, 60)
        self._timer_text.set("{:02d}:{:02d}".format(minutes, secs))

        if self._player_turn != self._human_player:
            self.non_human_player_process_turn()

    def non_human_player_process_turn(self):
        self._next_turn_btn.config(state=tk.DISABLED, text="End Turn")

        human_pieces = self.red_player if self._human_player == RED_PLAYER else self.green_player
        non_human_pieces = self.red_player if self._non_human_player == RED_PLAYER else self.green_player

        if self._strategy == "minimax":
            self.minimax(True, human_pieces, non_human_pieces, 0)
            old = self._best_move[0]
            new = self._best_move[1]
        elif self._strategy == "alpha-beta":
            self.alphaBeta(True, human_pieces, non_human_pieces, 0, float("-inf"), float("inf"))
            old = self._best_move[0]
            new = self._best_move[1]
        else:
            return

        self._pause = True
        self._root.after_cancel(self._timer_job)

        self.move(old, new)
        print([old, new])

        messagebox.showinfo("Non-Human Player Turn Done", "{} -> {}".format(self.get_coord(old), self.get_coord(new)))
        self._next_turn_btn.config(state=tk.NORMAL, text="End Turn")

        new_red_pieces = human_pieces if self._human_player == RED_PLAYER else non_human_pieces
        new_green_pieces = human_pieces if self._human_player == GREEN_PLAYER else non_human_pieces

        self._board.update(new_red_pieces, new_green_pieces)

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

    def _clear_input_label(self):
        self._input_label.config(text="")

    def _toggle_pause(self):
        self._pause = not self._pause
        self._pause_btn.config(text="Pause" if not self._pause else "Unpause")

        if self._pause:
            self._pause_time = time.time()
            self._root.after_cancel(self._timer_job)
            self._next_turn_btn.config(state=tk.DISABLED)
        else:
            self._start_time += time.time() - self._pause_time
            self.timer()
            self._next_turn_btn.config(state=tk.NORMAL)

    def _on_non_human(self, event):
        if self._human_player == self._player_turn:
            self._input_label.config(text="You're {} player".format("Red" if self._human_player == RED_PLAYER else "Green"))
        else:
            self._input_label.config(text="Not your turn!")
        self._input_label.after(2500, self._clear_input_label)

    def _on_process_turn(self, event):
        # a way to figure out where should the piece be correctly placed at
        newX = (event.x - OFFSET_X) // TILE_SIZE
        newY = (event.y - OFFSET_Y) // TILE_SIZE

        dragged_piece = self._board.get_dragged_piece()

        if self.move(dragged_piece[1], (newX, newY)):
            self._pause_btn.config(state=tk.DISABLED)
            self._next_turn_btn.config(text="End Turn")

            self._board.remove_events()

        self._board.update(self.red_player, self.green_player)

    def timer(self):
        delta = time.time() - self._start_time
        minutes, secs = divmod(round(self.time_limit - delta), 60)

        text = ""
        if minutes < 0:
            text = "-{:02d}:{:02d}".format(abs(math.ceil((self.time_limit - delta) / 60)), -round(self.time_limit - delta) % 60)
        else:
            text = "{:02d}:{:02d}".format(minutes, secs)

        if not self._pause:
            self._timer_job = self._root.after(1000, self.timer)
        else:
            text = "Paused! " + text

        self._timer_text.set(text)

    def move(self, old, pos):
        error_delay = 2500
        if self._player_turn == RED_PLAYER:
            if old in self.green_player:
                print("It's currently Red player's turn!", file=sys.stderr)
                self._input_label.config(text="It's currently Red player's turn!")
                self._input_label.after(error_delay, self._clear_input_label)
                return False
            elif old not in self.red_player:
                return False
            elif old == pos:
                return False
            elif pos not in self._board.findLegalMoves(old):
                print("Red Player: Illegal move.", file=sys.stderr)
                self._input_label.config(text="Red Player:s Illegal move.")
                self._clear_job = self._input_label.after(error_delay, self._clear_input_label)
                return False
            else:
                self.red_player.remove(old)
                self.red_player.append(pos)
        elif self._player_turn == GREEN_PLAYER:
            if old in self.red_player:
                print("It's currently Green player's turn!", file=sys.stderr)
                self._input_label.config(text="It's currently Green player's turn!")
                self._clear_job = self._input_label.after(error_delay, self._clear_input_label)
                return False
            elif old not in self.green_player:
                return False
            elif old == pos:
                return False
            elif pos not in self._board.findLegalMoves(old):
                print("Green Player: Illegal move.", file=sys.stderr)
                self._input_label.config(text="Green Player: Illegal move.")
                self._clear_job =  self._input_label.after(error_delay, self._clear_input_label)
                return False
            else:
                self.green_player.remove(old)
                self.green_player.append(pos)

        if self._clear_job:
            self._input_label.after_cancel(self._clear_job)

        print("Ply {:d}: Player {} {}->{}".format(self.ply_counter + 1, "Red" if self._player_turn == RED_PLAYER else "Green", self.get_coord(old), self.get_coord(pos)))
        self._input_label.config(text="Ply {:d}: Player {} {}->{}".format(self.ply_counter + 1, "Red" if self._player_turn == RED_PLAYER else "Green", self.get_coord(old), self.get_coord(pos)))
        print(self.red_player)

        return True

    @staticmethod
    def _get_distance(self, other):
        return math.sqrt((self[0] - other[0])**2 + (self[1] - other[1])**2)

    @staticmethod
    def _get_shortest_distance(piece, zone):
        return min(Game._get_distance(piece, tile) for tile in zone)

    def get_final_score(self, player):
        if player == RED_PLAYER:
            pieces_in_goal = set(self.red_player) & set(self.green_player_zone)
            pieces_outside_goal = set(self.red_player) - set(self.green_player_zone)

            return len(pieces_in_goal) + 1 / sum(
                Game._get_shortest_distance(piece, self.green_player_zone) for piece in pieces_outside_goal)
        elif player == GREEN_PLAYER:
            pieces_in_goal = set(self.green_player) & set(self.red_player_zone)
            pieces_outside_goal = set(self.green_player) - set(self.red_player_zone)

            return len(pieces_in_goal) + 1 / sum(
                Game._get_shortest_distance(piece, self.red_player_zone) for piece in pieces_outside_goal)
        else:
            return float("nan")

    # The "Utility" function
    def evalulation_func(self, player, pieces):
        # If Red Player
        if player == RED_PLAYER:
            return sum(Game._get_shortest_distance(piece, self.red_player_zone) for piece in pieces)
        # If Green Player
        elif player == GREEN_PLAYER:
            return sum(Game._get_shortest_distance(piece, self.green_player_zone) for piece in pieces)
        else:
            return float("nan")

    def minimax(self, max_player, human_pieces, non_human_pieces, depth):
        # Forcefully updates the window, keeps the interface from hanging
        self._root.update()

        availableMoves = []

        # we want to first check if the node is a terminal node
        # if its a terminal node, we want to get the score
        if depth == self._depth:
            player = self._non_human_player if max_player else self._human_player
            pieces = non_human_pieces if max_player else human_pieces

            return self.evalulation_func(player, pieces)

        if max_player:
            best_value = float("-inf")

            # this part is not right, because we don't want to make change on the real player every time
            for piece in non_human_pieces:
                availableMoves.append((piece, self._board.findLegalMoves(piece)))

            for move in availableMoves:
                old_position = move[0]
                new_positions = move[1]

                # there are a lot of choices for new positions
                for pos in new_positions:
                    new_pieces = non_human_pieces[:]
                    new_pieces.remove(old_position)
                    new_pieces.append(pos)

                    temp = self.minimax(not max_player, human_pieces, new_pieces, depth + 1)
                    if temp > best_value:
                        best_value = temp
                        if depth == 0:
                            self._best_move = old_position, pos

            return best_value
        else:
            best_value = float("inf")

            # this part is not right, because we don't want to make change on the real player every time
            for piece in human_pieces:
                availableMoves.append((piece, self._board.findLegalMoves(piece)))

            for move in availableMoves:
                old_position = move[0]
                new_positions = move[1]

                # there are a lot of choices for new positions
                for pos in new_positions:
                    new_pieces = human_pieces[:]
                    new_pieces.remove(old_position)
                    new_pieces.append(pos)

                    temp = self.minimax(not max_player, new_pieces, non_human_pieces, depth + 1)
                    if temp < best_value:
                        best_value = temp
                        if depth == 0:
                            self._best_move = old_position, pos

            return best_value

    def alphaBeta(self, max_player, human_pieces, non_human_pieces, depth, alpha, beta):
        # Forcefully updates the window, keeps the interface from hanging
        self._root.update()

        availableMoves = []

        # we want to first check if the node is a terminal node
        # if its a terminal node, we want to get the score
        if depth == self._depth:
            player = self._non_human_player if max_player else self._human_player
            pieces = non_human_pieces if max_player else human_pieces

            return self.evalulation_func(player, pieces)

        if max_player:
            # this part is not right, because we don't want to make change on the real player every time
            for piece in non_human_pieces:
                availableMoves.append((piece, self._board.findLegalMoves(piece)))

            for move in availableMoves:
                old_position = move[0]
                new_positions = move[1]

                # there are a lot of choices for new positions
                for pos in new_positions:
                    new_pieces = non_human_pieces[:]
                    new_pieces.remove(old_position)
                    new_pieces.append(pos)

                    temp = self.alphaBeta(not max_player, human_pieces, new_pieces, depth + 1, alpha, beta)
                    if temp > alpha:
                        alpha = temp
                        if depth == 0:
                            self._best_move = old_position, pos

                    if alpha >= beta:
                        return alpha

            return alpha
        else:
            # this part is not right, because we don't want to make change on the real player every time
            for piece in human_pieces:
                availableMoves.append((piece, self._board.findLegalMoves(piece)))

            for move in availableMoves:
                old_position = move[0]
                new_positions = move[1]

                # there are a lot of choices for new positions
                for pos in new_positions:
                    new_pieces = human_pieces[:]
                    new_pieces.remove(old_position)
                    new_pieces.append(pos)

                    temp = self.alphaBeta(not max_player, new_pieces, non_human_pieces, depth + 1, alpha, beta)
                    if temp < beta:
                        beta = temp
                        if depth == 0:
                            self._best_move = old_position, pos

                    if alpha >= beta:
                        return beta

            return beta

    def end_turn(self):
        if self._player_turn == RED_PLAYER:
            self._player_turn = GREEN_PLAYER
        elif self._player_turn == GREEN_PLAYER:
            self._player_turn = RED_PLAYER

        self.ply_counter += 1
        self._start_time = time.time()

        self.update_status("Player {}".format("Red" if self._player_turn == RED_PLAYER else "Green"))
        self.update_score(self.get_final_score(0), self.get_final_score(1))

        self._clear_input_label()

        if self.winning(self.green_player_zone, self.red_player) or self.winning(self.red_player_zone, self.green_player):
            self._pause = True
            self._board.remove_events()
            self._pause_btn.config(state=tk.DISABLED)
            self._next_turn_btn.config(state=tk.DISABLED)

            if self.winning(self.green_player_zone, self.red_player):
                self.update_status("{} Player wins! {} Player loses!".format("Red", "Green"))
            elif self.winning(self.red_player_zone, self.green_player):
                self.update_status("{} Player wins! {} Player loses!".format("Green", "Green"))
        else:
            self._pause_btn.config(state=tk.NORMAL)
            self._next_turn_btn.config(text="Skip Turn")

            if self._pause:
                self._pause = False
                self.timer()

            if self._player_turn != self._human_player:
                self.non_human_player_process_turn()

                self._board.add_events()


    def winning(self, zone, player):
        return all(piece in zone for piece in player)
    
    def update_status(self, msg):
        self._turn_text.set("Turn {:d}, Ply {:d} - {}".format(self.ply_counter // 2 + 1, self.ply_counter + 1, msg))
        
    def update_score(self, red_player_score, green_player_score):
        self._score_text.set("Red: {:f} - Green: {:f}".format(red_player_score, green_player_score))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Halma!")
    parser.add_argument("--bsize", type=int, help="The board size (8, 10, 16)", choices=[8, 10, 16], dest="size")
    parser.add_argument("--t-limit", default=20, type=int, help="The time limit (in seconds)", dest="t_limit")
    parser.add_argument("--h-player", default="Green", help="The human player ('Red' or 'Green')", choices=["Red", "Green"], dest="color")
    parser.add_argument("--optional", type=open, help="An optional path to a board", dest="board_fp")

    args = parser.parse_args()

    root = tk.Tk()
    root.wm_title("Halma {0:d} x {0:d}".format(args.size))
    game = Game(args.size, args.t_limit, args.color, root, "alpha-beta", 3)

    root.resizable(width=False, height=False)
    root.update()
    root.mainloop()
