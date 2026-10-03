import pygame

from scripts.image import Images


class EditorConfig:


    
    def init():
        #___/EDITOR\____
        EditorConfig.SETTINGS_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,2,0)
        EditorConfig.VALID_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,5,1)
        EditorConfig.SAVE_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,3,1)
        EditorConfig.EXIT_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,4,1)
        EditorConfig.PEN_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,6,0)
        EditorConfig.ERASER_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,6,1)
        EditorConfig.SPAWN_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,6,2)


        EditorConfig.SETTINGS_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,2,3)
        EditorConfig.VALID_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,5,4)
        EditorConfig.SAVE_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,3,4)
        EditorConfig.EXIT_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,4,4)
        EditorConfig.PEN_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,6,3)
        EditorConfig.ERASER_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,6,4)
        EditorConfig.SPAWN_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,6,5)

        EditorConfig.NON_SAVED =pygame.image.load("assets/others/non_saved.png").convert_alpha()
        EditorConfig.SAVED =pygame.image.load("assets/others/saved.png").convert_alpha()

        #___/SETTINGS\____
        EditorConfig.ADD_1_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,0)
        EditorConfig.ADD_10_BUTTON_TEXTURE = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,0,2)
        EditorConfig.REMOVE_1_BUTTON_TEXTURE = pygame.transform.flip(Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,0),True,False)
        EditorConfig.REMOVE_10_BUTTON_TEXTURE = pygame.transform.flip(Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,0,2),True,False)
        
        EditorConfig.ADD_1_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,3)
        EditorConfig.ADD_10_BUTTON_TEXTURE_SELECTED = Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,0,5)
        EditorConfig.REMOVE_1_BUTTON_TEXTURE_SELECTED = pygame.transform.flip(Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,1,3),True,False)
        EditorConfig.REMOVE_10_BUTTON_TEXTURE_SELECTED = pygame.transform.flip(Images.extract_tile_from_tileset("assets/buttons/buttons.png",16,0,5),True,False)

        EditorConfig.MAP_WIDTH_TEXTURE = pygame.image.load("assets/buttons/map_width.png").convert_alpha()
        EditorConfig.MAP_HEIGHT_TEXTURE = pygame.image.load("assets/buttons/map_height.png").convert_alpha()
        EditorConfig.CLEAR_MAP = pygame.image.load("assets/buttons/clear_map.png").convert_alpha()
        EditorConfig.CLEAR_MAP_WARNING = pygame.image.load("assets/buttons/clear_map_warning.png").convert_alpha()

        
        #___/CURSORS\____
        EditorConfig.ARROW4 = pygame.transform.scale(pygame.image.load("assets/cursor/Light/Arrows/Arrow4.png").convert_alpha(), (24,24))
        EditorConfig.HAND2 = pygame.transform.scale(pygame.image.load("assets/cursor/Light/Hands/HAND2.png").convert_alpha(), (24,24))
        EditorConfig.HAND_DRAG2 = pygame.transform.scale(pygame.image.load("assets/cursor/Light/Hands/Hand_Drag2.png").convert_alpha(), (24,24))

        EditorConfig.ERASER = pygame.transform.scale(pygame.image.load("assets/cursor/Tools/eraser.png").convert_alpha(), (48,48))
        EditorConfig.PEN = pygame.transform.scale(pygame.image.load("assets/cursor/Tools/pen.png").convert_alpha(), (48,48))
        EditorConfig.SPAWN = pygame.transform.scale(pygame.image.load("assets/cursor/Tools/spawn.png").convert_alpha(), (48,48))


        