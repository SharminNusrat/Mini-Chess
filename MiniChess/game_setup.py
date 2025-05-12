import pygame
from pygame.locals import *
from constants import *

class GameSetupMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("georgia", 40, bold=True)
        self.font_subtitle = pygame.font.SysFont("arial", 24)
        self.font_text = pygame.font.SysFont("arial", 20)
        
        self.white_player = "human"  # Default: human
        self.black_player = "ai"     # Default: AI
        
        self.start_button_rect = pygame.Rect(WIDTH//2 - 90, HEIGHT - 140, 180, 50)
    
    def draw(self):
        """Draw the game setup menu"""
        self.screen.fill((240, 245, 250))  # Light blue-gray background
        
        title = self.font_title.render("MiniChess Setup", True, (40, 60, 80))
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_subtitle.render("Configure your game settings", True, (100, 120, 140))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 140))
        self.screen.blit(subtitle, subtitle_rect)
        
        pygame.draw.line(self.screen, (200, 210, 220), (40, 190), (WIDTH-40, 190), 2)
        pygame.draw.line(self.screen, (200, 210, 220), (40, 590), (WIDTH-40, 590), 2)
        
        white_title = self.font_subtitle.render("White Player", True, (70, 90, 110))
        self.screen.blit(white_title, (75, 240))
        
        white_human_color = (0, 105, 209) if self.white_player == "human" else (150, 150, 150)
        white_ai_color = (0, 105, 209) if self.white_player == "ai" else (150, 150, 150)
        
        pygame.draw.circle(self.screen, (220, 230, 240), (85, 298), 18)
        pygame.draw.circle(self.screen, (220, 230, 240), (85, 340), 18)
        
        if self.white_player == "human":
            pygame.draw.circle(self.screen, white_human_color, (85, 298), 10)
        else:
            pygame.draw.circle(self.screen, white_ai_color, (85, 340), 10)
        
        white_human = self.font_text.render("Human Player", True, (70, 90, 110))
        white_ai = self.font_text.render("AI Player", True, (70, 90, 110))
        self.screen.blit(white_human, (110, 290))
        self.screen.blit(white_ai, (110, 332))
        
        black_title = self.font_subtitle.render("Black Player", True, (70, 90, 110))
        self.screen.blit(black_title, (75, 415))
        
        black_human_color = (0, 105, 209) if self.black_player == "human" else (150, 150, 150)
        black_ai_color = (0, 105, 209) if self.black_player == "ai" else (150, 150, 150)
        
        pygame.draw.circle(self.screen, (220, 230, 240), (85, 473), 18)
        pygame.draw.circle(self.screen, (220, 230, 240), (85, 515), 18)
        
        if self.black_player == "human":
            pygame.draw.circle(self.screen, black_human_color, (85, 473), 10)
        else:
            pygame.draw.circle(self.screen, black_ai_color, (85, 515), 10)
        
        black_human = self.font_text.render("Human Player", True, (70, 90, 110))
        black_ai = self.font_text.render("AI Player", True, (70, 90, 110))
        self.screen.blit(black_human, (110, 465))
        self.screen.blit(black_ai, (110, 507))
        
        pygame.draw.rect(self.screen, (240, 240, 240), self.start_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (0, 105, 209), self.start_button_rect, 2, border_radius=8)
        
        mouse_pos = pygame.mouse.get_pos()
        if self.start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (230, 240, 255), self.start_button_rect, border_radius=8)
            pygame.draw.rect(self.screen, (0, 105, 209), self.start_button_rect, 2, border_radius=8)
        
        start_text = self.font_subtitle.render("Start Game", True, (40, 60, 80))
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)
        
        pygame.display.flip()
    
    def handle_click(self, pos):
        """Handle mouse clicks in the setup menu"""
        x, y = pos
        
        if 65 <= x <= 105:
            if 280 <= y <= 316:  
                self.white_player = "human"
                return None
            elif 322 <= y <= 358:  
                self.white_player = "ai"
                return None
        
        
        if 65 <= x <= 105:
            if 455 <= y <= 491: 
                self.black_player = "human"
                return None
            elif 497 <= y <= 533:  
                self.black_player = "ai"
                return None
        
        if self.start_button_rect.collidepoint(pos):
            return {"white_player": self.white_player, "black_player": self.black_player}
        
        return None