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

    def toSqu(self):
        return board_files[self.x, self.y + 1]

    def __str__(self):
        return str(self.x)+","+str(self.y)


#squ always refers to a square as people see it e.g. E4
#The letter represents the file/collumn/x_pos while the number represents the rank/row/y_pos. This is common chess terminology.
class Squ:

    def __init__(self, file, rank):
        self.file = file
        self.rank = rank
    
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

    def __init__(self, x, y, colour, is_promoted, has_moved):
        self.pos = Pos(x, y)
        self.colour = colour
        self.is_promoted = is_promoted #Needed for material balance calculation/ display
        self.has_moved = has_moved
        total_pieces += 1

    def move_pos(self, new_pos):
        self.pos = new_pos
        self.has_moved = True


class Knight(Piece):

    moveset = ["KNIGHT_MOVES"]
    letter = "N"
    value = 3

    def __init__(self):
        pass

    def __str__(self):
        return self.colour, "Knight"
    
    #return co-ordinates of all squares this peace is allowed to move to. 
    #Start Tier 1 legality check (refer to "Legality Logic Explained")
    def get_piece_moves(self):
        possible_new_pos = [] 
        #TODO carry on making these



class Bishop(Piece):

    moveset = ["BISHOP_MOVES"]
    letter = "B"
    value = 3

    def __init__(self):
        pass

    def __str__(self):
        return self.colour, "Bishop"


class Pawn(Piece):

    moveset = ["PAWN_MOVES"]
    letter = "P"
    value = 1

    def __init__(self):
        pass

    def __str__(self):
        return self.colour, "Pawn"


class Queen(Piece):

    moveset = ["QUEEN_MOVES"]
    letter = "Q"
    value = 9

    def __init__(self):
        pass

    def __str__(self):
        return self.colour, "Queen"


class King(Piece):

    moveset = ["KING_MOVES"]
    letter = "K"
    value = 100 #essentially infinite

    def __init__(self):
        pass

    def __str__(self):
        return self.colour, "King"


class Rook(Piece):

    moveset = ["ROOK_MOVES"]
    letter = "R"
    value = 5

    def __init__(self):
        pass

    def __str__(self):
        return self.colour, "Rook"