import pygame


from scripts.map import Map
from scripts.text import Text
from scripts.button import Button
from scripts.tile import Tile

from settings import Settings
from editor_config import EditorConfig
from scripts.image import Images





class EditorState():

    def __init__(self,display,parent):

        #___/Initialisation du parent\___
        self.parent = parent

        #___/Initialisation de pygame\___
        self.display = display
        self.screen = pygame.Surface(Settings.SCREEN_RESOLUTION,pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        
        #___/Initialisation de la carte\___
        self.map = Map()
        self.load_map("main")

        #___/Initialisation des boutons\___
        #Buttons de l'éditeur:

        self.editor_buttons = pygame.sprite.Group()
        self.editor_buttons.add(Button(0,0,lambda: self.apply_button_action("settings_button"),EditorConfig.SETTINGS_BUTTON_TEXTURE,EditorConfig.SETTINGS_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton paramètre
        self.editor_buttons.add(Button(0,24,lambda: self.apply_button_action("save_map_button"),EditorConfig.SAVE_BUTTON_TEXTURE,EditorConfig.SAVE_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton sauvegarder
        self.editor_buttons.add(Button((Settings.SCREEN_RESOLUTION[0]) -24,0,lambda: self.apply_button_action("exit_editor_button"),EditorConfig.EXIT_BUTTON_TEXTURE,EditorConfig.EXIT_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton quitter
        self.editor_buttons.add(Button((Settings.SCREEN_RESOLUTION[0]//2) +12,(Settings.SCREEN_RESOLUTION[1]) -24, lambda: self.apply_button_action("tool_to_spawn"),EditorConfig.SPAWN_BUTTON_TEXTURE,EditorConfig.SPAWN_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton spawn
        self.editor_buttons.add(Button((Settings.SCREEN_RESOLUTION[0]//2)-36,(Settings.SCREEN_RESOLUTION[1]) -24, lambda: self.apply_button_action("tool_to_pen"),EditorConfig.PEN_BUTTON_TEXTURE,EditorConfig.PEN_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton pen
        self.editor_buttons.add(Button((Settings.SCREEN_RESOLUTION[0]//2) -12 ,(Settings.SCREEN_RESOLUTION[1]) -24, lambda: self.apply_button_action("tool_to_eraser"),EditorConfig.ERASER_BUTTON_TEXTURE,EditorConfig.ERASER_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton eraser
        
        #Buttons du menu paramètre:

        self.offset = [(Settings.SCREEN_RESOLUTION[0]-120)//2,0]

        self.settings_buttons = pygame.sprite.Group()
        self.settings_buttons.add(Button(0,24,lambda: self.apply_button_action("save_map_size_button"),EditorConfig.SAVE_BUTTON_TEXTURE,EditorConfig.SAVE_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton save
        self.settings_buttons.add(Button(0,0,lambda: self.apply_button_action("valid_button"),EditorConfig.VALID_BUTTON_TEXTURE,EditorConfig.VALID_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton valider
        self.settings_buttons.add(Button(72 + self.offset[0],24 + self.offset[1],lambda: self.apply_button_action("add_width",1),EditorConfig.ADD_1_BUTTON_TEXTURE,EditorConfig.ADD_1_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton add 1 width
        self.settings_buttons.add(Button(96+ self.offset[0],24 + self.offset[1],lambda: self.apply_button_action("add_width",10),EditorConfig.ADD_10_BUTTON_TEXTURE,EditorConfig.ADD_10_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton add 10 width
        self.settings_buttons.add(Button(24+ self.offset[0],24 + self.offset[1],lambda: self.apply_button_action("add_width",-1),EditorConfig.REMOVE_1_BUTTON_TEXTURE,EditorConfig.REMOVE_1_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton remove 1 width
        self.settings_buttons.add(Button(0+ self.offset[0],24 + self.offset[1],lambda: self.apply_button_action("add_width",-10),EditorConfig.REMOVE_10_BUTTON_TEXTURE,EditorConfig.REMOVE_10_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton remove 10 width
        self.settings_buttons.add(Button(72+ self.offset[0],72 + self.offset[1],lambda: self.apply_button_action("add_height",1),EditorConfig.ADD_1_BUTTON_TEXTURE,EditorConfig.ADD_1_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton add 1 height
        self.settings_buttons.add(Button(96+ self.offset[0],72 + self.offset[1],lambda: self.apply_button_action("add_height",10),EditorConfig.ADD_10_BUTTON_TEXTURE,EditorConfig.ADD_10_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton add 10 height
        self.settings_buttons.add(Button(24+ self.offset[0],72 + self.offset[1],lambda: self.apply_button_action("add_height",-1),EditorConfig.REMOVE_1_BUTTON_TEXTURE,EditorConfig.REMOVE_1_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton remove 1 height  
        self.settings_buttons.add(Button(0+ self.offset[0],72 + self.offset[1],lambda: self.apply_button_action("add_height",-10),EditorConfig.REMOVE_10_BUTTON_TEXTURE,EditorConfig.REMOVE_10_BUTTON_TEXTURE_SELECTED,scale_factor=1.5))#Bouton remove 10 height
        self.settings_buttons.add(Button(self.offset[0],120 +self.offset[1],lambda: self.apply_button_action("clear_map"),image_still=EditorConfig.CLEAR_MAP, image_hovered=EditorConfig.CLEAR_MAP_WARNING))



        #___________________________
        
        #___/Initialisation des états\___
        self.current_editing_layer = list(self.map.data.keys())[len(self.map.data.keys())-1]
        self.current_tile = "tileset_0_0"
        self.current_page = "editing"
        self.current_editing_tool = "pen"
        
        #___/Initialisation des variables dynamiques\___
        self.map_width_counter = self.map.size["width"] 
        self.map_height_counter = self.map.size["height"]
        self.screen_scroll = [0,0]
        self.ctrl_pressed = False
        self.save_state = True
        self.mouse_pos = pygame.mouse.get_pos()


        #___/Test\___
        self.tileset_scale = 1
        self.tileset_window = pygame.Surface((Settings.DISPLAY_RESOLUTION[0]*(2/7),Settings.DISPLAY_RESOLUTION[1]*(2/7)),pygame.SRCALPHA) 
        self.tileset_window_scroll = [0,0]


        self.tile_dict = Images.extract_tiles("assets/maps/" + self.map.name + "/textures/tiles/tileset.png")
        self.tileset_image = pygame.image.load("assets/maps/" + self.map.name  + "/textures/tiles/tileset.png").convert_alpha()


        self.current_cursor = EditorConfig.ARROW4


    #############################
    ####     Events part     ####
    #############################


    def events(self):
        """
        Gére les évenements
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.current_page == "editing":
                #___/Vérifie le scroll de la souris\___
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button == 4: #Tile suivant (Molette haut)
                        self.apply_key_action("up")
                    elif event.button == 5: #Tile précédent (Molette bas)
                        self.apply_key_action("down")

                #___/Vérifie si une touche est pressée\___
                if event.type == pygame.KEYDOWN:           
                    
                    if event.key == pygame.K_s: #Sauvegarde la carte
                        if self.ctrl_pressed:
                            self.map.save()
                            self.save_state = True
                    elif event.key == pygame.K_a: #Couche (layer) suivante
                        self.apply_key_action("a")
                    elif event.key == pygame.K_e: #Couche (layer) précédent
                        self.apply_key_action("e")
                    elif event.key == pygame.K_1:  #Change l'outil à pen
                        self.current_editing_tool = "pen"
                    elif event.key == pygame.K_2: #Change l'outil à eraser
                        self.current_editing_tool = "eraser"
                    elif event.key == pygame.K_3: #Change l'outil à spawn
                        self.current_editing_tool = "spawn"
                    elif event.key == pygame.K_ESCAPE: #Quitte l'editeur
                        self.parent.current_state = "menu"
                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        self.ctrl_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL: 
                        self.ctrl_pressed = False

            elif self.current_page == "settings":
                #___/Vérifie si une touche est pressée\___
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_ESCAPE: #Quitte les options
                        self.current_page = "editing"
                    

    ############################
    ####     Utils part     ####
    ############################
    def mouse_to_tile_coordinates(self):
        """
        Méthode permettant d'obtenir la position d'une tile en fonction de l'emplacement de la souris sur le screen
        """
        return self.mouse_pos[0] // Settings.SCREEN_SCALE // Settings.TILE_SIZE,self.mouse_pos[1] // Settings.SCREEN_SCALE // Settings.TILE_SIZE


    def is_cursor_on_buttons(self,buttons):
        """
        Permet de savoir si le curseur est sur un groupe de boutons
        """
        return any(button.rect.collidepoint((self.mouse_pos[0]) // Settings.SCREEN_SCALE,self.mouse_pos[1] // Settings.SCREEN_SCALE) for button in buttons)

    def is_cursor_on_tileset_window(self):
        """
        Permet de savoir si le curseur est sur la fenêtre du tileset
        """
        width, height = self.tileset_window.get_width(), self.tileset_window.get_height()
        topleft_x, top_left_y = 0, Settings.DISPLAY_RESOLUTION[1] - height
        return  topleft_x <= self.mouse_pos[0] <= topleft_x + width and top_left_y <= self.mouse_pos[1] <=  top_left_y + height

    
    def is_cursor_on_editing_map(self):
        """
        Permet de savoir si le curseur est sur la carte
        """
        x,y = self.mouse_to_tile_coordinates()
        return 0 <= y + self.screen_scroll[1] // Settings.TILE_SIZE < self.map.size["height"]  and 0 <= x + self.screen_scroll[0] // Settings.TILE_SIZE < self.map.size["width"]


    def load_map(self,name):
        """
        Méthode qui permet de charger la carte
        """
        self.map.load(name)
        self.map_width_counter = self.map.size["width"]
        self.map_height_counter = self.map.size["height"]

    
    
    #############################
    ####     Update part     ####
    #############################
    
    def update_cursor(self):
        clicked = pygame.mouse.get_pressed()
        if self.current_page == "editing":
            if self.is_cursor_on_buttons(self.editor_buttons):
                self.current_cursor = EditorConfig.HAND2
            elif self.is_cursor_on_tileset_window() and clicked[1]:
                self.current_cursor = EditorConfig.HAND_DRAG2
            elif self.is_cursor_on_tileset_window() :
                self.current_cursor = EditorConfig.ARROW4
            elif self.current_editing_tool == "pen":
                self.current_cursor = EditorConfig.PEN
            elif self.current_editing_tool == "spawn":
                self.current_cursor = EditorConfig.SPAWN
            elif self.current_editing_tool == "eraser":
                self.current_cursor = EditorConfig.ERASER
            else:
                self.current_cursor = EditorConfig.ARROW4
        

        elif self.current_page == "settings":
            if self.is_cursor_on_buttons(self.settings_buttons):
                self.current_cursor = EditorConfig.HAND2
            else:
                self.current_cursor = EditorConfig.ARROW4
        
        
        
        


    def update_mouse_pos(self):
        """
        Permet de mettre à jour la position de la souris
        """
        self.mouse_pos = pygame.mouse.get_pos()

    def update_scroll(self):
        """
        Méthode mettant à jour les différents scrolls
        """
        #___/SCROLL DE LA MAP\___
        if not self.ctrl_pressed:
            keys = pygame.key.get_pressed()
            tile_size = Settings.TILE_SIZE
            multiplier = 3 if keys[pygame.K_LSHIFT] else 1

            if keys[pygame.K_z]:
                self.screen_scroll[1] -= tile_size * multiplier
            if keys[pygame.K_s]:
                self.screen_scroll[1] += tile_size * multiplier
            if keys[pygame.K_d]:
                self.screen_scroll[0] += tile_size * multiplier
            if keys[pygame.K_q]:
                self.screen_scroll[0] -= tile_size * multiplier
        


        # ___/SCROLL DE L'EDITEUR\___
        if self.is_cursor_on_tileset_window():
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[1]:
                if not hasattr(self.update_scroll, 'prev_pos'):
                    EditorState.update_scroll.prev_pos = self.mouse_pos

                current_pos = self.mouse_pos
                d_pos = [current_pos[0] - EditorState.update_scroll.prev_pos[0], current_pos[1] - EditorState.update_scroll.prev_pos[1]]

                # Update the scroll based on the cursor movement
                self.tileset_window_scroll[0] -= d_pos[0]
                self.tileset_window_scroll[1] -= d_pos[1]

                EditorState.update_scroll.prev_pos = current_pos
            
            else:
                if hasattr(EditorState.update_scroll, 'prev_pos'):
                    del EditorState.update_scroll.prev_pos

       

            

    ############################
    ####     Action part    ####
    ############################

    def apply_button_action(self,bouton,value=None):
        """
        Fonction qui gère les différentes actions des boutons
        """
        if bouton == "settings_button":
            self.current_page = "settings"
        
        elif bouton == "valid_button":
            if self.current_page == "settings":
                self.map_width_counter = self.map.size["width"] 
                self.map_height_counter = self.map.size["height"] 
                self.current_page = "editing"
        
        elif bouton == "exit_editor_button":
            self.parent.current_state = "menu"
        
        elif bouton == "save_map_button":
            self.map.save()
            self.save_state = True
        
        elif bouton == "save_map_size_button":
            self.map.change_size(self.map_width_counter,self.map_height_counter)
            self.save_state = False
        
        elif bouton == "add_width":
            if value > 0:
                self.map_width_counter = min(1000, self.map_width_counter + value)
            else:
                self.map_width_counter = max(1, self.map_width_counter + value)
        
        elif bouton == "add_height":
            if value > 0:
                self.map_height_counter = min(1000, self.map_height_counter + value)
            else:
                self.map_height_counter = max(1, self.map_height_counter + value)

        elif bouton == "tool_to_spawn":
            self.current_editing_tool = "spawn"

        elif bouton == "tool_to_pen":
            self.current_editing_tool = "pen"

        elif bouton == "tool_to_eraser":
            self.current_editing_tool = "eraser"

        elif bouton == "clear_map":
            self.map.clear()
            self.save_state = False


    def apply_tool_action(self):
        """
        Méthode qui effectue l'action de l'outil (pen,eraser,spawn) en fonction des inputs de l'utilisateur
        """
        
        if not self.is_cursor_on_buttons(self.editor_buttons) and not self.is_cursor_on_tileset_window():
            mouse = pygame.mouse.get_pressed()
            x,y = self.mouse_to_tile_coordinates()
            if self.is_cursor_on_editing_map():
                position = [int(x) + self.screen_scroll[0]// Settings.TILE_SIZE,int(y) + self.screen_scroll[1]// Settings.TILE_SIZE]
                if mouse[0]:
                    if self.current_editing_tool == "pen":
                        tile = Tile(self.current_tile,int(x)*Settings.TILE_SIZE + self.screen_scroll[0],int(y)*Settings.TILE_SIZE + self.screen_scroll[1],self.tile_dict[self.current_tile])
                        self.map.change_tile(self.current_editing_layer,position, tile)  
                    if self.current_editing_tool == "eraser":
                        self.map.change_tile(self.current_editing_layer,position,"-1")
                    if self.current_editing_tool == "spawn":
                        self.map.change_spawn(position)
                    self.save_state = False  
                elif mouse[2]:
                    if self.current_editing_tool == "eraser" or self.current_editing_tool == "pen":
                        self.map.change_tile(self.current_editing_layer,position,"-1")
                    self.save_state = False
                elif mouse[1]:
                    if self.current_editing_tool == "pen":
                        if self.map.data[self.current_editing_layer][position[1]][position[0]] != "-1":
                            self.current_tile = self.map.data[self.current_editing_layer][position[1]][position[0]].name

        



    def apply_key_action(self,key):
        """
        Méthode qui permet de gérer les actions des différentes touches préssées
        """
        if self.is_cursor_on_tileset_window():
            if key == "down":
                self.tileset_scale = max(1,self.tileset_scale-1)
            if key == "up":
                self.tileset_scale = min(3,self.tileset_scale + 1)
        if key == "a":
            current_layer_indice = list(self.map.layers).index(self.current_editing_layer)
            next_layer_indice = min(current_layer_indice + 1 , len(list(self.map.data.keys()))-1)
            self.current_editing_layer = list(self.map.layers)[next_layer_indice]
        if key == "e":
            current_layer_indice = list(self.map.layers).index(self.current_editing_layer)
            next_layer_indice = max(current_layer_indice - 1 , 0)
            self.current_editing_layer = list(self.map.layers)[next_layer_indice]
            

    ##########################
    ####     Draw part    ####
    ##########################
    
    #____/TILESET WINDOW\___

    def draw_tilset_border(self):
        """
        Permet de dessiner les bords de la fenêtre du tileset
        """
        width,height  = self.tileset_window.get_width(),self.tileset_window.get_height()
        pygame.draw.rect(self.display, (255, 255, 255), (0, Settings.DISPLAY_RESOLUTION[1] - height -3 , width + 3, height + 3),3)

    def draw_tileset(self):
        """
        Permet de dessiner les tiles sur la fenêtre du tileset
        """
        for tile in self.tile_dict:
            x = (int(tile.split("_")[1]) )*Settings.TILE_SIZE*self.tileset_scale - int(self.tileset_window_scroll[0])
            y = (int(tile.split("_")[2]) )*Settings.TILE_SIZE*self.tileset_scale - int(self.tileset_window_scroll[1])
            width, height = Settings.TILE_SIZE * self.tileset_scale , Settings.TILE_SIZE * self.tileset_scale
            self.tileset_window.blit(pygame.transform.scale(self.tile_dict[tile],(width, height)),(x,y))
        
    def draw_selected_tile(self):
        """
        Permet de dessiner les tiles sur la fenêtre du tileset
        """
        x = (int(self.current_tile.split("_")[1]) )*Settings.TILE_SIZE*self.tileset_scale - int(self.tileset_window_scroll[0])
        y = (int(self.current_tile.split("_")[2]) )*Settings.TILE_SIZE*self.tileset_scale - int(self.tileset_window_scroll[1])
        selection = pygame.Surface((Settings.TILE_SIZE * self.tileset_scale,Settings.TILE_SIZE * self.tileset_scale), pygame.SRCALPHA)
        selection.fill((0,128,255,96))
        self.tileset_window.blit(selection, (x, y))

    def draw_tile_selection_preview(self):
        """
        Permet de dessiner quelle tile sera selectionné et met à jour le tile courant si on appuie sur clique droit
        """
        clicked = pygame.mouse.get_pressed()[0]
        if self.is_cursor_on_tileset_window():
            tile_x = self.mouse_pos[0] //(Settings.TILE_SIZE * self.tileset_scale)
            tile_y = (self.mouse_pos[1]- (Settings.DISPLAY_RESOLUTION[1] - self.tileset_window.get_height()))//(Settings.TILE_SIZE * self.tileset_scale)
            selection = pygame.Surface((Settings.TILE_SIZE * self.tileset_scale,Settings.TILE_SIZE * self.tileset_scale), pygame.SRCALPHA)
            selection.fill((255,255,255,96))
            self.tileset_window.blit(selection, (tile_x*(Settings.TILE_SIZE * self.tileset_scale) +int(self.tileset_window_scroll[0])  ,  tile_y*(Settings.TILE_SIZE * self.tileset_scale) - int(self.tileset_window_scroll[1])))
            
            
            if clicked and f"tileset_{tile_x + int(self.tileset_window_scroll[0])}_{tile_y + int(self.tileset_window_scroll[1])}" in self.tile_dict:
                self.current_tile = f"tileset_{tile_x + int(self.tileset_window_scroll[0])}_{tile_y + int(self.tileset_window_scroll[1])}"
    

    def draw_tile_selection_preview(self):
        """
        Permet de dessiner quelle tile sera selectionné et met à jour le tile courant si on appuie sur clique droit
        """
        clicked = pygame.mouse.get_pressed()[0]
        if self.is_cursor_on_tileset_window():
            relative_mouse_x = self.mouse_pos[0]
            relative_mouse_y = self.mouse_pos[1] - (Settings.DISPLAY_RESOLUTION[1] - self.tileset_window.get_height())

            tile_x = (relative_mouse_x + int(self.tileset_window_scroll[0])) // (Settings.TILE_SIZE * self.tileset_scale)
            tile_y = (relative_mouse_y + int(self.tileset_window_scroll[1])) // (Settings.TILE_SIZE * self.tileset_scale)
            
            selection = pygame.Surface((Settings.TILE_SIZE * self.tileset_scale, Settings.TILE_SIZE * self.tileset_scale), pygame.SRCALPHA)
            selection.fill((255, 255, 255, 96))

            self.tileset_window.blit(selection, (tile_x * (Settings.TILE_SIZE * self.tileset_scale) - int(self.tileset_window_scroll[0]), tile_y * (Settings.TILE_SIZE * self.tileset_scale) - int(self.tileset_window_scroll[1])))


            if clicked and f"tileset_{tile_x}_{tile_y}" in self.tile_dict:
                self.current_tile = f"tileset_{tile_x}_{tile_y}"


    #__________/\_________


    #____/OTHER DRAW\_____

    def draw_cursor(self):
        self.display.blit(self.current_cursor, self.mouse_pos)



    def draw_save_state(self):
        """
        Permet de dessiner l'icone si la carte a été sauvegardée ou non.
        """
        if self.save_state:
            self.screen.blit(EditorConfig.SAVED, (Settings.SCREEN_RESOLUTION[0] -16 , Settings.SCREEN_RESOLUTION[1] -16 ))
        else:
            self.screen.blit(EditorConfig.NON_SAVED, (Settings.SCREEN_RESOLUTION[0] -16 , Settings.SCREEN_RESOLUTION[1] -16 ))
    


    def draw_spawn_point(self):
        """
        Méthode qui permet de dessiner le point de spawn
        """
        pygame.draw.rect(self.screen, (0, 255, 0), (self.map.spawn[0] * 16  - self.screen_scroll[0] ,self.map.spawn[1] * 16 - self.screen_scroll[1], 16, 16))

    
    def draw_tool_preview(self):
        """
        Méthode qui permet de dessiner l'aperçu du placement des tiles en fonction de l'outil en cours
        """
        if self.is_cursor_on_editing_map():
            x,y = self.mouse_to_tile_coordinates()
            if self.current_editing_tool == "spawn":
                temp_surface = pygame.Surface((Settings.TILE_SIZE, Settings.TILE_SIZE), pygame.SRCALPHA)
                temp_surface.fill((0,255,0,128))
                self.screen.blit(temp_surface, (x * Settings.TILE_SIZE, y * Settings.TILE_SIZE))
            if self.current_editing_tool == "pen":
                temp_image = self.tile_dict[self.current_tile].copy()
                temp_image.set_alpha(128)
                self.screen.blit(temp_image, (x * Settings.TILE_SIZE, y * Settings.TILE_SIZE))
            if self.current_editing_tool == "eraser":
                temp_surface = pygame.Surface((Settings.TILE_SIZE, Settings.TILE_SIZE), pygame.SRCALPHA)
                temp_surface.fill((200,200,200,128))
                self.screen.blit(temp_surface, (x * Settings.TILE_SIZE, y * Settings.TILE_SIZE))


    #__________/\_________

    def draw(self):
        """
        Méthode qui dessine tous les éléments sur le screen et display
        """
        #___/DRAW SCREEN\___
        if self.current_page == "editing":
            self.screen.fill((0,0,0))      
            self.map.draw_tile(self.screen,self.screen_scroll, map_layer= self.current_editing_layer)
            self.map.draw_borders(self.screen,self.screen_scroll) 
            self.draw_save_state()
            self.draw_spawn_point()
            self.draw_tool_preview()
            Text.draw_text(self.screen,self.current_editing_layer,16,(25,0),(255,255,255))
            self.editor_buttons.draw(self.screen)
        
        elif self.current_page == "settings":
            self.screen.fill((0,0,0)) 
            self.screen.blit(EditorConfig.MAP_WIDTH_TEXTURE,(self.offset[0],self.offset[1]))
            self.screen.blit(EditorConfig.MAP_HEIGHT_TEXTURE,(self.offset[0],48 +self.offset[1]))
            Text.draw_text(self.screen,str(self.map_width_counter),16,(48 + self.offset[0],32 + self.offset[1]),(255,255,255))
            Text.draw_text(self.screen,str(self.map_height_counter),16,(48 + self.offset[0],80 + self.offset[1]),(255,255,255))
            self.settings_buttons.draw(self.screen)
        
        self.display.blit(pygame.transform.scale(self.screen, Settings.DISPLAY_RESOLUTION), (0,0))
        
        
        
        #___/DRAW DISPLAY\___
        if self.current_page == "editing":
            self.tileset_window.fill((0,0,0))
            self.draw_tileset()
            self.draw_selected_tile()
            self.draw_tile_selection_preview()
            self.draw_tilset_border()
            self.display.blit(self.tileset_window, (0,(Settings.DISPLAY_RESOLUTION[1] - self.tileset_window.get_height())))
        elif self.current_page == "settings":
            pass



        self.draw_cursor()
        
    
    
    def render(self):
        """
        Méthode qui gère le rendu du display
        """
        pygame.display.flip()
        self.clock.tick(Settings.GAME_FPS)

    ##########################


    ##########################
    ####     Loop part    ####
    ##########################

    def main_loop(self):
        if self.current_page == "editing":
            self.editing_loop()
        elif self.current_page == "settings":
            self.settings_loop()
        else:
            self.editing_loop()


    def editing_loop(self):
        self.update_scroll()
        self.editor_buttons.update()
        self.apply_tool_action()
        self.update_mouse_pos()
        self.update_cursor()
        self.events()
        self.draw()
        self.render()
        

    def settings_loop(self):
        self.settings_buttons.update()
        self.update_mouse_pos()
        self.update_cursor()
        self.events()
        self.draw()
        self.render()

    ##########################
