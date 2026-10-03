import pygame
import os

from scripts.button import Button, ToggleButton

from menu_config import MenuConfig
from settings import Settings
from game_state import GameState

from scripts.text import Text
from scripts.map import Map
from scripts.timer import Timer

class MenuState():
    def __init__(self,display,parent):

        #___/Initialisation du parent\___
        self.parent = parent

        #___/Initialisation de pygame\___
        self.display = display
        self.screen = pygame.Surface(Settings.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        
        #___/Initialisation des états\___
        self.run = True
        self.key_pressed = {}
        self.current_page = "main_menu"
        self.previous_page = "main_menu"
        self.current_map_selection = self.get_map_name("assets/maps")[0]
        self.timer = Timer()

        #___/Initialisation des boutons du Main menu\___

        center_x = Settings.SCREEN_RESOLUTION[0] // 2
        offset_y = 80
        self.main_menu_buttons = pygame.sprite.Group()
        self.main_menu_buttons.add(Button(center_x,0 + offset_y,self.button_start_pressed,MenuConfig.BUTTON_JOUER_STILL,MenuConfig.BUTTON_JOUER_HOVERED,MenuConfig.BUTTON_JOUER_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton commencer
        self.main_menu_buttons.add(Button(center_x,30 + offset_y,self.button_editeur,MenuConfig.EDITEUR_STILL,MenuConfig.EDITEUR_HOVERED,MenuConfig.EDITEUR_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton editeur
        self.main_menu_buttons.add(Button(center_x,60 + offset_y,self.button_option_pressed,MenuConfig.BUTTON_OPTIONS_STILL,MenuConfig.BUTTON_OPTIONS_HOVERED,MenuConfig.BUTTON_OPTIONS_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton option
        self.main_menu_buttons.add(Button(center_x,90 + offset_y,self.button_quit_pressed,MenuConfig.BUTTON_QUITTER_STILL,MenuConfig.BUTTON_QUITTER_HOVERED,MenuConfig.BUTTON_QUITTER_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton quitter
        
        
        #___/Initialisation des BUTTONs du menu pause\___
        self.pause_menu_buttons = pygame.sprite.Group()
        self.pause_menu_buttons.add(Button(center_x,40,self.button_resume_pressed,MenuConfig.BUTTON_REPRENDRE_STILL,MenuConfig.BUTTON_REPRENDRE_HOVERED,MenuConfig.BUTTON_REPRENDRE_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton reprendre
        self.pause_menu_buttons.add(Button(center_x,70,self.button_restart_pressed,MenuConfig.BUTTON_RECOMMENCER_STILL,MenuConfig.BUTTON_RECOMMENCER_HOVERED,MenuConfig.BUTTON_RECOMMENCER_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton recommencer
        self.pause_menu_buttons.add(Button(center_x,100,self.button_option_pressed,MenuConfig.BUTTON_OPTIONS_STILL,MenuConfig.BUTTON_OPTIONS_HOVERED,MenuConfig.BUTTON_OPTIONS_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton option
        self.pause_menu_buttons.add(Button(center_x,130,self.button_main_menu_pressed,MenuConfig.BUTTON_MENU_PRINCIPAL_STILL,MenuConfig.BUTTON_MENU_PRINCIPAL_HOVERED,MenuConfig.BUTTON_MENU_PRINCIPAL_CLICKED,scale_factor=2, center=True,play_sound=True))#Bouton menu principale
        


        #___/Initialise les buttons du menu config\___
        self.option_menu_buttons = pygame.sprite.Group()
        self.option_menu_buttons.add(ToggleButton(center_x,30,self.button_fps_pressed,MenuConfig.SHOW_FPS_STILL,MenuConfig.SHOW_FPS_STILL_PRESSED,MenuConfig.SHOW_FPS_HOVERED,MenuConfig.SHOW_FPS_HOVERED_PRESSED,MenuConfig.SHOW_FPS_CLICKED,MenuConfig.SHOW_FPS_CLICKED_PRESSED,scale_factor=2,center=True,pressed_by_default=Settings.SHOW_FPS,play_sound=True))
        self.option_menu_buttons.add(ToggleButton(center_x,60,self.button_full_screen,MenuConfig.FULLSCREEN_STILL,MenuConfig.FULLSCREEN_STILL_PRESSED,MenuConfig.FULLSCREEN_HOVERED,MenuConfig.FULLSCREEN_HOVERED_PRESSED,MenuConfig.FULLSCREEN_CLICKED,MenuConfig.FULLSCREEN_CLICKED_PRESSED,scale_factor=2,center=True,pressed_by_default=Settings.FULLSCREEN,play_sound=True))
        self.option_menu_buttons.add(ToggleButton(center_x,90,self.button_play_music,MenuConfig.MUSIC_STILL,MenuConfig.MUSIC_STILL_PRESSED,MenuConfig.MUSIC_HOVERED,MenuConfig.MUSIC_HOVERED_PRESSED,MenuConfig.MUSIC_CLICKED,MenuConfig.MUSIC_CLICKED_PRESSED,scale_factor=2,center=True,pressed_by_default=Settings.PLAY_MUSIC,play_sound=True))
        self.option_menu_buttons.add(Button(center_x + 20, 150 ,lambda: self.button_change_volume("up"),MenuConfig.INCREASE_BUTTON,MenuConfig.INCREASE_BUTTON_HOVERED,scale_factor=1,center=True))
        self.option_menu_buttons.add(Button(center_x - 20 , 150,lambda: self.button_change_volume("down"),MenuConfig.DECREASE_BUTTON,MenuConfig.DECREASE_BUTTON_HOVERED,scale_factor=1,center=True))
        self.option_menu_buttons.add(Button(5 ,5 ,self.button_return,MenuConfig.RETURN_STILL,MenuConfig.RETURN_HOVERED,MenuConfig.RETURN_CLICKED,scale_factor=1.5,play_sound=True))


        #___/Initialise les buttons du menu editeur selection\___
        self.editeur_selection_buttons = pygame.sprite.Group()
        self.editeur_selection_buttons.add(Button(0,Settings.SCREEN_RESOLUTION[1] - 14,self.button_delete_map,MenuConfig.SUPPRIMER_LA_CARTE_STILL,MenuConfig.SUPPRIMER_LA_CARTE_HOVERED,MenuConfig.SUPPRIMER_LA_CARTE_CLICKED,scale_factor=1.5,play_sound=True))
        self.editeur_selection_buttons.add(Button(Settings.SCREEN_RESOLUTION[0],Settings.SCREEN_RESOLUTION[1] - 14,self.button_create_map,MenuConfig.CREER_UNE_NOUVELLE_CARTE_STILL,MenuConfig.CREER_UNE_NOUVELLE_CARTE_HOVERED,MenuConfig.CREER_UNE_NOUVELLE_CARTE_CLICKED,scale_factor=1.5,top_right=True))
        self.editeur_selection_buttons.add(Button(center_x,140,self.button_selection_editor_map,MenuConfig.SELECTIONNER_STILL,MenuConfig.SELECTIONNER_HOVERED,MenuConfig.SELECTIONNER_CLICKED,scale_factor=1.5,center=True,play_sound=True))
        self.editeur_selection_buttons.add(Button(center_x + 50, 110 ,lambda: self.button_change_map_selection("right"),MenuConfig.INCREASE_BUTTON,MenuConfig.INCREASE_BUTTON_HOVERED,scale_factor=1,center=True,play_sound=True))
        self.editeur_selection_buttons.add(Button(center_x - 50 , 110,lambda: self.button_change_map_selection("left"),MenuConfig.DECREASE_BUTTON,MenuConfig.DECREASE_BUTTON_HOVERED,scale_factor=1,center=True,play_sound=True))
        self.editeur_selection_buttons.add(Button(5 ,5 ,self.button_return,MenuConfig.RETURN_STILL,MenuConfig.RETURN_HOVERED,MenuConfig.RETURN_CLICKED,scale_factor=1.5,play_sound=True))

        #___/Initialise les buttons du menu jouer selection\___
        self.jouer_selection_buttons = pygame.sprite.Group()
        self.jouer_selection_buttons.add(Button(center_x,140,self.button_selection_editor_map,MenuConfig.SELECTIONNER_STILL,MenuConfig.SELECTIONNER_HOVERED,MenuConfig.SELECTIONNER_CLICKED,scale_factor=1.5,center=True,play_sound=True))
        self.jouer_selection_buttons.add(Button(center_x + 50, 110 ,lambda: self.button_change_map_selection("right"),MenuConfig.INCREASE_BUTTON,MenuConfig.INCREASE_BUTTON_HOVERED,scale_factor=1,center=True,play_sound=True))
        self.jouer_selection_buttons.add(Button(center_x - 50 , 110,lambda: self.button_change_map_selection("left"),MenuConfig.DECREASE_BUTTON,MenuConfig.DECREASE_BUTTON_HOVERED,scale_factor=1,center=True,play_sound=True))
        self.jouer_selection_buttons.add(Button(5 ,5 ,self.button_return,MenuConfig.RETURN_STILL,MenuConfig.RETURN_HOVERED,MenuConfig.RETURN_CLICKED,scale_factor=1.5,play_sound=True))
    
    #___/Gère les events\___
    def events(self):
        """
        Fonction qui gère les événements du menu principal
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_page != "main_menu":
                        if self.current_page == "pause_menu":
                            self.parent.current_state = "game"
                        else:
                            self.current_page = self.previous_page

                if event.key == pygame.K_y:
                    self.timer.start_timer()


                if event.key == pygame.K_u:
                    print(self.timer.get_time())


                if event.key == pygame.K_i:
                    self.timer.pause_timer()
                    print(self.timer.get_time())
                    


                if event.key == pygame.K_o:
                    self.timer.resume_timer()
                    print(self.timer.get_time())


    ###################################
    ####     BUTTON ACTION part    ####
    ###################################

    #___/Actions pour les boutons du menu pause\___
    def button_resume_pressed(self) :
        self.parent.current_state = "game"
    
    def button_restart_pressed(self):
        self.parent.game_state.initialize_game(self.current_map_selection)
        self.parent.current_state = "game"

    def button_option_pressed(self):
        self.previous_page = self.current_page
        self.current_page = "option_menu"
    
    def button_main_menu_pressed(self):
        self.current_page = "main_menu"
    
    def button_start_pressed(self):
        if Settings.PLAY_INTRO:
            self.parent.current_state = "game"
            self.current_page = "pause_menu"
            self.current_map_selection = "intro"
            self.parent.game_state.initialize_game("intro")
            self.parent.game_state.current_state = "intro"
        else:
            self.current_page = "jouer_selection_menu"
    
    
    def button_quit_pressed(self) :
        pygame.quit()
        exit()
    
    def button_credit_pressed(self) :
        self.previous_page = self.current_page
        self.current_page = "credit_menu"

    def button_fps_pressed(self):
        Settings.change_show_fps()

    def button_full_screen(self):
        Settings.change_full_screen()

    def button_play_music(self):
        Settings.change_play_music()
        pygame.mixer.music.set_volume(Settings.MUSIC_VOLUME if Settings.PLAY_MUSIC else 0)


    def button_change_volume(self,value):
        Settings.change_volume(value)
        pygame.mixer.music.set_volume(Settings.MUSIC_VOLUME if Settings.PLAY_MUSIC else 0)
        
    def button_return(self):
        self.current_page = self.previous_page

    def button_editeur(self):
        self.previous_page = self.current_page
        self.current_page = "editeur_selection_menu"



    def button_change_map_selection(self,value):
        maps_name = self.get_map_name("assets/maps")
        current_map_indice = maps_name.index(self.current_map_selection)

        if value == "left":
            self.current_map_selection = maps_name[max(0,current_map_indice-1)]
        elif value == "right":
            self.current_map_selection = maps_name[min(len(maps_name)-1,current_map_indice+1)]

    def button_selection_editor_map(self):
        if self.current_page == "editeur_selection_menu":
            self.parent.editor_state.load_map(self.current_map_selection)
            self.parent.current_state = "editor"
        elif self.current_page == "jouer_selection_menu":
            self.parent.current_state = "game"
            self.current_page = "pause_menu"
            self.parent.game_state.initialize_game(self.current_map_selection)
            self.parent.game_state.current_state = "playing"


    def button_create_map(self):
        map = Map()
        map_names = self.get_map_name("assets/maps")
        if len(map_names) < 10:
            for i in range(1, 11): 
                map_name = f"map{i}"
                if map_name not in map_names:
                    map.create(map_name, 10, 10) 
                    print(f"La carte {map_name} a été créée.")
                    return


    def button_delete_map(self):
        if self.current_map_selection not in ["Main","intro"]:
            map = Map()
            map.name = self.current_map_selection
            self.button_change_map_selection("left")
            map.delete()
            



    ##########################
    ####     Utils part    ####
    ##########################


    def get_map_name(self,path):
        """
        Permet de d'obtenir le nom de toutes les maps situées dans le dossier
        """
        data = os.listdir(path)
        dossiers = [name for name in data if os.path.isdir(os.path.join(path, name))]
        return dossiers


    ##########################
    ####     Draw part    ####
    ##########################
    
    def render(self):
        """
        Gére les évenements
        """
        
        pygame.display.flip()
        self.clock.tick(Settings.GAME_FPS)

    def draw_cursor(self):
        """
        Méthode qui dessine le curseur sur l'écran
        """
        x,y = pygame.mouse.get_pos()
        self.display.blit(MenuConfig.ARROW4,(x,y))


    def draw(self):
        self.screen.fill((0,0,0))
        
        #___/SCREEN\__
        if self.current_page == "main_menu":
            self.draw_main_menu()
        elif self.current_page == "pause_menu":
            self.draw_pause_menu()

        elif self.current_page == "option_menu":
            self.draw_option_menu()
        elif self.current_page == "editeur_selection_menu":
            self.draw_editeur_selection_menu()
        elif self.current_page == "jouer_selection_menu":
            self.draw_jouer_selection_menu()
        
        self.display.blit(pygame.transform.scale(self.screen, Settings.DISPLAY_RESOLUTION), (0,0))

        #___/DISPLAY\___
        self.draw_cursor()


    def draw_main_menu(self):
        center_x = Settings.SCREEN_RESOLUTION[0] //2 
        self.main_menu_buttons.draw(self.screen)
        self.screen.blit(MenuConfig.GAME_LOGO,(center_x - MenuConfig.GAME_LOGO.get_width()//2,0))

    def draw_pause_menu(self):
        self.pause_menu_buttons.draw(self.screen)

    def draw_option_menu(self):
        center_x = Settings.SCREEN_RESOLUTION[0] //2 
        self.option_menu_buttons.draw(self.screen)
        self.screen.blit(MenuConfig.MUSIQUE_VOLUME_TEXTE,(center_x - MenuConfig.MUSIQUE_VOLUME_TEXTE.get_width()//2,120))
        Text.draw_text(self.screen,str(Settings.MUSIC_VOLUME)[:3],15,(center_x,150),(255,255,255),center=True)


    def draw_editeur_selection_menu(self):
        center_x = Settings.SCREEN_RESOLUTION[0] //2 
        self.editeur_selection_buttons.draw(self.screen)
        self.screen.blit(MenuConfig.SELECTIONNER_LA_CARTE,(center_x - MenuConfig.SELECTIONNER_LA_CARTE.get_width()//2,30))
        Text.draw_text(self.screen,self.current_map_selection,15,(center_x,110),(255,255,255),center=True)

    def draw_jouer_selection_menu(self):
        center_x = Settings.SCREEN_RESOLUTION[0] //2 
        self.jouer_selection_buttons.draw(self.screen)
        self.screen.blit(MenuConfig.SELECTIONNER_LA_CARTE,(center_x - MenuConfig.SELECTIONNER_LA_CARTE.get_width()//2,30))
        Text.draw_text(self.screen,self.current_map_selection,15,(center_x,110),(255,255,255),center=True)


    



    def editeur_selection_loop(self):
        self.events()
        self.editeur_selection_buttons.update()
        self.draw()
        self.render()

    def pause_loop(self):
        self.events()
        self.pause_menu_buttons.update()
        self.draw()
        self.render()

    def menu_loop(self) :
        self.events()
        self.main_menu_buttons.update()
        self.draw()
        self.render()

    def option_loop(self):
        self.events()
        self.option_menu_buttons.update()
        self.draw()
        self.render()

    def jouer_selection_loop(self):
        self.events()
        self.jouer_selection_buttons.update()
        self.draw()
        self.render()



    #___/Gère les boucles des différents menu\___
    def main_loop(self):
        if self.current_page == "main_menu":
            self.menu_loop()
        elif self.current_page == "pause_menu":
            self.pause_loop()
        elif self.current_page == "option_menu":
            self.option_loop()

        elif self.current_page == "editeur_selection_menu":
            self.editeur_selection_loop()

        elif self.current_page == "jouer_selection_menu":
            self.jouer_selection_loop()
        
        else:
            self.menu_loop()
    


