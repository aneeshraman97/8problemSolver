from queue import PriorityQueue
import curses
import time
import random
from scipy.spatial.distance import cdist
import numpy as np

DIRECTIONS = ["left","right","up","down"];
COL_SIZE = 3;
ROW_SIZE = 3;
MAX_VALUE_SIZE = 8;

GOAL_STATE = [[1,2,3],[8,0,4],[7,6,5]];
GOAL_STATE_POSITIONS = [[1,0,0],[2,0,1],[3,0,2],[4,1,2],[5,2,2],[6,2,1],[7,2,0],[8,1,0]];

def generate_random_initial_state(board):
    
    placed_numbers = [];
    
    for i in range (0,ROW_SIZE):
        for j in range (0,COL_SIZE):
            probable_value = random.randint(0,MAX_VALUE_SIZE);
            if probable_value in placed_numbers:
                while True:
                    probable_value = random.randint(0,MAX_VALUE_SIZE);
                    if(probable_value not in placed_numbers):
                        board[i][j] = probable_value;
                        placed_numbers.append(board[i][j]);
                        break;
                    
            else:
                board[i][j] = probable_value;
                placed_numbers.append(board[i][j]);
    
    return board;
            

class Board(object):
    
    board=[[0,0,0],[0,0,0],[0,0,0]];
    
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
        elif isinstance(anotherBoard, Board):
            return self.board == anotherBoard.board;
        else:
            return self.board == anotherBoard;
            
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
            "left": col % ROW_SIZE != 0,
            "right": col % ROW_SIZE != 2,
            "up": row % COL_SIZE != 0,
            "down": row % COL_SIZE != 2
        }
        
        return switcher.get(direction,None)
        
    
    def move_empty_tile(self,direction):
        
        empty_tile_coordinates = self.find_empty_tile();
        print("cond",self.switch_move_condition(direction, empty_tile_coordinates), empty_tile_coordinates, direction)
        if(self.switch_move_condition(direction, empty_tile_coordinates)):
            self.move_operation(direction, empty_tile_coordinates);
            
    
    def move_operation(self,direction,empty_tile_coordinates):
        
        row, column = self.get_destination_coordinates(direction, empty_tile_coordinates);
        
        if row is not None and column is not None:
            self.exchange_tiles(empty_tile_coordinates, [row,column]);
    
    def get_destination_coordinates(self,targetDirection,empty_tile_coordinates):
        
        if empty_tile_coordinates is None:
            return None;
        
        if targetDirection not in DIRECTIONS:
            return None;
            
        row = empty_tile_coordinates[0];
        col = empty_tile_coordinates[1];
        
        if targetDirection == "left" :
            return row, (col % 3) - 1;
        
        elif targetDirection == "right" :
            return row, (col % 3) + 1;
            
        elif targetDirection == "up" :
            return (row % 3) - 1, col;
            
        elif targetDirection == "down":
            return (row % 3) + 1, col;
            
    
    def exchange_tiles(self,source,destination):
        #print("dest",destination)
        source_value = self.board[source[0]][source[1]];
        destination_value = self.board[destination[0]][destination[1]];
        
        self.board[source[0]][source[1]], self.board[destination[0]][destination[1]] = destination_value, source_value;
        
    
    def clone_board(self):
        
        return Board(self.board.copy(), self.moves+1, self);
        
    
    def get_valid_neighbors(self):
        
        empty_tile_coordinates = self.find_empty_tile();
        
        valid_neighbors = [];
        
        for direction in DIRECTIONS:
            if(self.switch_move_condition(direction, empty_tile_coordinates)):
                new_board = self.clone_board();
                new_board.move_empty_tile(direction);
                valid_neighbors.append(new_board);
                
        return valid_neighbors;
        
        
    def get_manhattan_distance(self):
        
        manhattan_distance = 0;
        
        board_1d = np.array(self.board).flatten();
        for i in range(0, ROW_SIZE):
            for j in range(0, COL_SIZE):
                if self.board[i][j] != 0:
                    final_row, final_column = find_final_position(self.board[i][j]);
                    manhattan_distance += abs(final_row - i) + abs(final_column - j);
            
        return manhattan_distance;
                    
                    
    def place_into_priority_queue(self,count):
        
        return self.moves + self.get_manhattan_distance(), count, self;
        
    
    def get_board_as_string(self):
        
        string = "";
        string += "+===+===+===+\n";
        
        for i in range(0,ROW_SIZE):
            for j in range(0,COL_SIZE):
                tile = self.board[i][j];
                string+= "| {} ".format(" " if tile==0 else tile);
                #string+="|\n";
            string+="\n+===+===+===+\n";
                
        return string;
        
        
    def get_all_previous_states(self):
        
        all_previous_states = [self];
        previous_state = self.previous; 
        
        while previous_state is not None:
            all_previous_states.append(previous_state);
            previous_state = previous_state.previous;
            
        all_previous_states.reverse();
        return all_previous_states;
        
def find_final_position(value):
    
    
    for i in range(len(GOAL_STATE_POSITIONS)):
        if GOAL_STATE_POSITIONS[i][0] == value:
            return GOAL_STATE_POSITIONS[i][1],GOAL_STATE_POSITIONS[i][2];
            
    
def get_coordinates(empty_tile_coordinates):
    
    return empty_tile_coordinates[0],[1];
    

def direction_switcher(intercept,value):
    
    x_switch={
      1:"Move Left",
      -1: "Move Right"
    };
    
    y_switch={
      1:"Move Up",
      -1: "Move Down"
    };
    
    if(intercept=="x"):
        return x_switch.get(value,None);
    
    elif(intercept=="y"):
        return y_switch.get(value,None);
        

def describe_move(board1,board2):
    
    if board1 is None:
        return "Initial State";
        
    if board2 is None:
        return " ";
            
   
    source_row,source_column=get_coordinates(board1.find_empty_tile());
    destination_row,destination_column=get_coordinates(board2.find_empty_tile());
    
    x_direction=source_column-destination_column;
    y_direction=source_row-destination_row;
    
    described_move=direction_switcher("x",x_direction);
    
    if(described_move is not None):
        return described_move;
 
    described_move=direction_switcher("y",y_direction);
    return described_move;
    
def solve(initial_state):
    
    queue = PriorityQueue();
    queue.put(initial_state.place_into_priority_queue(0));
    
    i = 1;
    while not queue.empty():
        board = queue.get()[2];
        print(board.get_board_as_string())
        if not board.has_reached_goal_state():
            
            for neighbor in board.get_valid_neighbors():
                
                #if(neighbor != board.previous):
                if(not neighbor.equals(board.previous)):
                    
                    queue.put(neighbor.place_into_priority_queue(i));
                    i += 1;
                
            break;
        else:
            return board.get_all_previous_states();
        
    return None;
    
    
    
def main():
    
    initial = Board();
    
    print(initial.get_board_as_string())
    
    moves = solve(initial);
    
    prev = None;
    steps = [];
    
 
    for move in moves:
        print(describe_move(prev,move));
        print(move.get_board_as_string());
        prev = move;
       
    
    
if __name__ == '__main__':
    main();
    