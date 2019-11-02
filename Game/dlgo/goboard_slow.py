import numpy as np

import copy
from dlgo.gotypes import Player
from dlgo.gotypes import Point
from dlgo.scoring import compute_game_result
import time

__all__ = [
    'Board',
    'GameState',
    'Move',
]

class IllegalMoveError(Exception):
    pass

# String Class as a structure of the board
# Go strings are stones that are linked by a chain of connected stones of the same color.
# Return a new Go string containing all stones in both strings.
class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)
    
    def add_liberty(self, point):
        self.liberties.add(point)

    # Merge two adjacent strings
    def merged_with(self, go_string):
        assert (go_string.color == self.color)
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
        (self.liberties | go_string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    # Check redundant strings
    def __eq__(self, other):
        return (isinstance(other, GoString)) and \
            (self.color == other.color) and \
            (self.stones == other.stones) and \
            (self.liberties == other.liberties)

# Board Class as a grid
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    # Check valid coordinates for a point
    def is_on_grid(self, point):
        return (1 <= point.row <= self.num_rows) and \
            (1 <= point.col <= self.num_cols)
    
    # Get stone color
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color
    
    # Get connected group 
    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string
    
    # Remove zero liberty groups
    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                # Add liberty to the adjacent
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)

            del(self._grid[point])

    # Place a stone on the board
    def place_stone(self, player, point, prisoners):
        # Check if a point is valid inside the board
        assert self.is_on_grid(point)
        # Check if a point is free to play
        assert self._grid.get(point) is None
        
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        
        # Check direct neighbors
        for neighbor in point.neighbors():
            # Check if a neighbor is valid inside the board
            if not self.is_on_grid(neighbor):
                continue
            # Get neighbor's string
            neighbor_string = self._grid.get(neighbor)
            # If the neighbor is empty then it's a liberty
            if neighbor_string is None:
                liberties.append(neighbor)
            # If the neighbor is same as you
            elif neighbor_string.color == player:
                # The neighbor isn't traversed before then traverse it
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                # If the neighbor is an opponent and isn't traversed before then traverse it
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)

        # Create a string with the new stone
        new_string = GoString(player, [point], liberties)
        
        # Merge the new stone with the friendly adjacent neighbors
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        
        # Place the stones on the grid
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        
        # Remove liberties from any adjacent opponent
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        
        # Remove any group of adjacent opponent if its liberties is zero
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                prisoners.append(len(other_color_string.stones))
                self._remove_string(other_color_string)

    def __eq__(self, other):
        return isinstance(other, Board) and \
            self.num_rows == other.num_rows and \
            self.num_cols == other.num_cols and \
            self._grid == other._grid

# Move Class
class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign
    
    # Play a move
    @classmethod
    def play(cls, point):
        return Move(point=point)
    
    # Pass the turn
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    
    # Resign from the game
    @classmethod
    def resign(cls):
        return Move(is_resign=True)

# Game State Class
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_over(self):
        # Start a game
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        # After first play
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        # Two consecutive passes
        return self.last_move.is_pass and second_last_move.is_pass

    # Returns a game state and number of number of captured stones
    def apply_move(self, move):
        prisoners = []
        # If a player places a stone
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point, prisoners)
        # If a player passes his turn 
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move),prisoners

    # Prevent self-capture or suicide moves
    def is_move_self_capture(self, player, move):
        prisoners = []
        if not move.is_play:
            return False
        # Copy the board first to check any captures that will regain more libreties
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point, prisoners)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    # Prevent Ko
    @property
    def situation(self):
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        prisoners = []
        if not move.is_play:
            return False
        # Copy the next state to check whether it was played before or not
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point, prisoners)
        next_situation = (player.other, next_board)
        past_state = self.previous_state

        # Loop over the whole previous history
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        return False

    # Prevent a move that leads to self-capture and ko
    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        # If a point is empty and not self-capture play and follow ko rule
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))

    # Available moves to play + pass + resign
    def legal_moves(self):
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal.
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves
    def semi_winner(self,captures):
        if self.last_move.is_resign:
            return self.next_player ,0
        game_result,score = compute_game_result(self,captures)
        return game_result.winner,score

    def winner(self,captures):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        
        game_result,score = compute_game_result(self,captures)
        return game_result.winner,score