import pygame
from pygame.locals import *
from constants import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        
        self.TITLE_FONT = pygame.font.SysFont(TITLE_FONT_NAME, TITLE_FONT_SIZE, bold=True)
        self.MENU_FONT = pygame.font.SysFont(MENU_FONT_NAME, MENU_FONT_SIZE)
        self.STATUS_FONT = pygame.font.SysFont(STATUS_FONT_NAME, STATUS_FONT_SIZE)
        self.PIECE_FONT = pygame.font.SysFont(PIECE_FONT_NAME, PIECE_FONT_SIZE)
        self.THEME_FONT = pygame.font.SysFont(THEME_FONT_NAME, THEME_FONT_SIZE)
        
        self.button_rects = {}
    
    def draw_main_menu(self):
        """Draw the main menu screen"""
        self.screen.fill(BACKGROUND_COLOR)
        
        title = self.TITLE_FONT.render("ChessChamp", True, GOLD_COLOR)
        title_rect = title.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        options = ["New Game", "Quit"]
        
        for i, option in enumerate(options):
            rect = pygame.Rect(WIDTH//2 - 100, 250 + i*80, 200, 50)
            color = BUTTON_COLOR if rect.collidepoint(mouse_pos) else (50, 50, 80)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 255), rect, 2, border_radius=10)
            
            text = self.MENU_FONT.render(option, True, TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    def draw_theme_menu(self, current_theme):
        """Draw the theme selection menu with 2 columns"""
        self.screen.fill(MENU_BACKGROUND)
        
        title = self.MENU_FONT.render("Board Theme", True, TEXT_COLOR)
        self.screen.blit(title, (20, 20))
        
        mouse_pos = pygame.mouse.get_pos()
        theme_names = list(THEMES.keys())
        
        for i, theme in enumerate(theme_names[:8]):
            x = 20
            y = 70 + i * 40
            
            checkbox = pygame.Rect(x, y + 5, 20, 20)
            pygame.draw.rect(self.screen, (200, 200, 200), checkbox, 2)
            
            if theme == current_theme:
                pygame.draw.rect(self.screen, (100, 255, 100), checkbox.inflate(-4, -4))
            
            text = self.THEME_FONT.render(theme, True, TEXT_COLOR)
            self.screen.blit(text, (x + 30, y))
            
            option_rect = pygame.Rect(x, y, WIDTH//2 - 30, 30)
            if option_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BUTTON_COLOR, option_rect, border_radius=5)
        for i, theme in enumerate(theme_names[8:]):
            x = WIDTH // 2 + 10
            y = 70 + i * 40
            
            checkbox = pygame.Rect(x, y + 5, 20, 20)
            pygame.draw.rect(self.screen, (200, 200, 200), checkbox, 2)
            
            if theme == current_theme:
                pygame.draw.rect(self.screen, (100, 255, 100), checkbox.inflate(-4, -4))
            
            text = self.THEME_FONT.render(theme, True, TEXT_COLOR)
            self.screen.blit(text, (x + 30, y))
        
            option_rect = pygame.Rect(x, y, WIDTH//2 - 30, 30)
            if option_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BUTTON_COLOR, option_rect, border_radius=5)
        
        back_rect = pygame.Rect(20, HEIGHT - 60, 100, 40)
        pygame.draw.rect(self.screen, BUTTON_COLOR, back_rect, border_radius=5)
        back_text = self.THEME_FONT.render("Back", True, TEXT_COLOR)
        self.screen.blit(back_text, (back_rect.centerx - 25, back_rect.centery - 10))
        
        pygame.display.flip()
    
    def draw_game(self, board, current_theme, current_player, selected_square, valid_moves, game_over=False, winner=None):
        """Draw the game board and interface"""
        theme = THEMES[current_theme]
        self.screen.fill(BACKGROUND_COLOR)
        
        for row in range(ROWS):
            for col in range(COLS):
                x = MARGIN_X + col * SQUARE_SIZE
                y = MARGIN_Y + row * SQUARE_SIZE
                
                if selected_square and (row, col) == selected_square:
                    color = HIGHLIGHT_COLOR
                elif valid_moves and (row, col) in valid_moves:
                    color = VALID_MOVE_COLOR
                elif (row + col) % 2 == 0:
                    color = theme["light"]
                else:
                    color = theme["dark"]
                
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                piece = board[row][col]
                if piece:
                    color, piece_type = piece
                    text = self.PIECE_FONT.render(PIECES[color][piece_type], True, 
                                        (255, 255, 255) if color == 'white' else (50, 50, 50))
                    self.screen.blit(text, (x + SQUARE_SIZE//2 - text.get_width()//2, 
                                        y + SQUARE_SIZE//2 - text.get_height()//2))
        
        for i in range(COLS):
            letter = chr(97 + i)
            text = self.STATUS_FONT.render(letter, True, COORDINATES_COLOR)
            self.screen.blit(text, (MARGIN_X + i*SQUARE_SIZE + SQUARE_SIZE//2 - 5, 
                                MARGIN_Y + ROWS*SQUARE_SIZE + 10))
        
        for i in range(ROWS):
            number = str(ROWS - i)
            text = self.STATUS_FONT.render(number, True, COORDINATES_COLOR)
            self.screen.blit(text, (MARGIN_X - 25, MARGIN_Y + i*SQUARE_SIZE + SQUARE_SIZE//2 - 10))
        

        status_bar = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)
        pygame.draw.rect(self.screen, STATUS_BAR_COLOR, status_bar)
        
        
        if game_over:
            if winner == "draw":
                status_text = "Game Over - Draw"
            else:
                status_text = f"Game Over - {winner.capitalize()} wins"
            turn_text = self.STATUS_FONT.render(status_text, True, GOLD_COLOR)
        else:
            turn_text = self.STATUS_FONT.render(f"{current_player.capitalize()}'s turn", True, TEXT_COLOR)
        self.screen.blit(turn_text, (20, HEIGHT - 30))
        
        
        undo_rect = pygame.Rect(WIDTH - 220, HEIGHT - 35, 80, 30)
        redo_rect = pygame.Rect(WIDTH - 120, HEIGHT - 35, 80, 30)
        theme_rect = pygame.Rect(WIDTH - 350, HEIGHT - 35, 110, 30)
        
        
        self.button_rects = {
            "undo": undo_rect,
            "redo": redo_rect,
            "theme": theme_rect
        }
        
       
        pygame.draw.rect(self.screen, BUTTON_COLOR, undo_rect, border_radius=5)
        pygame.draw.rect(self.screen, BUTTON_COLOR, redo_rect, border_radius=5)
        pygame.draw.rect(self.screen, BUTTON_COLOR, theme_rect, border_radius=5)
        
        
        undo_text = self.STATUS_FONT.render("📄 Undo", True, TEXT_COLOR)
        redo_text = self.STATUS_FONT.render("🍀 Redo", True, TEXT_COLOR)
        theme_text = self.STATUS_FONT.render("Themes", True, TEXT_COLOR)
        
        self.screen.blit(undo_text, (undo_rect.centerx - undo_text.get_width()//2, 
                                undo_rect.centery - undo_text.get_height()//2))
        self.screen.blit(redo_text, (redo_rect.centerx - redo_text.get_width()//2, 
                                redo_rect.centery - redo_text.get_height()//2))
        self.screen.blit(theme_text, (theme_rect.centerx - theme_text.get_width()//2, 
                                    theme_rect.centery - theme_text.get_height()//2))
        
        
        if game_over:
            self.draw_game_over(winner)
        
        
        pygame.display.flip()
    def get_button_rects(self):
        """Return button rectangles for event handling"""
        return self.button_rects
    
    def check_main_menu_click(self, pos):
        """Check which option was clicked in the main menu"""
        if WIDTH//2 - 100 <= pos[0] <= WIDTH//2 + 100:
            if 250 <= pos[1] <= 300:  
                return "new_game"
            elif 330 <= pos[1] <= 380:  
                return "quit"
        return None
    
    def check_theme_menu_click(self, pos):
        """Check which theme was clicked in the theme menu"""
        
        for i in range(8):
            if (20 <= pos[0] <= WIDTH//2 - 10 and 
                70 + i*40 <= pos[1] <= 110 + i*40):
                return list(THEMES.keys())[i]
        
        
        for i in range(8, 16):
            if (WIDTH//2 + 10 <= pos[0] <= WIDTH - 20 and 
                70 + (i-8)*40 <= pos[1] <= 110 + (i-8)*40):
                return list(THEMES.keys())[i]
        
       
        if (20 <= pos[0] <= 120 and 
            HEIGHT - 60 <= pos[1] <= HEIGHT - 20):
            return "back"
        
        return None
        
    def draw_game_over(self, winner):
        """Draw the game over screen with winner information and buttons"""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        panel_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 120, 300, 240)
        pygame.draw.rect(self.screen, MENU_BACKGROUND, panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, GOLD_COLOR, panel_rect, 3, border_radius=15)
        
        game_over_text = self.TITLE_FONT.render("Game Over", True, GOLD_COLOR)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        if winner == "draw":
            winner_text = self.MENU_FONT.render("Draw by Stalemate", True, TEXT_COLOR)
        else:
            winner_text = self.MENU_FONT.render(f"{winner.capitalize()} Wins!", True, TEXT_COLOR)
        winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
        self.screen.blit(winner_text, winner_rect)
        
        new_game_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 20, 240, 40)
        quit_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 80, 240, 40)
        
        self.game_over_buttons = {
            "new_game": new_game_rect,
            "quit": quit_rect
        }
        
        mouse_pos = pygame.mouse.get_pos()
        
        new_game_color = BUTTON_COLOR
        if new_game_rect.collidepoint(mouse_pos):
            new_game_color = (100, 100, 160)
        pygame.draw.rect(self.screen, new_game_color, new_game_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 255), new_game_rect, 2, border_radius=8)
        
        quit_color = BUTTON_COLOR
        if quit_rect.collidepoint(mouse_pos):
            quit_color = (100, 100, 160)
        pygame.draw.rect(self.screen, quit_color, quit_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 255), quit_rect, 2, border_radius=8)
        
        new_game_text = self.MENU_FONT.render("New Game", True, TEXT_COLOR)
        new_game_text_rect = new_game_text.get_rect(center=new_game_rect.center)
        self.screen.blit(new_game_text, new_game_text_rect)
        
        quit_text = self.MENU_FONT.render("Quit", True, TEXT_COLOR)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        self.screen.blit(quit_text, quit_text_rect)
    def check_game_over_click(self, pos):
        """Check clicks on game over screen"""
        if hasattr(self, 'game_over_buttons'):
            for button_name, button_rect in self.game_over_buttons.items():
                if button_rect.collidepoint(pos):
                    return button_name
        return None