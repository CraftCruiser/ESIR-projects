import pygame
import copy

from game_config import GameConfig
from settings import Settings

from scripts.image import Images

class Player(pygame.sprite.Sprite):

    def __init__(self,position = [0,0]):
        super().__init__()

        
        #Variable
        self.position = position
        self.velocity = [0,0]
        self.air_time = 0
        self.dash_time = 0
        self.dash_count = 0
        self.dash_max = 1
        self.collision_direction = {"left": False, "right": False, "top": False, "bottom": False}

        #Etats
        self.is_jumping = False
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_moving_down = False
        self.is_moving_up = False
        self.player_rotation = 0
        self.is_dashing = False
        self.is_dead_animation = False
        self.is_on_ladder = False
        #Rect et textures
        
        
        self.current_animation = "idle_right"
        self.animation_frame = 0
        self.image_offset = [12, 10]
        self.animations = Images.extract_animations_from_sheet("assets/entities/player/player.png",{ 
            "idle_right" : [0,4,None],
            "idle_left" : [0,4,"horizontal"],
            "jumping_right" : [1,1,None],
            "jumping_left" : [3,1,None],
            "moving_right" : [1,8,None],
            "moving_left" : [3,8,None],
            "death_left" : [12,10,"horizontal"],
            "death_right" : [12,10,None],
            "ladder" : [6,8,None],
            "ladder_idle" : [6,1,None]
        },Settings.TILE_SIZE*2,Settings.TILE_SIZE*2)

        
        self.image = self.animations[self.current_animation][0]
        
        self.rect = pygame.Rect(position[0],position[1],10,14)
        self.mask = pygame.mask.Mask((10, 14), fill=True)
        


    def collision_sprites(self, sprites_group):
        """
        Méthode qui teste les collisions
        """
        collisions = pygame.sprite.spritecollide(self, sprites_group, False)
        return collisions


    def draw(self,surface,scroll):
        """
        Méthode qui dessine le personange sur une surface en fonction d'un scroll
        """
        surface.blit(self.image, (self.position[0] - 11 - scroll[0],self.position[1] - 10 - scroll[1]))


    def is_on_ladder_func(self,sprite_group):
        """
        Méthode qui vérifie si le joueur ce situe sur une échelle et change l'attribut
        """
        if len(self.collision_sprites(sprite_group)) != 0:
            if self.is_moving_up or (self.is_moving_down and not self.collision_direction["bottom"]):
                self.is_on_ladder = True
        else:
            self.is_on_ladder = False


    def death_animation(self):
        """
        Méthode permemttant de lancer l'animation de mort
        """
        self.current_animation = ["death_right",None,"death_left"][self.player_rotation//90]
        self.animation_frame += 0.25
        self.image = self.animations[self.current_animation][int(self.animation_frame)]
        if self.animation_frame >= len(self.animations[self.current_animation]) -1:
            self.animation_frame = 0
            self.is_dead_animation = False


    def animation(self):
        """
        Méthode qui gère les animations en fonction du mouvement du joueur.
        """
        # Détermine l'animation principale
        if self.air_time > 5:
            # Animation de saut selon la rotation du joueur
            self.current_animation = ["jumping_right", None, "jumping_left"][self.player_rotation // 90]
        
        elif self.is_on_ladder:
            # Gestion des animations sur une échelle
            if self.is_moving_up or self.is_moving_down or self.is_moving_left or self.is_moving_right:
                self.current_animation = "ladder"
            else:
                self.current_animation = "ladder_idle"
        
        elif self.is_moving_right:
            self.current_animation = "moving_right"
        elif self.is_moving_left:
            self.current_animation = "moving_left"
        
        else:
            # Animation au repos selon la rotation du joueur
            self.current_animation = ["idle_right", None, "idle_left"][self.player_rotation // 90]

        # Gestion des frames de l'animation
        self.animation_frame += 0.15
        if self.animation_frame >= len(self.animations[self.current_animation]):
            self.animation_frame = 0

        # Mise à jour de l'image uniquement si nécessaire
        current_image = self.animations[self.current_animation][int(self.animation_frame)]
        if self.image != current_image:
            self.image = current_image



    def update(self,collision_dict):
        """
        Fonction qui met à jour les états du joueur
        """
        #___/ANIMATION\___
        if self.is_moving_right:
            self.player_rotation = 0
            self.current_animation = "moving_right"
        elif self.is_moving_left:
            self.player_rotation = 180
            self.current_animation = "moving_left"
        self.animation()
        
        #___/STATE VERIFICATION\___
        self.is_on_ladder_func(collision_dict["ladder_tile_map"])

        



        

        #___/MOUVEMENT\___
        if not self.is_on_ladder:

            #__JUMP__
            if self.is_jumping and self.air_time < 7 and self.velocity[1] > 0 :
                self.velocity[1] -= GameConfig.JUMP_Y_VELOCITY

            #__DASH__
            if  self.is_dashing and self.dash_count < self.dash_max and self.air_time > 6 :
                self.dash_time = 60
                self.velocity[1] = 0
                self.dash_count += 1
                if self.is_moving_left :
                    self.velocity[0] = -GameConfig.DASH_VELOCITY
                if self.is_moving_right :
                    self.velocity[0] = GameConfig.DASH_VELOCITY
            else :
                self.dash_time = max(0,self.dash_time-1)
                if self.air_time < 7 and self.dash_time == 0 :
                    self.dash_count = 0
                self.dash_time = max(0,self.dash_time-1)
                
            
            #__MOUV_DEPART_ARRETE__
            if self.is_moving_left and abs(self.velocity[0]) == 0 :
                self.velocity[0] += -GameConfig.WALKING_A_X
            if self.is_moving_right and abs(self.velocity[0]) == 0 :
                self.velocity[0] += GameConfig.WALKING_A_X 
            
            #__MOUV_SUR_SOL__
            if self.air_time < 7  :
                if not self.is_moving_right and not self.is_moving_left :
                    if abs(self.velocity[0]) > GameConfig.MIN_VELOCITY :
                        self.velocity[0] += - (GameConfig.FRICTION_GX)*self.velocity[0]
                    else :
                        self.velocity[0] = 0
                if self.is_moving_left and self.velocity[0] != 0 :
                    self.velocity[0] += - GameConfig.WALKING_A_X - (GameConfig.FRICTION_GX)*self.velocity[0]
                if self.is_moving_right and self.velocity[0] != 0 :
                    self.velocity[0] += GameConfig.WALKING_A_X - (GameConfig.FRICTION_GX)*self.velocity[0]

            #__MOUV_DANS_AIR__
            if self.air_time > 6 :
                    if not self.is_moving_right and not self.is_moving_left :
                        if not abs(self.velocity[0]) > GameConfig.MAX_VELOCITY :
                            self.velocity [0] += - (GameConfig.FRICTION_AX)*self.velocity[0]
                        else :
                              self.velocity [0] += - (GameConfig.FRICTION_AX)*self.velocity[0]
                    if self.is_moving_left and self.velocity[0] != 0 :
                            self.velocity[0] += - GameConfig.WALKING_A_X - (GameConfig.FRICTION_GX)*self.velocity[0]
                    if self.is_moving_right and self.velocity[0] != 0 :
                            self.velocity[0] += GameConfig.WALKING_A_X - (GameConfig.FRICTION_GX)*self.velocity[0]
                

                
            if self.collision_direction["bottom"] :
                self.air_time = 0
                self.velocity[1] = 0
            if not self.collision_direction["bottom"] :
                self.air_time += 1
                self.velocity[1] +=  GameConfig.GRAVITY_A_Y - GameConfig.FRICTION_Y*self.velocity[1]
            if self.collision_direction["top"] :     
                self.velocity[1] = 0
            if self.collision_direction["right"] or self.collision_direction["left"] :
                self.velocity[0] = 0     
       




       #___/LADDER_MOUVEMENT\___
        if self.is_on_ladder:
            self.air_time = 0
            self.velocity[0] *= 0.2  # Preserve some horizontal momentum
            self.velocity[1] = 0
            if self.is_moving_left:
                self.velocity[0] -= 0.5
            if self.is_moving_right:
                self.velocity[0] += 0.5
            if self.is_moving_up:
                self.velocity[1] -= 1
            if self.is_moving_down:
                self.velocity[1] += 1
            
            if self.is_jumping and self.air_time < 4:
                self.velocity[1] = - 1
               # jump_velocity = self.velocity[0]
               # self.velocity = [jump_velocity, - GameConfig.JUMP_Y_VELOCITY]
                self.is_on_ladder = False


        #___/COLLISION\___
        
        

        self.rect.y += self.velocity[1] 
        collisions = self.collision_sprites(collision_dict["collision_tile_map"])
        if len(collisions) == 0:
            self.collision_direction["top"] = False
            self.collision_direction["bottom"] = False
        for collision in collisions:
            if self.velocity[1] > 0:
                self.collision_direction["bottom"] = True
                self.rect.bottom = collision.rect.top     
            if self.velocity[1] < 0:
                self.collision_direction["top"] = True
                self.rect.top = collision.rect.bottom 

        self.position = [self.rect.x, self.rect.y]
                   
        self.rect.x += self.velocity[0] 
        collisions = self.collision_sprites(collision_dict["collision_tile_map"])
        if len(collisions) == 0:
            self.collision_direction["right"] = False
            self.collision_direction["left"] = False
        for collision in collisions:
            if self.velocity[0] > 0:
                self.collision_direction["right"] = True
                self.rect.right = collision.rect.left
            if self.velocity[0] < 0:
                self.collision_direction["left"] = True
                self.rect.left = collision.rect.right



        #___/COLLISION ACTION\___
         # Gère l'air time et la velocité si le joueur touche le sol
        if self.collision_direction["bottom"]:
            self.air_time = 0
            self.is_on_ladder = False
            self.velocity[1] = 0
        else:
            self.air_time += 1

        # Gère la self.velocity si le joueur touche le plafond
        if self.collision_direction["top"]:
            self.velocity[1] = 0




        

    
        self.position = [self.rect.x, self.rect.y]  
        





