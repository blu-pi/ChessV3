import pygame

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

    def __init__(self, x, y, colour, letter):
        self.pos = Pos(x, y)
        self.colour = colour
        self.letter = letter
        Piece.total_pieces += 1

    def __eq__(self, other):
        if (isinstance(other, Pos)):
            return self.letter == other.letter and self.colour == other.colour
        return False

    def __str__(self):
        return self.colour + self.getLetter

    def move_pos(self, new_pos):
        self.pos = new_pos
        self.has_moved = True


class Knight(Piece):

    letter = "N"
    value = 3

    def __init__(self, x, y, colour, is_promoted):
        self.is_promoted = is_promoted
        Piece.__init__(self, x, y, colour, Knight.letter)

    def __str__(self):
        return self.colour + " Knight"
    
    #return co-ordinates of all squares this peace is allowed to move to. 
    #Start Tier 1 legality check (refer to "Legality Logic Explained")
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
            if new_pos.isValid:
                possible_new_pos.append(new_pos)
            #modify deltas for next loop
            if i % 2 == 0:
                delta_y *= -1
            else:
                delta_x *= -1           
        print(possible_new_pos + " DEBUG TEST")
        #proceed to Tier 3 legality checks    
    
    def getLetter(self):
        return self.letter


class Bishop(Piece):

    letter = "B"
    value = 3

    def __init__(self, x, y, colour, is_promoted):
        self.is_promoted = is_promoted
        Piece.__init__(self, x, y, colour, Bishop.letter)

    def __str__(self):
        return self.colour + " Bishop"


class Pawn(Piece):

    letter = "P"
    value = 1

    def __init__(self, x, y, colour, has_moved):
        self.is_promoted = False #promoting to a pawn isn't allowed
        self.has_moved = has_moved #only relevant in rules for pawn, king and rooks.
        Piece.__init__(self, x, y, colour, Pawn.letter)

    def __str__(self):
        return self.colour + " Pawn"


class Queen(Piece):

    letter = "Q"
    value = 9

    def __init__(self, x, y, colour, is_promoted):
        self.is_promoted = is_promoted
        Piece.__init__(self, x, y, colour, Queen.letter)

    def __str__(self):
        return self.colour + " Queen"


class King(Piece):

    letter = "K"
    value = 100 #essentially infinite

    def __init__(self, x, y, colour, has_moved):
        self.is_promoted = False #promoting to a king isn't allowed
        self.has_moved = has_moved
        Piece.__init__(self, x, y, colour, King.letter)

    def __str__(self):
        return self.colour + " King"


class Rook(Piece):

    letter = "R"
    value = 5

    def __init__(self, x, y, colour, is_promoted, has_moved):
        self.is_promoted = is_promoted
        self.has_moved = has_moved
        Piece.__init__(self, x, y, colour, Rook.letter)

    def __str__(self):
        return self.colour + " Rook"

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
print("Knight square: " + str(knight.pos.toSqu()))