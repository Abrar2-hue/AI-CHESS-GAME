import pygame
import chess
import chess.svg
import chess.engine
import sys

WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE, GREEN = (255, 255, 255), (118, 150, 86) #RGB COLOR CODES

pygame.init()

pieces = {}
def load_images():
    names = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk',
             'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    for name in names:
        pieces[name] = pygame.transform.scale(
            pygame.image.load(f'images/{name}.png'), (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(win, board):
    colors = [WHITE, GREEN]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(win, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            color = 'w' if piece.color == chess.WHITE else 'b'
            kind = piece.symbol().lower()
            win.blit(pieces[color + kind], (col * SQUARE_SIZE, row * SQUARE_SIZE))

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def evaluate(board):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            score += value if piece.color == chess.WHITE else -value
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate(board), None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# Get board square from mouse
def get_square(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess AI with Alpha-Beta")
    clock = pygame.time.Clock()

    board = chess.Board()
    load_images()

    selected_square = None
    move_from = None

    running = True
    while running:
        draw_board(screen, board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif board.turn == chess.WHITE and event.type == pygame.MOUSEBUTTONDOWN:
                square = get_square(pygame.mouse.get_pos())
                if move_from is None:
                    if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                        move_from = square
                else:
                    move_to = square
                    move = chess.Move(move_from, move_to)
                    if move in board.legal_moves:
                        board.push(move)
                    move_from = None

        if board.turn == chess.BLACK and not board.is_game_over():
            _, ai_move = minimax(board, 3, float('-inf'), float('inf'), False)
            if ai_move:
                board.push(ai_move)

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
