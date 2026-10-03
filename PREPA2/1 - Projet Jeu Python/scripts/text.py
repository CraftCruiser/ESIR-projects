import pygame


class Text():
    def draw_text(screen, text, font_size, position, color=(255, 255, 255), font_path=None,center= False):
        font = pygame.font.Font(font_path, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if not center:
            text_rect.topleft = position
        else:
            text_rect.center = position
        
        screen.blit(text_surface, text_rect)
        return text_rect