from pdb import line_prefix
import pygame
from pathlib import Path

#Legality Logic Explained:
#Tiers are for understanding what code does which action. Checks may move between tiers and are NOT perfectly sequential in execution!
#Tier 1: How a peace moves according to the rules of chess e.g. Knight moves like an "L" 
#Tier 2: Exceptional moves (Pawn capture, En passant, Castling) 
#Tier 3: Is the move within bounds of the board?
#Tier 4: Is the move "blocked" by another piece? Pieces may not travel through other pieces. (This tier doesn't apply to the knight) Special mention for castling where the method is written
#Tier 5: Does this move cause the current player to check themselves? A player isn't allowed to check themselves.
#Tier 6: If the player is in Check, is the move still legal?
    #e.g The player must "stop" the check. When this isn't possible the game is already over anyway as this is checked at the end of the previous player's turn
#Any move created from Tier 1 and 2 that passes all checks can be considered to be a "Candidate Move" and is allowed to be played

board_files = ["A","B","C","D","E","F","G","H"] #all files/collumnes on a chess board

#COLOUR THEN PIECE LETTER. 00 represents empty square 
#Only exists as documentation for what format the board is represented in and isn't used in the program
test_board = [
    ["WR","WP","00","00","00","00","BP","BR"],
    ["WN","WP","00","00","00","00","BP","BN"],
    ["WB","WP","00","00","00","00","BP","BB"],
    ["WQ","WP","00","00","00","00","BP","BQ"],
    ["WK","WP","00","00","00","00","BP","BK"],
    ["WB","WP","00","00","00","00","BP","BB"],
    ["WN","WP","00","00","00","00","BP","BN"],
    ["WR","WP","00","00","00","00","BP","BR"]
    ]

#pos always refers a coordinate 
class Pos: #cba to find import for co-ordinates

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if (isinstance(other, Pos)):
            return self.x == other.x and self.y == other.y
        return False

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)  
    #__radd__ not needed as only 2 Pos can be added. Pos + int or int + Pos is not supported!

    def isFriendly(self, piece):
        return Game.readSquare(self)[0] == piece.colour[0]
    
    def isHostile(self, piece):
        return not self.isFriendly(piece) and Game.readSquare(self) != "00" #if it's not friendly and not neutral it's hostile!

    #checks if the position is on the board
    def isValid(self):
        return self.x >= 0 and self.x < 8 and self.y >= 0 and self.y < 8

    def toSqu(self):
        return Squ(board_files[self.x], self.y + 1)

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "]"


#squ always refers to a square as people see it e.g. E4
#The letter represents the file/collumn/x_pos while the number represents the rank/row/y_pos. This is common chess terminology.
class Squ:

    def __init__(self, file, rank):
        self.file = file
        self.rank = rank

    def __eq__(self, other):
        if (isinstance(other, Pos)):
            return self.file == other.file and self.rank == other.rank
        return False

    #checks if the square exists on the board
    def isValid(self):
        return self.file in board_files and self.rank >= 0 and self.rank < 9
    
    #convert Squ to Pos. Does NOT check for validity! Input must be valid
    def toPos(self):
        counter = -1
        for file in board_files:
            counter += 1
            if self.file == file:
                break
        return Pos(counter, self.rank - 1)
    
    def __str__(self):
        return self.file + str(self.rank)


#interface (the oop kind)
class Piece:
    total_pieces = 0
    piece_dict = { #stores object references themselves
        "White" : [],
        "Black" : [],
        "Captured by White" : [], #all pieces here are black
        "Captured by Black" : []  #all pieces here are white
    }

    def __init__(self, x, y, colour, letter):
        self.pos = Pos(x, y)
        self.colour = colour
        self.letter = letter
        self.possible_moves = []
        other_info = Game.board[x][y]
        Game.board[x][y] = colour[0] + letter[0] + other_info #has_moved and is_promoted symbols are written before but need to come after piece and colour symbols
        Piece.total_pieces += 1

    def __eq__(self, other):
        if (isinstance(other, Pos)):
            return self.letter == other.letter and self.colour == other.colour
        return False

    def __str__(self):
        return self.colour + self.letter

    #all checks applied normally
    def moveTo(self, new_pos):
        if new_pos in self.possible_moves:
            Game.update_pgn(self, new_pos)
            init_pos_entry = Game.readSquare(self.pos)
            Game.writeSquare(self.pos, "00")
            self.pos = new_pos
            if self.letter == "P" or self.letter == "K" or self.letter == "R":
                if not self.has_moved:
                    self.has_moved = True
                    init_pos_entry.rstrip(init_pos_entry[-1])
            Game.writeSquare(self.pos, init_pos_entry)

    #no checks made
    def moveToAnarchy(self, new_pos):
        init_pos_entry = Game.readSquare(self.pos)
        Game.writeSquare(self.pos, "00")
        self.pos = new_pos
        Game.writeSquare(self.pos, init_pos_entry)


class Knight(Piece):

    letter = "N"
    value = 3

    def __init__(self, x, y, colour, is_promoted):
        self.is_promoted = is_promoted
        if is_promoted:
            Game.board[x][y] = "p"
        Piece.piece_dict[colour].append(self)
        Piece.__init__(self, x, y, colour, Knight.letter)

    def __str__(self):
        return self.colour + " Knight"
    
    #return co-ordinates of all squares this peace is allowed to move to. 
    #Start Tier 1,3,4 legality checks (refer to "Legality Logic Explained")
    def get_possible_moves(self):
        possible_new_pos = [] 
        delta_x = 2
        delta_y = 1
        for i in range(8):
            if i == 4: #flip deltas to create other 4 moves
                delta_x = 1
                delta_y = 2
            move_vector = Pos(delta_x, delta_y)
            new_pos = self.pos + move_vector
            if new_pos.isValid() and not new_pos.isFriendly(self): 
                possible_new_pos.append(new_pos)
            #modify deltas for next loop
            if i % 2 == 0:
                delta_y *= -1
            else:
                delta_x *= -1           
        return possible_new_pos
        #proceed to Tier 5,6 legality checks later


class Bishop(Piece):

    letter = "B"
    value = 3

    def __init__(self, x, y, colour, is_promoted):
        self.is_promoted = is_promoted
        if is_promoted:
            Game.board[x][y] = "p"
        Piece.piece_dict[colour].append(self)
        Piece.__init__(self, x, y, colour, Bishop.letter)

    def __str__(self):
        return self.colour + " Bishop"

    def get_possible_moves(self):
        possible_new_pos = [] 
        delta_x = delta_y = 1
        for i in range(4):
            new_pos = self.pos 
            move_vector = Pos(delta_x, delta_y)
            for distance in range(8): #maximum diagonal distance a bishop can travel is 7 squares. 
                new_pos += move_vector
                if new_pos.isValid() and not new_pos.isFriendly(self):
                    possible_new_pos.append(new_pos)
                    if new_pos.isHostile(self): #can't travel through hostile pieces but can take their place (capture them)
                        break
                else:
                    break

            #modify deltas for next loop
            if i % 2 == 0:
                delta_y *= -1
            else:
                delta_x *= -1 
        return possible_new_pos 



class Pawn(Piece):

    letter = "P"
    value = 1

    def __init__(self, x, y, colour, has_moved):
        self.is_promoted = False #promoting to a pawn isn't allowed
        self.has_moved = has_moved #only relevant in rules for pawn, king and rooks.
        if has_moved:
            Game.board[x][y] = "m"
        Piece.piece_dict[colour].append(self)
        Piece.__init__(self, x, y, colour, Pawn.letter)

    def __str__(self):
        return self.colour + " Pawn"

    def get_possible_moves(self):
        possible_new_pos = [] 
        delta_x = 1 #only when capturing
        delta_y = 1
        if self.colour == "Black":
            delta_y = -1
            delta_x = -1
        normal_move = self.pos + Pos(0, delta_y)
        move_2_forward = self.pos + Pos(0, delta_y * 2) #only if the pawn hasn't yet moved
        capture_right = self.pos + Pos(delta_x, delta_y)
        capture_left = self.pos + Pos(delta_x * -1, delta_y)
        if not normal_move.isFriendly(self) and not normal_move.isHostile(self): #then it's clear
            possible_new_pos.append(normal_move)
            #if pawn hasn't moved yet and destination square isn't occupied
            if self.has_moved == False and not move_2_forward.isFriendly(self) and not move_2_forward.isHostile(self):
                possible_new_pos.append(move_2_forward)
        if capture_right.isHostile(self) or self.canEnPassant():
            possible_new_pos.append(capture_right)
        if capture_left.isHostile(self) or self.canEnPassant():
            possible_new_pos.append(capture_left)
        return possible_new_pos

    def canEnpassant(self): #google en passant. Holy hell
        pass #TODO write method from notes on pad


class Queen(Piece):

    letter = "Q"
    value = 9

    def __init__(self, x, y, colour, is_promoted):
        self.is_promoted = is_promoted
        if is_promoted:
            Game.board[x][y] = "p"
        Piece.piece_dict[colour].append(self)
        Piece.__init__(self, x, y, colour, Queen.letter)

    def __str__(self):
        return self.colour + " Queen"


class King(Piece):

    letter = "K"
    value = 100 #essentially infinite

    def __init__(self, x, y, colour, has_moved):
        self.is_promoted = False #promoting to a king isn't allowed
        self.has_moved = has_moved
        if has_moved:
            Game.board[x][y] = "m"
        Piece.piece_dict[colour].append(self)
        Piece.__init__(self, x, y, colour, King.letter)

    def __str__(self):
        return self.colour + " King"


class Rook(Piece):

    letter = "R"
    value = 5

    def __init__(self, x, y, colour, is_promoted, has_moved):
        self.is_promoted = is_promoted
        self.has_moved = has_moved
        if has_moved:
            Game.board[x][y] = "m"
        elif is_promoted:
            Game.board[x][y] = "p"
        Piece.piece_dict[colour].append(self)
        Piece.__init__(self, x, y, colour, Rook.letter)

    def __str__(self):
        return self.colour + " Rook"

class Game:

    turn = "White"
    move = 0

    #no matter what happens board dimensions will never change
    board = [
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""]
        ]
    
    pgn = [] #"Portable Game Notation" as used by World Chess governing body Fide

    def __init__(self, type, isNew):
        self.type = type
        self.isNew = isNew
        if isNew:
            if type == "Classic":
                Game.loadGame("new_game.txt")
            elif type == "C960":
                Game.load960Game() #TODO implement
            else:
                print("Error, wrong game type attempted to be initialized, " + type + " isn't supported!")
        else:
            Game.loadGame("custom_game.txt") #TODO implement

    def update_pgn(piece_obj, new_pos):
        piece_rep = piece_obj.letter
        capture = "x"
        new_sq = str(new_pos.toSqu()).casefold()
        if isinstance(piece_obj, Pawn):
            pass #TODO finish this (if pawn cap but destination empty) then finish pgn generation

    
    @staticmethod
    def populateVirtualBoard(file):
        x = 0
        wasted_line = file.readline() #get rid of empty line
        for x in range(8):
            line = file.readline().strip("\n").split(",")
            print(x)
            print(line)
            y = -1
            for data in line:
                y += 1
                colour_letter = data[0]
                piece_letter = data[1]
                other = len(data) == 3
                if colour_letter == "W":
                    colour = "White"
                else:
                    colour = "Black"
                if piece_letter == "N":
                    knight = Knight(x,y, colour, other)
                elif piece_letter == "B":
                    bishop = Bishop(x,y,colour, other)
                elif piece_letter == "P":
                    pawn = Pawn(x,y, colour, other)
                elif piece_letter == "Q":
                    queen = Queen(x,y, colour, other)
                elif piece_letter == "K":
                    king = King(x,y, colour, other)
                elif piece_letter == "R":
                    if other:
                        if data[2] == "m":
                            rook = Rook(x,y, colour, False, True)
                        elif data[2] == "p":
                            rook = Rook(x,y, colour, True, False)
                    else:
                        rook = Rook(x,y, colour, False, False)
                elif piece_letter == "0":
                    Game.writeSquare(Pos(x,y), "00")


    @staticmethod
    def loadGame(file_name):
        try:
            file_dir = Path("saved_games/")
            file_path = file_dir / file_name
            file = open(file_path,"r+")
            Game.populateVirtualBoard(file)
        except FileNotFoundError:
            print("Can't find file",str(file_name)+" is not in your directory!")

    @staticmethod
    def readSquare(pos): #read from board 2D array using a Pos object
        if isinstance(pos, Pos):
            return Game.board[pos.x][pos.y]
        return None

    @staticmethod
    def writeSquare(pos, value): #write to board 2D array using a Pos object
        if isinstance(pos, Pos):
            Game.board[pos.x][pos.y] = value


def main():
    game = Game("Classic", True)
    

main()



#CODE TESTS
#Yes this is scuffed but good enough to get the job done. 

knight = Knight(2,2,"White",False)
knight2 = Knight(2,3,"White",False)
bishop = Bishop(0,2, "Black",False)
pawn = Pawn(6,0,"Black",False)
queen = Queen(4,3,"White", True)
king = King(7,4,"Black", False)
rook = Rook(0,0,"White", False, False)
print(knight)
print(knight2)
test1 = knight == knight2
test2 = knight == rook
test3 = knight.pos.isValid()
print("False? " + str(test1))
print("False? " + str(test2))
print("Knight pos Valid (True) ? " + str(test3))
print("knight pos: "+ str(knight.pos))
print("knight pos: "+ str(knight.pos.toSqu().toPos()))
print("Knight square: " + str(knight.pos.toSqu()))
pos_arr = knight.get_possible_moves()
moves = ""
for pos in pos_arr:
    moves += " ," + (str(pos.toSqu())) 
print("Knight can go to " + moves)

knight.moveToAnarchy(Pos(0,0))
print("Knight square: " + str(knight.pos.toSqu()))
pos_arr = knight.get_possible_moves()
moves = ""
for pos in pos_arr:
    moves += " ," + (str(pos.toSqu())) 
print("Knight can go to " + moves)

moves = ""
pos_arr = bishop.get_possible_moves()
print("Bishop square: " + str(bishop.pos.toSqu()))
for pos in pos_arr:
    moves += " ," + (str(pos.toSqu())) 
print("Bishop can go to " + moves)

moves = ""
pos_arr = pawn.get_possible_moves()
print("Pawn square: " + str(pawn.pos.toSqu()))
for pos in pos_arr:
    moves += " ," + (str(pos.toSqu())) 
print("Pawn can go to " + moves)

#TODO Test new features