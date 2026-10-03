import pygame

from game_config import GameConfig
from settings import Settings

from scripts.player import Player
from scripts.text import Text
from scripts.map import Map
from scripts.timer import Timer

class GameState():

    def __init__(self, display,parent):
        
        #___/Initialisation du parent\___
        self.parent = parent


        #___/Initialisation de pygame\___
        self.display = display
        self.screen = pygame.Surface(Settings.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        self.map = Map()

        #___/Initialisation des états\___
        self.current_state = "playing"

        #___/Initialisation des sprites\___
        self.player = Player()

        #___/Initialisation des attributs\___
        self.scroll =  [0,0]
        
        #___/Initialisation du timer\___
        self.timer = Timer()
        self.finish_time = 0



 
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                # Démarre le timer si celui-ci n'est pas lancé et que le joueur presse une touche
                if not self.timer.is_timer_on and not Settings.PLAY_INTRO:
                    self.timer.start_timer()
                
                #Touche  Z, Q, S, D (Déplacement)
                if event.key == pygame.K_z:
                    self.player.is_moving_up = True
                if event.key == pygame.K_q:
                    self.player.is_moving_left = True
                if event.key == pygame.K_s:
                    self.player.is_moving_down = True
                if event.key == pygame.K_d:
                    self.player.is_moving_right = True
                
                #Touche ESPACE (Saut)
                if event.key == pygame.K_SPACE:
                    self.player.is_jumping = True
                
                #Touche Shift (Dash)
                if event.key == pygame.K_LSHIFT :
                    self.player.is_dashing = True
                
                #Touche ECHAP (Pause)
                if event.key == pygame.K_ESCAPE:  
                    self.parent.current_state = "menu"
                    self.timer.pause_timer()
                    self.player.is_moving_left = False
                    self.player.is_moving_right = False
                    self.player.is_jumping = False


    
            if event.type == pygame.KEYUP:
                #Touche  Z, Q, S, D (Déplacement)
                if event.key == pygame.K_q:
                    self.player.is_moving_left = False
                if event.key == pygame.K_d:
                    self.player.is_moving_right = False
                if event.key == pygame.K_z:
                    self.player.is_moving_up = False
                if event.key == pygame.K_s:
                    self.player.is_moving_down = False

                #Touche ESPACE (Saut)
                if event.key == pygame.K_SPACE:
                    self.player.is_jumping = False

                #Touche SHIFT GAUCHE (Dash)
                if event.key == pygame.K_LSHIFT :
                    self.player.is_dashing = False

    ################################
    ###        INIT PART         ###
    ################################


    def initialize_game(self,map_name):
        """
        Méthode qui permet d'initialiser une partie
        """
        self.load_map(map_name) #On charge la carte
        self.spawn_player() #On fait appaitre le joueur
        self.timer = Timer() #On initialize le timer
        self.set_scroll_to_spawn() #On met le scroll au spawn


    ##################################
    ###        UPDATE PART         ###
    ##################################


    def load_map(self, map_name):
        """
        Méthode qui permet de charger une carte
        """
        self.map.load(map_name)
        


    def spawn_player(self):
        """
        Méthode qui permet de faire spawn le joueur (Créer un nouveau joueur)
        """
        self.player = Player([self.map.spawn[0] * Settings.TILE_SIZE,self.map.spawn[1] * Settings.TILE_SIZE])
        


    def set_scroll_to_spawn(self):
        """
        Méthode qui permet de mettre la caméra au point de spawn
        """
        self.scroll = [self.map.spawn[0]* Settings.TILE_SIZE - Settings.SCREEN_RESOLUTION[0]//2, self.map.spawn[1]* Settings.TILE_SIZE- Settings.SCREEN_RESOLUTION[1]//2]


    
    def update_scroll(self,coord_x,coord_y):
        """
        Méthode qui met à jour le scroll de la caméra
        """
        screen_x_center = Settings.SCREEN_RESOLUTION[0]//2
        self.scroll[0] += ((coord_x - screen_x_center - self.scroll[0]) / GameConfig.SCROLLING_SMOOTHNESS) * int(GameConfig.X_SCROLLING)


        screen_y_center = Settings.SCREEN_RESOLUTION[1]//2
        self.scroll[1] += ((coord_y - screen_y_center - self.scroll[1]) / GameConfig.SCROLLING_SMOOTHNESS) * int(GameConfig.Y_SCROLLING)


    def handle_player_death(self,player):
        """
        Méthode qui gère la mort du joueur.
        """
        if self.is_player_dead(player):
            self.player.is_dead_animation = True
            self.player.animation_frame = 0
            
            #___/On joue l'animation de mort du joueur\___
            while self.player.is_dead_animation:
                self.player.death_animation()
                self.draw()
                self.render()
            
            #___/On déplace la caméra au point de départ\___
            spawn_x = self.map.spawn[0] * Settings.TILE_SIZE
            spawn_y = self.map.spawn[1] * Settings.TILE_SIZE
            scroll_goal = [spawn_x - Settings.SCREEN_RESOLUTION[0]//2,spawn_y - Settings.SCREEN_RESOLUTION[1]//2]

            while abs(scroll_goal[0] - self.scroll[0]) > 1 or (scroll_goal[1] - self.scroll[1]) > 1:
                self.update_scroll(spawn_x,spawn_y)
                self.draw()
                self.render()
                

            #Apparation du joueur
            self.spawn_player()


    #################################
    ###        STATE PART         ###
    #################################


    def is_player_finished(self,player):
        """
        Méthode qui vérifie si le joueur a fini le niveau (Dépasse la hauteur de la carte)
        """



        if player.position[1] <= 0:

            if self.current_state == "intro":
                Settings.change_intro_state()
                self.current_state = "playing"
                self.initialize_game("main")


            elif self.current_state == "playing":
                self.finish_time = self.timer.get_time()
                self.current_state = "finish"


    def is_player_dead(self,player):
        """
        Méthode qui permet de savoir si le joueur est mort
        """
        if (player.position[1] > self.map.size["height"] * Settings.TILE_SIZE + 100): #Si le joueur tombe 100 pixel en-dessous de la carte
            return True
        elif pygame.sprite.spritecollide(player, self.map.collision_dict["killable_tile_map"], False, pygame.sprite.collide_mask): #Si le joueur touche un pique
            return True
        return False

    

    ################################
    ###        DRAW PART         ###
    ################################

    def draw_filter(self):
        """
        Méthode permettant de simuler de l'ombre autour du joueur
        """
        size = 150 #Taille de la lumière
        power = 210 #Puissance de l'ombre de la pièce

        filtre = pygame.Surface((Settings.SCREEN_RESOLUTION[0],Settings.SCREEN_RESOLUTION[1]), pygame.SRCALPHA)
        filtre.fill((0, 0, 0, power))  # Dernier paramètre : alpha (0 = transparent, 255 = opaque)
        for x in range(size,0,-1):
            alpha = int(power * (x / size))
            pygame.draw.circle(filtre, (0, 0, 0, alpha),(self.player.rect.centerx - self.scroll[0], self.player.rect.centery - self.scroll[1]),x // 2)

        self.screen.blit(filtre,(0,0))
    

    def draw_timer(self):
        """
        Permet d'afficher le timer s'il est allumé
        """
        if self.timer.is_timer_on:
            center_x = Settings.SCREEN_RESOLUTION[0] // 2
            Text.draw_text(self.screen,str(self.timer.get_time()),15,(center_x,10),(255,255,255),center= True)


    def draw_fps(self):
        """
        Méthode qui permet d'afficher les fps
        """
        if Settings.SHOW_FPS: 
            fps = str(self.clock).split("=")[1][:-5]
            Text.draw_text(self.screen,fps,20,(0,0),(0,255,0))


    def draw(self):
        if self.current_state == "finish":
            self.draw_finish()
        else:
            self.draw_game()

        


    def draw_game(self):
        self.screen.fill(GameConfig.BACKGROUND_COLOR)
        self.map.draw_tile(self.screen, self.scroll, player=self.player)
        self.player.draw(self.screen, self.scroll)
        self.map.draw_gradient_borders(self.screen, self.scroll, (0, 0, 0))
        self.draw_fps()
        self.draw_timer()

    def draw_finish(self):
        self.screen.fill((0, 0, 0))
        center_x = Settings.SCREEN_RESOLUTION[0] // 2
        center_y = Settings.SCREEN_RESOLUTION[1] // 2
        self.draw_fps()
        Text.draw_text(self.screen, "Fini en :", 15, (center_x, center_y - 15), (255, 255, 255), center=True)
        Text.draw_text(self.screen, str(self.finish_time), 15, (center_x, center_y), (255, 255, 255), center=True)





    def render(self):
        """
        Méthode qui gère le rendu du display
        """
        self.display.blit(pygame.transform.scale(self.screen, Settings.DISPLAY_RESOLUTION), (0, 0))
        pygame.display.flip()
        self.clock.tick(Settings.GAME_FPS)

    
    def main_loop(self):
        if self.timer.is_timer_on:
            self.timer.resume_timer()
        
        if self.current_state == "finish":
            self.finish_loop()
        else:
            self.game_loop()
      


    def game_loop(self):
        self.events()
        self.update_scroll(self.player.position[0],self.player.position[1])
        self.player.update(self.map.collision_dict)
        self.handle_player_death(self.player)
        self.is_player_finished(self.player)
        self.draw()
        self.render()
    
    def finish_loop(self):
        self.events()
        self.draw()
        self.render()
