import pygame
import sys
import time
from alpha_beta_pruning import *
from boardFunctions import *

pygame.init()

decision_times = []
ai_wins = 0   


WIDTH, HEIGHT = 800, 800
BOARD_COLOR = (222, 184, 135)
LINE_COLOR = (0, 0, 0)
WHITE_PIECE_COLOR = (255, 255, 255)
BLACK_PIECE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 215, 0)
EMPTY_SPOT_COLOR = (200, 200, 200)
FONT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (240, 240, 240)


FPS = 60
PIECE_RADIUS = 15
ANIMATION_SPEED = 0.05  


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nine Men's Morris")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)


board_positions = [
    (100, 100), (400, 100), (700, 100),  # 0, 1, 2
    (100, 400), (700, 400),              # 3, 4
    (100, 700), (400, 700), (700, 700),  # 5, 6, 7
    (175, 175), (400, 175), (625, 175),  # 8, 9, 10
    (175, 400), (625, 400),              # 11, 12
    (175, 625), (400, 625), (625, 625), # 13, 14, 15
    (250, 250), (400, 250), (550, 250),  # 16, 17, 18
    (250, 400), (550, 400),              # 19, 20
    (250, 550), (400, 550), (550, 550),   # 21, 22, 23
]

def heuristicFunction(board, isStage1):
    utility = 0

    player1Pieces = countPieces(board, "1")
    player2Pieces = countPieces(board, "2")

    numPossibleMillsPlayer1 = getPossibleMillCount(board, "1")  # Own potential mills
    potentialMillsPlayer2 = opponentThreatMillSites(board, "2") #how close the opponent is to forming a mill using the player’s current board state
    difference = player1Pieces - player2Pieces

    if player1Pieces <= 2:
        return float('-inf')
    if player2Pieces <= 2:
        return float('inf')

    if isStage1:
        # Placing Phase
        utility += 18 * numPossibleMillsPlayer1
        utility -= 10 * potentialMillsPlayer2
        utility += 9 * difference
    else:
        player1Moves = NextMoves(board)
        player2Moves = opponentMoves(NextMoves(flipBoard(board)))

        if player2Pieces < 3 or len(player2Moves) == 0:
            return float('inf')
        elif player1Pieces < 3 or len(player1Moves) == 0:
            return float('-inf')
        
        legal_moves = len(NextMoves(board))
        utility += 26 * numPossibleMillsPlayer1
        utility -= 8 * potentialMillsPlayer2
        utility += 11 * difference
        utility -= 5 * legal_moves

    return utility


class GameState:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.board = ["X"] * 24
        self.phase = 1 
        self.selected_pos = None
        self.human_turn = True
        self.message = "Place your piece (White)"
        self.animation = None
        self.removing_piece = False
        self.human_pieces_to_place = 9
        self.ai_pieces_to_place = 9
        self.human_pieces_on_board = 0
        self.ai_pieces_on_board = 0
        self.pending_ai_move = None
        self.game_over = False
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.depth = 3
        self.ai_depth = 3
        self.pending_removal = False
        self.pending_removal_pos = None


game_state = GameState()

def draw_board():
    screen.fill(BOARD_COLOR)
    
    # Draw board lines
    pygame.draw.line(screen, LINE_COLOR, board_positions[0], board_positions[2], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[2], board_positions[7], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[7], board_positions[5], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[5], board_positions[0], 3)
    
    pygame.draw.line(screen, LINE_COLOR, board_positions[8], board_positions[10], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[10], board_positions[15], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[15], board_positions[13], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[13], board_positions[8], 3)
    
    pygame.draw.line(screen, LINE_COLOR, board_positions[16], board_positions[18], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[18], board_positions[23], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[23], board_positions[21], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[21], board_positions[16], 3)
    
    pygame.draw.line(screen, LINE_COLOR, board_positions[1], board_positions[9], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[9], board_positions[17], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[6], board_positions[14], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[14], board_positions[22], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[3], board_positions[11], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[11], board_positions[19], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[4], board_positions[12], 3)
    pygame.draw.line(screen, LINE_COLOR, board_positions[12], board_positions[20], 3)
    

    for i, pos in enumerate(board_positions):
        if game_state.board[i] == "X":
            pygame.draw.circle(screen, EMPTY_SPOT_COLOR, pos, PIECE_RADIUS)
            pygame.draw.circle(screen, LINE_COLOR, pos, PIECE_RADIUS, 1)
    
  
    for i, pos in enumerate(board_positions):
        if game_state.board[i] == "1" and (not game_state.animation or i != game_state.animation[0]):  #human (white)
            pygame.draw.circle(screen, WHITE_PIECE_COLOR, pos, PIECE_RADIUS)
            pygame.draw.circle(screen, LINE_COLOR, pos, PIECE_RADIUS, 1)
        elif game_state.board[i] == "2" and (not game_state.animation or i != game_state.animation[0]):  #AI (black)
            pygame.draw.circle(screen, BLACK_PIECE_COLOR, pos, PIECE_RADIUS)
            pygame.draw.circle(screen, LINE_COLOR, pos, PIECE_RADIUS, 1)
    
    if game_state.selected_pos is not None:
        pygame.draw.circle(screen, HIGHLIGHT_COLOR, board_positions[game_state.selected_pos], PIECE_RADIUS + 5, 3)
    
    if game_state.animation:
        from_pos, to_pos, progress = game_state.animation
        start_pos = board_positions[from_pos]
        end_pos = board_positions[to_pos]
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
        piece = game_state.board[from_pos]
        color = WHITE_PIECE_COLOR if piece == "1" else BLACK_PIECE_COLOR
        pygame.draw.circle(screen, color, (int(x), int(y)), PIECE_RADIUS)
        pygame.draw.circle(screen, LINE_COLOR, (int(x), int(y)), PIECE_RADIUS, 1)
    
    text = font.render(game_state.message, True, FONT_COLOR)
    screen.blit(text, (20, 20))
    
    human_text = font.render(f"Human: {game_state.human_pieces_to_place} to place, {game_state.human_pieces_on_board} on board", True, FONT_COLOR)
    ai_text = font.render(f"AI: {game_state.ai_pieces_to_place} to place, {game_state.ai_pieces_on_board} on board", True, FONT_COLOR)
    screen.blit(human_text, (20, 50))
    screen.blit(ai_text, (20, 80))

def get_position_index(pos):
    for i, board_pos in enumerate(board_positions):
        if ((pos[0] - board_pos[0]) ** 2 + (pos[1] - board_pos[1]) ** 2) <= PIECE_RADIUS ** 2:
            return i
    return None

def handle_phase1_click(pos_index):
    if game_state.board[pos_index] == "X":
        game_state.board[pos_index] = "1"
        game_state.human_pieces_to_place -= 1
        game_state.human_pieces_on_board += 1
        
        if isCloseMill(pos_index, game_state.board):
            game_state.message = "Click an AI piece to remove"
            game_state.removing_piece = True
            return True
        else:
            game_state.human_turn = False
            game_state.message = "AI is thinking..."
            return True
    return False

def handle_phase2_click(pos_index):
    if game_state.selected_pos is None:
        if game_state.board[pos_index] == "1":
            game_state.selected_pos = pos_index
            game_state.message = "Select destination"
            return False
    else:
        if game_state.board[pos_index] == "X":
            human_pieces = countPieces(game_state.board, "1")
            if human_pieces <= 3:  # flying allowed
                valid_move = True
            else:
                valid_move = pos_index in adjacentPositions(game_state.selected_pos)
            
            if valid_move:
                game_state.animation = (game_state.selected_pos, pos_index, 0.0)
                game_state.message = "Animating move..."
                return True

        game_state.selected_pos = None
        game_state.message = "Select a piece to move"
    return False


def update_animation():
    if game_state.animation:
        from_pos, to_pos, progress = game_state.animation
        progress += ANIMATION_SPEED

        if progress >= 1.0:
            game_state.animation = None

            if game_state.board[from_pos] == "1":
                game_state.board[from_pos] = "X"
                game_state.board[to_pos] = "1"
                game_state.selected_pos = None

                if isCloseMill(to_pos, game_state.board):
                    game_state.message = "Click an AI piece to remove"
                    game_state.removing_piece = True
                else:
                    game_state.human_turn = False
                    game_state.message = "AI is thinking..."
        else:
            game_state.animation = (from_pos, to_pos, progress)


def ai_turn():
    if game_state.animation or game_state.game_over:
        return
    
    try:
        original_board = game_state.board.copy()
        original_human_count = sum(1 for p in original_board if p == "1")
        original_ai_count = sum(1 for p in original_board if p == "2")

        if game_state.phase == 1:
            start_time = time.time()
            evalBoard = minimax(original_board.copy(), game_state.depth, False, 
                                      game_state.alpha, game_state.beta, True, heuristicFunction)
            decision_times.append(time.time() - start_time)

            game_state.board = evalBoard.board
            
            new_human_count = sum(1 for p in game_state.board if p == "1")
            new_ai_count = sum(1 for p in game_state.board if p == "2")
            
            if new_human_count < original_human_count:
                game_state.human_pieces_on_board = new_human_count
            if new_ai_count > original_ai_count:
                game_state.ai_pieces_on_board = new_ai_count
                game_state.ai_pieces_to_place -= 1
            
            if game_state.human_pieces_to_place == 0 and game_state.ai_pieces_to_place == 0:
                game_state.phase = 2
                game_state.message = "Move your piece (White)"
            
            game_state.human_turn = True
        
        else:  # Phase 2 or 3

            start_time = time.time()
            eval_board = minimax(original_board.copy(), game_state.ai_depth, False,
                                      game_state.alpha, game_state.beta, False, heuristicFunction)
            
            decision_times.append(time.time() - start_time)

            game_state.board = eval_board.board
            
            new_human_count = sum(1 for p in game_state.board if p == "1")
            new_ai_count = sum(1 for p in game_state.board if p == "2")
            
            if new_human_count < original_human_count:
                game_state.human_pieces_on_board = new_human_count
            if new_ai_count != original_ai_count:
                game_state.ai_pieces_on_board = new_ai_count
            
            game_state.human_turn = True
            game_state.message = "Your turn"
    
    except Exception as e:
        print(f"AI Error: {str(e)}")
        game_state.human_turn = True
        game_state.message = "AI Error - Your turn again"

def check_game_over():
    if game_state.phase == 2 or game_state.phase == 3:
        if game_state.human_pieces_on_board < 3 or has_no_legal_moves(game_state.board, "1"):
            game_state.message = "Game Over - You Lost!"
            game_state.game_over = True
            return 'AI'
        if game_state.ai_pieces_on_board < 3 or has_no_legal_moves(game_state.board, "2"):
            game_state.message = "Game Over - You Won!"
            game_state.game_over = True
            return 'Human'
    return None
 
def HUMAN_VS_AI_GUI():
    global ai_wins, decision_times
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and game_state.human_turn and not game_state.animation and not game_state.game_over:
                pos = pygame.mouse.get_pos()
                pos_index = get_position_index(pos)
                
                if pos_index is not None:
                    if game_state.removing_piece:
                        if game_state.board[pos_index] == "2":
                            if not isCloseMill(pos_index, game_state.board) or allPiecesInMill(game_state.board, "2"):
                                game_state.board[pos_index] = "X"
                                game_state.ai_pieces_on_board -= 1
                                game_state.removing_piece = False
                                game_state.human_turn = False
                                game_state.message = "AI is thinking..."
                    else:
                        if game_state.phase == 1:
                            if handle_phase1_click(pos_index):
                                if game_state.human_pieces_to_place == 0 and game_state.ai_pieces_to_place == 0:
                                    game_state.phase = 2
                                    game_state.message = "Move your piece (White)"
                        else:
                            if handle_phase2_click(pos_index):
                                pass 
        
        if game_state.pending_removal and not game_state.animation:
            game_state.board[game_state.pending_removal_pos] = "X"
            game_state.human_pieces_on_board -= 1
            game_state.pending_removal = False
            game_state.pending_removal_pos = None
        
        update_animation()
        
        # AI turn
        if not game_state.human_turn and not game_state.animation and not game_state.removing_piece and not game_state.game_over:
            ai_turn()
            if check_game_over() == None:
                if game_state.phase == 1:
                    game_state.message = "Place your piece (White)"
                else:
                    game_state.message = "Move your piece (White)"
            elif check_game_over() == 'AI':
                print(f"Game Winner: AI")
                ai_wins+=1
            else:
                print(f"Game Winner: Human")
            
        
        draw_board()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    print("Welcome to Nine Mens Morris")
    print("==========================")
    print("Human vs AI")

    total_games = 1

    for game_num in range(total_games):
        game_state.reset()      
        pygame.init()              
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        HUMAN_VS_AI_GUI()

    pygame.quit()

    win_rate = (ai_wins / total_games) * 100
    avg_decision_time = sum(decision_times) / len(decision_times) if decision_times else 0

    print(f"\nAI Performance Report")
    print("=======================")
    print(f"AI Win Rate: {win_rate:.2f}%")
    print(f"Average Decision Time: {avg_decision_time:.2f} seconds")

