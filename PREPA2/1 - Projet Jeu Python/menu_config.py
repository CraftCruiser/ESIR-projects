import pygame
from scripts.image import Images


class MenuConfig :

    TILE_SIZE = 16

    
    def init() :
        #___/Initialisation des BUTTONs du main menu\___
        MenuConfig.BUTTON_JOUER_STILL = pygame.image.load("assets/buttons/menu_buttons/jouer_button/jouer_still.png").convert_alpha()
        MenuConfig.BUTTON_JOUER_CLICKED = pygame.image.load("assets/buttons/menu_buttons/jouer_button/jouer_clicked.png").convert_alpha()
        MenuConfig.BUTTON_JOUER_HOVERED = pygame.image.load("assets/buttons/menu_buttons/jouer_button/jouer_hovered.png").convert_alpha()

        MenuConfig.BUTTON_QUITTER_STILL = pygame.image.load("assets/buttons/menu_buttons/quitter_button/quitter_still.png").convert_alpha()
        MenuConfig.BUTTON_QUITTER_CLICKED = pygame.image.load("assets/buttons/menu_buttons/quitter_button/quitter_clicked.png").convert_alpha()
        MenuConfig.BUTTON_QUITTER_HOVERED = pygame.image.load("assets/buttons/menu_buttons/quitter_button/quitter_hovered.png").convert_alpha()

        MenuConfig.BUTTON_CREDIT_STILL = pygame.image.load("assets/buttons/menu_buttons/credit_button/credit_still.png").convert_alpha()
        MenuConfig.BUTTON_CREDIT_CLICKED = pygame.image.load("assets/buttons/menu_buttons/credit_button/credit_clicked.png").convert_alpha()
        MenuConfig.BUTTON_CREDIT_HOVERED = pygame.image.load("assets/buttons/menu_buttons/credit_button/credit_hovered.png").convert_alpha()

        MenuConfig.BUTTON_OPTIONS_STILL = pygame.image.load("assets/buttons/menu_buttons/options_button/options_still.png").convert_alpha()
        MenuConfig.BUTTON_OPTIONS_CLICKED = pygame.image.load("assets/buttons/menu_buttons/options_button/options_clicked.png").convert_alpha()
        MenuConfig.BUTTON_OPTIONS_HOVERED = pygame.image.load("assets/buttons/menu_buttons/options_button/options_hovered.png").convert_alpha()
        
        MenuConfig.BUTTON_REPRENDRE_STILL = pygame.image.load("assets/buttons/menu_buttons/reprendre_button/reprendre_still.png").convert_alpha()
        MenuConfig.BUTTON_REPRENDRE_CLICKED = pygame.image.load("assets/buttons/menu_buttons/reprendre_button/reprendre_clicked.png").convert_alpha()
        MenuConfig.BUTTON_REPRENDRE_HOVERED = pygame.image.load("assets/buttons/menu_buttons/reprendre_button/reprendre_hovered.png").convert_alpha()

        MenuConfig.BUTTON_MENU_PRINCIPAL_STILL = pygame.image.load("assets/buttons/menu_buttons/menu_principal_button/menu_principal_still.png").convert_alpha()
        MenuConfig.BUTTON_MENU_PRINCIPAL_CLICKED = pygame.image.load("assets/buttons/menu_buttons/menu_principal_button/menu_principal_clicked.png").convert_alpha()
        MenuConfig.BUTTON_MENU_PRINCIPAL_HOVERED = pygame.image.load("assets/buttons/menu_buttons/menu_principal_button/menu_principal_hovered.png").convert_alpha()

        MenuConfig.BUTTON_RECOMMENCER_STILL = pygame.image.load("assets/buttons/menu_buttons/recommencer_button/recommencer_still.png").convert_alpha()
        MenuConfig.BUTTON_RECOMMENCER_CLICKED = pygame.image.load("assets/buttons/menu_buttons/recommencer_button/recommencer_clicked.png").convert_alpha()
        MenuConfig.BUTTON_RECOMMENCER_HOVERED = pygame.image.load("assets/buttons/menu_buttons/recommencer_button/recommencer_hovered.png").convert_alpha()

        MenuConfig.GAME_LOGO = pygame.image.load("assets/others/game_logo.png").convert_alpha()

        #___/BUTTON RETURN\___
        MenuConfig.RETURN_STILL = pygame.image.load("assets/buttons/menu_buttons/return_button/return_still.png").convert_alpha()
        MenuConfig.RETURN_HOVERED = pygame.image.load("assets/buttons/menu_buttons/return_button/return_hovered.png").convert_alpha()
        MenuConfig.RETURN_CLICKED = pygame.image.load("assets/buttons/menu_buttons/return_button/return_clicked.png").convert_alpha()



        #___/BUTTON SHOW FPS\___
        MenuConfig.SHOW_FPS_STILL = pygame.image.load("assets/buttons/menu_buttons/showfps/show_fps_still.png").convert_alpha()
        MenuConfig.SHOW_FPS_STILL_PRESSED = pygame.image.load("assets/buttons/menu_buttons/showfps/show_fps_still_pressed.png").convert_alpha()
        MenuConfig.SHOW_FPS_HOVERED = pygame.image.load("assets/buttons/menu_buttons/showfps/show_fps_hovered.png").convert_alpha()
        MenuConfig.SHOW_FPS_HOVERED_PRESSED = pygame.image.load("assets/buttons/menu_buttons/showfps/show_fps_hovered_pressed.png").convert_alpha()
        MenuConfig.SHOW_FPS_CLICKED = pygame.image.load("assets/buttons/menu_buttons/showfps/show_fps_clicked.png").convert_alpha()
        MenuConfig.SHOW_FPS_CLICKED_PRESSED = pygame.image.load("assets/buttons/menu_buttons/showfps/show_fps_clicked_pressed.png").convert_alpha()

        #___/BUTTON FULLSCREEN\___
        MenuConfig.FULLSCREEN_STILL = pygame.image.load("assets/buttons/menu_buttons/fullscreen/fullscreen_still.png").convert_alpha()
        MenuConfig.FULLSCREEN_STILL_PRESSED = pygame.image.load("assets/buttons/menu_buttons/fullscreen/fullscreen_still_pressed.png").convert_alpha()
        MenuConfig.FULLSCREEN_HOVERED = pygame.image.load("assets/buttons/menu_buttons/fullscreen/fullscreen_hovered.png").convert_alpha()
        MenuConfig.FULLSCREEN_HOVERED_PRESSED = pygame.image.load("assets/buttons/menu_buttons/fullscreen/fullscreen_hovered_pressed.png").convert_alpha()
        MenuConfig.FULLSCREEN_CLICKED = pygame.image.load("assets/buttons/menu_buttons/fullscreen/fullscreen_clicked.png").convert_alpha()
        MenuConfig.FULLSCREEN_CLICKED_PRESSED = pygame.image.load("assets/buttons/menu_buttons/fullscreen/fullscreen_clicked_pressed.png").convert_alpha()

        #___/BUTTON MUSIC\___
        MenuConfig.MUSIC_STILL = pygame.image.load("assets/buttons/menu_buttons/music/music_still.png").convert_alpha()
        MenuConfig.MUSIC_STILL_PRESSED = pygame.image.load("assets/buttons/menu_buttons/music/music_still_pressed.png").convert_alpha()
        MenuConfig.MUSIC_HOVERED = pygame.image.load("assets/buttons/menu_buttons/music/music_hovered.png").convert_alpha()
        MenuConfig.MUSIC_HOVERED_PRESSED = pygame.image.load("assets/buttons/menu_buttons/music/music_hovered_pressed.png").convert_alpha()
        MenuConfig.MUSIC_CLICKED = pygame.image.load("assets/buttons/menu_buttons/music/music_clicked.png").convert_alpha()
        MenuConfig.MUSIC_CLICKED_PRESSED = pygame.image.load("assets/buttons/menu_buttons/music/music_clicked_pressed.png").convert_alpha()

        MenuConfig.INCREASE_BUTTON = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,0)
        MenuConfig.DECREASE_BUTTON = pygame.transform.flip(Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,0),True,False)
        
        MenuConfig.INCREASE_BUTTON_HOVERED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,3)
        MenuConfig.DECREASE_BUTTON_HOVERED = pygame.transform.flip(Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,3),True,False)

        #___/EDITEUR\___
        MenuConfig.EDITEUR_STILL = pygame.image.load("assets/buttons/menu_buttons/editeur_button/editeur_still.png").convert_alpha()
        MenuConfig.EDITEUR_CLICKED = pygame.image.load("assets/buttons/menu_buttons/editeur_button/editeur_clicked.png").convert_alpha()
        MenuConfig.EDITEUR_HOVERED = pygame.image.load("assets/buttons/menu_buttons/editeur_button/editeur_hovered.png").convert_alpha()


        #___/SUPPRIMER LA CARTE\___
        MenuConfig.SUPPRIMER_LA_CARTE_STILL = pygame.image.load("assets/buttons/menu_buttons/supprimer_la_carte_button/supprimer_la_carte_still.png").convert_alpha()
        MenuConfig.SUPPRIMER_LA_CARTE_CLICKED = pygame.image.load("assets/buttons/menu_buttons/supprimer_la_carte_button/supprimer_la_carte_clicked.png").convert_alpha()
        MenuConfig.SUPPRIMER_LA_CARTE_HOVERED = pygame.image.load("assets/buttons/menu_buttons/supprimer_la_carte_button/supprimer_la_carte_hovered.png").convert_alpha()

        #___/CREER UNE NOUVELLE CARTE\___
        MenuConfig.CREER_UNE_NOUVELLE_CARTE_STILL = pygame.image.load("assets/buttons/menu_buttons/creer_une_nouvelle_carte_button/creer_une_nouvelle_carte_still.png").convert_alpha()
        MenuConfig.CREER_UNE_NOUVELLE_CARTE_CLICKED = pygame.image.load("assets/buttons/menu_buttons/creer_une_nouvelle_carte_button/creer_une_nouvelle_carte_clicked.png").convert_alpha()
        MenuConfig.CREER_UNE_NOUVELLE_CARTE_HOVERED = pygame.image.load("assets/buttons/menu_buttons/creer_une_nouvelle_carte_button/creer_une_nouvelle_carte_hovered.png").convert_alpha()

        #___/SELECTIONNER\___
        MenuConfig.SELECTIONNER_STILL = pygame.image.load("assets/buttons/menu_buttons/selectionner_button/selectionner_still.png").convert_alpha()
        MenuConfig.SELECTIONNER_CLICKED = pygame.image.load("assets/buttons/menu_buttons/selectionner_button/selectionner_clicked.png").convert_alpha()
        MenuConfig.SELECTIONNER_HOVERED = pygame.image.load("assets/buttons/menu_buttons/selectionner_button/selectionner_hovered.png").convert_alpha()

        #___/TEXT\___
        MUSIQUE_VOLUME_TEXTE = pygame.image.load("assets/texts/musique_volume.png").convert_alpha()
        MenuConfig.MUSIQUE_VOLUME_TEXTE = pygame.transform.scale(MUSIQUE_VOLUME_TEXTE, (MUSIQUE_VOLUME_TEXTE.get_width()*2,MUSIQUE_VOLUME_TEXTE.get_height()*2))
        SELECTIONNER_LA_CARTE = pygame.image.load("assets/texts/selectionner_la_carte.png").convert_alpha()
        MenuConfig.SELECTIONNER_LA_CARTE = pygame.transform.scale(SELECTIONNER_LA_CARTE, (SELECTIONNER_LA_CARTE.get_width()*1.5,SELECTIONNER_LA_CARTE.get_height()*1.5))



        #___/CURSOR\___
        MenuConfig.ARROW4 = pygame.transform.scale(pygame.image.load("assets/cursor/Light/Arrows/Arrow4.png").convert_alpha(), (24,24))


        

        