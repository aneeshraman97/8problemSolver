from Queue import PriorityQueue
import curses
import time
import random

DIRECTIONS = ["left","right","up","down"];
COL_SIZE = 3;
ROW_SIZE = 3;
MAX_VALUE_SIZE = 9;

GOAL_STATE = [[1,2,3],[8,0,4],[7,6,5]];

def generate_random_initial_state(board):
    
    placed_numbers = [];
    
    for i in range (0,ROW_SIZE):
        for j in range (0,COL_SIZE):
            probable_value = random.randint(0,MAX_VALUE_SIZE);
            while(probable_value not in placed_numbers):
                board[i][j] = probable_value;
                placed_numbers.append(board[i][j]);
    
    return board;
            

class Board(object):
    
    board=[[]];
    
    def __init__(self, board=None, moves=0, previous=None):
        
        if board is not None:
            self.board = board;
        else:
            self.board = generate_random_initial_state(self.board);
            
        self.previous = previous;
        self.moves = moves;
        

    def has_reached_goal_state(self):
        
        return self.equals(GOAL_STATE);
        
    def equals(self,anotherBoard):
        
        if anotherBoard is None:
            return False;
        else:
            return self.board == anotherBoard.board;
            
    def find_empty_tile(self):
        
        for i in range(0, ROW_SIZE):
            for j in range(0, COL_SIZE):
                if self.board[i][j] == 0:
                    return i,j
                    
        return None;
        
    def switch_move_condition(self, direction, empty_tile_coordinates):
        
        if empty_tile_coordinates is None:
            return None;
            
        row = empty_tile_coordinates[0];
        col = empty_tile_coordinates[1];
        
        switcher = {
            "left": row % ROW_SIZE != 0,
            "right": row % ROW_SIZE != 2,
            "up": col % COL_SIZE != 0,
            "down": col % COL_SIZE != 2
        }
        
        return switcher.get(direction,None)
        
    