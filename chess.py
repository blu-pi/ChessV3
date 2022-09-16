import pygame

#Legality Logic Explained:
#Tiers are for understanding what code does which action. Checks may move between tiers and are NOT perfectly sequential in execution!
#Tier 1: How a peace moves according to the rules of chess e.g. Knight moves like an "L" 
#Tier 2: Exceptional moves (Pawn capture, En passant, Castling) 
#Tier 3: Is the move "blocked" by another piece? Pieces may not travel through other pieces. (This tier doesn't apply to the knight) Special mention for castling where the method is written
#Tier 4: Does this move cause the current player to check themselves? A player isn't allowed to check themselves.
#Tier 5: If the player is in Check, is the move still legal?
    #e.g The player must "stop" the check. When this isn't possible the game is already over anyway as this is checked at the end of the previous player's turn
#Any move created from Tier 1 and 2 that passes all checks can be considered to be a "Candidate Move" and is allowed to be played


#interface (the oop kind)
class Piece:
    total_pieces = 0

    def __init__(self, pos, colour, is_promoted):
        self.pos = pos
        self.colour = colour
        self.is_promoted = is_promoted #Needed for material balance calculation/ display
        self.has_moved = False
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
    #Only checks Tier 1 legality (refer to "Legality Logic Explained")
    def get_piece_moves(self):
        possible_new_pos = [] 


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