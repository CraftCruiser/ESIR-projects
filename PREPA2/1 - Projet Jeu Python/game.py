import pygame
 
from game_state import GameState
from editor_state import EditorState
from menu_state import MenuState

from settings import Settings
from menu_config import MenuConfig
from editor_config import EditorConfig




class Game():
    def __init__(self):
        Settings.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(Settings.DISPLAY_RESOLUTION, pygame.FULLSCREEN if Settings.FULLSCREEN else 0)
        self.current_state = "menu"
        pygame.mouse.set_visible(False) #On cache le curseur

        pygame.display.set_icon(pygame.image.load("assets/others/game_icon.png")) #On change l'icone de la fenêtre
        pygame.display.set_caption("Knight Tower") # On change le nom de la fenêtre
        
        pygame.mixer.music.load("assets/musics/game.ogg") # On charge la musique
        pygame.mixer.music.play(-1) # On joue la musique
        pygame.mixer.music.set_volume(Settings.MUSIC_VOLUME if Settings.PLAY_MUSIC else 0) # On change le volume


    def launch_game(self):
        """
        Permet de lancer le jeu
        """
        MenuConfig.init()
        EditorConfig.init()
        
        
        self.game_state = GameState(self.display,self)
        self.menu_state = MenuState(self.display,self)
        self.editor_state = EditorState(self.display,self)
        
        self.game_loop()
        

    def restart_game(self):
        """
        Permet de relancer la partie
        """
        
        self.game_state = GameState(self.display,self)
        


    

    def game_loop(self):
        """
        Permet de gérer les différentes boucles du jeu
        """
        run = True
        while run:
            #Si l'état courant est
            if self.current_state == "menu":  #on affiche le menu
                self.menu_state.main_loop()

            elif self.current_state == "editor": #on affiche l'éditeur
                self.editor_state.main_loop()
                
            elif self.current_state == "game": #on affiche le jeu
                self.game_state.main_loop()
            

            
        

    
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.launch_game()
    


