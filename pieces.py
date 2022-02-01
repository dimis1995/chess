import pygame


class Block:
    x: int
    y: int
    has_chess_piece: bool
    color: [int, int, int]
    is_selected: bool = False

    def __init__(self, x, y, piece, color: [int, int, int]):
        self.x = x
        self.y = y
        self.has_chess_piece = piece
        self.color = color

    def __str__(self):
        return "Block: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "Block: " + str(self.x) + "," + str(self.y)

    def draw(self, surface):
        if self.has_chess_piece and self.is_selected:
            pygame.draw.rect(surface, [0, 255, 0], pygame.Rect(self.x, self.y, 100, 100))
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, 100, 100))


class Piece:

    x: int
    y: int
    white: bool
    board_block: Block

    def __init__(self, x: int, y: int, white: bool, block: Block):
        self.x = x
        self.y = y
        self.white = white
        self.board_block = block

    def __str__(self):
        return "Piece: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "Piece: " + str(self.x) + "," + str(self.y)

    def draw(self, surface):
        image: pygame.image
        if self.white:
            image = pygame.image.load('image/white pawn.png')
        else:
            image = pygame.image.load('image/black pawn.png')
        image = pygame.transform.scale(image, (50, 50))
        surface.blit(image, (self.x, self.y))


class Pawn(Piece):

    def draw(self, surface):
        super().draw(surface)

    def __str__(self):
        return "Pawn: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "Pawn: " + str(self.x) + "," + str(self.y)


class Rook(Piece):

    def draw(self, surface):
        image: pygame.image
        if self.white:
            image = pygame.image.load('image/white rook.png')
        else:
            image = pygame.image.load('image/black rook.png')
        image = pygame.transform.scale(image, (50, 50))
        surface.blit(image, (self.x, self.y))

    def __str__(self):
        return "Rook: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "Rook: " + str(self.x) + "," + str(self.y)


class Knight(Piece):
    def __str__(self):
        return "Knight: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "Knight: " + str(self.x) + "," + str(self.y)

    def draw(self, surface):
        image: pygame.image
        if self.white:
            image = pygame.image.load('image/white knight.png')
        else:
            image = pygame.image.load('image/black knight.png')
        image = pygame.transform.scale(image, (50, 50))
        surface.blit(image, (self.x, self.y))


class Bishop(Piece):
    def __str__(self):
        return "Bishop: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "Bishop: " + str(self.x) + "," + str(self.y)

    def draw(self, surface):
        image: pygame.image
        if self.white:
            image = pygame.image.load('image/white bishop.png')
        else:
            image = pygame.image.load('image/black bishop.png')
        image = pygame.transform.scale(image, (50, 50))
        surface.blit(image, (self.x, self.y))


class Queen(Piece):
    def __str__(self):
        return "Queen: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "Queen: " + str(self.x) + "," + str(self.y)

    def draw(self, surface):
        image: pygame.image
        if self.white:
            image = pygame.image.load('image/white queen.png')
        else:
            image = pygame.image.load('image/black queen.png')
        image = pygame.transform.scale(image, (50, 50))
        surface.blit(image, (self.x, self.y))


class King(Piece):
    def __str__(self):
        return "King: " + str(self.x) + "," + str(self.y)

    def __repr__(self):
        return "King: " + str(self.x) + "," + str(self.y)

    def draw(self, surface):
        image: pygame.image
        if self.white:
            image = pygame.image.load('image/white king.png')
        else:
            image = pygame.image.load('image/black king.png')
        image = pygame.transform.scale(image, (50, 50))
        surface.blit(image, (self.x, self.y))