import pygame
import numpy as np

from pieces import Piece, Pawn, Knight, Rook, Bishop, Queen, King, Block

grid_size: int = 8
screen = pygame.display.set_mode((800, 800))


def get_piece(pieces: [], pos: (int, int)):
    for column in pieces:
        for piece in column:
            if piece.x <= pos[0] <= piece.x + 50 and piece.y <= pos[1] <= piece.y + 50:
                return piece
    return None


def get_block(grid: [], pos: (int, int)):
    for column in grid:
        for block in column:
            if block.x <= pos[0] <= block.x + 100 and block.y <= pos[1] <= block.y + 100:
                return block


def remove_piece(pieces: [], piece_to_die: Piece):
    for column in pieces:
        if piece_to_die in column:
            column.remove(piece_to_die)


def check_pawn_rules(piece: Piece, pieces: [], grid: [], block_to_be_populated: Block):
    if block_to_be_populated.y - piece.board_block.y > 100 \
            or block_to_be_populated.y - piece.board_block.y < -100:
        print("something's fishy here")
        return False
    else:
        if block_to_be_populated.has_chess_piece and \
                (block_to_be_populated.x - piece.board_block.x < 100 or
                 block_to_be_populated.x - piece.board_block.x > -100):
            print("going in for the kill it seems")
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if not dead_piece_walking:
                print("error, block should had a chess piece on it, but it doesnt")
                return False
            elif dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            elif block_to_be_populated.x == piece.board_block.x:
                print("you can't kill a piece in front of you")
                return False
            else:
                if piece.white and block_to_be_populated.y < piece.board_block.y:
                    print("pawn can't move backwards")
                    return False
                elif not piece.white and block_to_be_populated.y > piece.board_block.y:
                    print("pawn can't move backwards")
                    return False
                remove_piece(pieces, dead_piece_walking)
                print("piece killed : " + str(dead_piece_walking))
                return True
        elif block_to_be_populated.x != piece.board_block.x:
            print("way out of x bounds to move")
        else:
            if piece.white and block_to_be_populated.y < piece.board_block.y:
                print("pawn can't move backwards")
                return False
            elif not piece.white and block_to_be_populated.y > piece.board_block.y:
                print("pawn can't move backwards")
                return False
            return True


def move(piece: Piece, pieces: [], grid: [], new_pos: (int, int)):
    block_to_be_populated: Block
    block_to_be_populated = get_block(grid, new_pos)
    if not block_to_be_populated:
        print("error, new position out of bounds")
        return
    if type(piece) == Pawn:
        if check_pawn_rules(piece, pieces, grid, block_to_be_populated):
            piece.board_block.has_chess_piece = False
            block_to_be_populated.has_chess_piece = True
            piece.board_block = block_to_be_populated
            piece.x = piece.board_block.x + 25
            piece.y = piece.board_block.y + 25
        else:
            print("move failed, check error log")


def main():
    pygame.init()
    logo = pygame.image.load('image/chessLogo.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Chess')

    running = True

    screen.fill((255, 0, 0))

    grid = []
    color = True
    for i in range(0, grid_size):
        column = []
        for j in range(0, grid_size):
            if color:
                b = Block(i*100, j*100, False, [255, 255, 255])
                b.draw(screen)
                column.append(b)
                color = False
            else:
                b = Block(i*100, j*100, False, [0, 0, 0])
                b.draw(screen)
                column.append(b)
                color = True
            if j == 7:
                color = not color
        grid.append(column)
    pieces = []
    for i in range(0, grid_size):
        column = []
        for j in range(0, grid_size):
            if j == 1:
                piece = Pawn((i*100)+25, ((j*100)+25), True, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif j == 6:
                piece = Pawn((i*100) + 25, ((j*100)+25), False, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif (j == 0 and i == 0) or (j == 0 and i == 7):
                piece = Rook((i * 100) + 25, ((j * 100) + 25), True, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif (j == 7 and i == 0) or (j == 7 and i == 7):
                piece = Rook((i * 100) + 25, ((j * 100) + 25), False, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif (j == 0 and i == 1) or (j == 0 and i == 6):
                piece = Knight((i * 100) + 25, ((j * 100) + 25), True, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif (j == 7 and i == 1) or (j == 7 and i == 6):
                piece = Knight((i * 100) + 25, ((j * 100) + 25), False, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif (j == 0 and i == 2) or (j == 0 and i == 5):
                piece = Bishop((i * 100) + 25, ((j * 100) + 25), True, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif (j == 7 and i == 2) or (j == 7 and i == 5):
                piece = Bishop((i * 100) + 25, ((j * 100) + 25), False, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif j == 0 and i == 4:
                piece = Queen((i * 100) + 25, ((j * 100) + 25), True, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif j == 7 and i == 4:
                piece = Queen((i * 100) + 25, ((j * 100) + 25), False, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif j == 0 and i == 3:
                piece = King((i * 100) + 25, ((j * 100) + 25), True, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
            elif j == 7 and i == 3:
                piece = King((i * 100) + 25, ((j * 100) + 25), False, grid[i][j])
                piece.draw(screen)
                column.append(piece)
                piece.board_block.has_chess_piece = True
        pieces.append(column)

    print(pieces)

    piece_selected = None
    while running:
        for column in grid:
            for block in column:
                block.draw(screen)
        for column in pieces:
            for piece in column:
                piece.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                piece = get_piece(pieces, pygame.mouse.get_pos())
                print("mouse position: " + str(pygame.mouse.get_pos()))
                if piece and not piece_selected:
                    print("Piece selected: " + str(piece))
                    piece_selected = piece
                    piece.board_block.is_selected = True
                elif piece_selected:
                    move(piece_selected, pieces, grid, pygame.mouse.get_pos())
                    piece_selected.board_block.is_selected = False
                    piece_selected = None
                else:
                    print("no piece in this position")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(pieces)
        pygame.display.update()


if __name__ == '__main__':
    main()


