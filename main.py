import pygame

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
        print("pawn can't move across multiple spaces")
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
            elif block_to_be_populated.x - piece.board_block.x > 150 or \
                    block_to_be_populated.x - piece.board_block.x < -150:
                print("x axis too far movement")
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


def check_knight_rules(piece: Piece, pieces: [], grid: [], block_to_be_populated: Block):
    available_move_set = []
    x = piece.board_block.x
    y = piece.board_block.y
    available_move_set.append((x+100, y-200))
    available_move_set.append((x+200, y-100))
    available_move_set.append((x+200, y+100))
    available_move_set.append((x+100, y+200))
    available_move_set.append((x-100, y+200))
    available_move_set.append((x-200, y+100))
    available_move_set.append((x-200, y-100))
    available_move_set.append((x-100, y-200))

    if (block_to_be_populated.x, block_to_be_populated.y) in available_move_set:
        if block_to_be_populated.has_chess_piece:
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if not dead_piece_walking:
                print("something unexpected happened")
                return False
            if dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            else:
                remove_piece(pieces, dead_piece_walking)
                print("piece killed: " + str(dead_piece_walking))
                return True
        else:
            return True
    else:
        print("knight can't make that move")
        return False


def get_all_blocks_between(block1: Block, block2: Block, grid: []):
    blocks_between = []
    if block1.x == block2.x and block1.y != block2.y:
        # vertical movement
        for column in grid:
            for block in column:
                if block.x == block1.x and (block1.y < block.y < block2.y or block2.y < block.y < block1.y):
                    blocks_between.append(block)
    elif block1.x != block2.x and block1.y == block2.y:
        # horizontal movement
        for column in grid:
            for block in column:
                if block.y == block1.y and (block1.x < block.x < block2.x or block2.x < block.x < block1.x):
                    blocks_between.append(block)
    elif block1.x != block2.x and block1.y != block2.y:
        # diagonal movement
        if abs(block1.x - block2.x) != abs(block1.y - block2.y):
            print("SOMETHING HAPPENED, SOMEONE ALERT THE QUEEN")
            exit(1)
        x_polarity = block2.x - block1.x
        y_polarity = block2.y - block1.y
        for column in grid:
            for block in column:
                block_x_polarity = block.x - block1.x
                block_y_polarity = block.y - block1.y
                if abs(block_x_polarity) == abs(block_y_polarity):
                    if (x_polarity * block_x_polarity > 0) and (y_polarity * block_y_polarity > 0):
                        if abs(block_x_polarity) < abs(x_polarity) and abs(block_y_polarity) < abs(y_polarity):
                            blocks_between.append(block)
    return blocks_between


def check_rook_rules(piece, pieces, grid, block_to_be_populated):
    if (piece.board_block.x == block_to_be_populated.x and piece.board_block.y != block_to_be_populated.y)\
            or (piece.board_block.y == block_to_be_populated.y and piece.board_block.x != block_to_be_populated.x):
        blocks_in_between = get_all_blocks_between(piece.board_block, block_to_be_populated, grid)
        for block in blocks_in_between:
            if block.has_chess_piece:
                print("colliding with block: " + str(block))
                return False
        if block_to_be_populated.has_chess_piece:
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            else:
                remove_piece(pieces, dead_piece_walking)
                print("piece killed: " + str(dead_piece_walking))
                return True
        else:
            return True
    else:
        print("rooks can't move diagonally")
        return False


def check_bishop_rules(piece, pieces, grid, block_to_be_populated):
    if (piece.board_block.x == block_to_be_populated.x) or (piece.board_block.y == block_to_be_populated.y):
        print("rook can't move horizontally or vertically")
        return False
    if abs(piece.board_block.x - block_to_be_populated.x) == abs(piece.board_block.y - block_to_be_populated.y):
        blocks_in_between = get_all_blocks_between(piece.board_block, block_to_be_populated, grid)
        for block in blocks_in_between:
            if block.has_chess_piece:
                print("colliding with block: " + str(block))
                return False
        if block_to_be_populated.has_chess_piece:
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            else:
                remove_piece(pieces, dead_piece_walking)
                print("piece killed: " + str(dead_piece_walking))
                return True
        else:
            return True


def check_queen_rules(piece, pieces, grid, block_to_be_populated):
    if (piece.board_block.x == block_to_be_populated.x) or (piece.board_block.y == block_to_be_populated.y):
        blocks_in_between = get_all_blocks_between(piece.board_block, block_to_be_populated, grid)
        for block in blocks_in_between:
            if block.has_chess_piece:
                print("colliding with block: " + str(block))
                return False
        if block_to_be_populated.has_chess_piece:
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            else:
                remove_piece(pieces, dead_piece_walking)
                print("piece killed: " + str(dead_piece_walking))
                return True
        else:
            return True
    if abs(piece.board_block.x - block_to_be_populated.x) == abs(piece.board_block.y - block_to_be_populated.y):
        blocks_in_between = get_all_blocks_between(piece.board_block, block_to_be_populated, grid)
        for block in blocks_in_between:
            if block.has_chess_piece:
                print("colliding with block: " + str(block))
                return False
        if block_to_be_populated.has_chess_piece:
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            else:
                remove_piece(pieces, dead_piece_walking)
                print("piece killed: " + str(dead_piece_walking))
                return True
        else:
            return True


def check_king_rules(piece, pieces, grid, block_to_be_populated):
    if abs(piece.board_block.x - block_to_be_populated.x) > 150 or \
            abs(piece.board_block.y - block_to_be_populated.y) > 150:
        print("king can't move more than one block space")
        return False
    if (piece.board_block.x == block_to_be_populated.x) or (piece.board_block.y == block_to_be_populated.y):
        if block_to_be_populated.has_chess_piece:
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            else:
                remove_piece(pieces, dead_piece_walking)
                print("piece killed: " + str(dead_piece_walking))
                return True
        else:
            return True
    if abs(piece.board_block.x - block_to_be_populated.x) == abs(piece.board_block.y - block_to_be_populated.y):
        if block_to_be_populated.has_chess_piece:
            dead_piece_walking = get_piece(pieces, (block_to_be_populated.x + 30, block_to_be_populated.y + 30))
            if dead_piece_walking.white == piece.white:
                print("pieces of same color can't kill each other")
                return False
            else:
                remove_piece(pieces, dead_piece_walking)
                print("piece killed: " + str(dead_piece_walking))
                return True
        else:
            return True


def move(piece: Piece, pieces: [], grid: [], new_pos: (int, int)):
    block_to_be_populated: Block
    block_to_be_populated = get_block(grid, new_pos)
    check: bool = False
    if not block_to_be_populated:
        print("error, new position out of bounds")
        return
    if type(piece) == Pawn and check_pawn_rules(piece, pieces, grid, block_to_be_populated):
        check = True
    elif type(piece) == Knight and check_knight_rules(piece, pieces, grid, block_to_be_populated):
        check = True
    elif type(piece) == Rook and check_rook_rules(piece, pieces, grid, block_to_be_populated):
        check = True
    elif type(piece) == Bishop and check_bishop_rules(piece, pieces, grid, block_to_be_populated):
        check = True
    elif type(piece) == Queen and check_queen_rules(piece, pieces, grid, block_to_be_populated):
        check = True
    elif type(piece) == King and check_king_rules(piece, pieces, grid, block_to_be_populated):
        check = True
    else:
        print("error, see error log")
        return
    if check:
        piece.board_block.has_chess_piece = False
        block_to_be_populated.has_chess_piece = True
        piece.board_block = block_to_be_populated
        piece.x = piece.board_block.x + 25
        piece.y = piece.board_block.y + 25


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
