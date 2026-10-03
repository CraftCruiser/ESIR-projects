import os
import pygame
import shutil
from datetime import datetime

from scripts.file import File
from scripts.image import Images
from scripts.tile import Tile
from settings import Settings

class Map():



    def __init__(self):
        self.name = ""  # Nom de la carte
        self.data = {}  # Dictionnaire contenant les couches de la carte 
        self.spawn = [] # Point de spawn du joueur
        self.size = {} # Taille de la carte
        
        # Dictionnaire contenant les sprites des tiles proches du joueurs de chaques couches
        self.collision_dict = {"collision_tile_map" : pygame.sprite.Group(), "killable_tile_map" : pygame.sprite.Group(), "background_tile_map" : pygame.sprite.Group(), "ladder_tile_map" : pygame.sprite.Group()} 
        self.layers = ["ladder_tile_map","background_tile_map","killable_tile_map","collision_tile_map"] #Le nom de chaque couche 




    def load(self,name):
        """
        Méthode qui charge la carte avec le config
        """
        
        self.name = name

        map_path = "assets/maps/" + name

        #___/Extraire le fichier config\___
        config = File.import_json(map_path + "/config.json")
        for setting,value in config.items():
            if setting == "width":
                self.size["width"] = int(value)
            
            if setting == "height":
                self.size["height"]= int(value)
            
            if setting == "spawn":
                self.spawn = [int(value[0]),int(value[1])]
        
        #___/Extraire les couches\___
        tile_dict = Images.extract_tiles(map_path + "/textures/tiles/tileset.png")
        for layer in self.layers:
            layer_data = File.import_csv(map_path + "/" + layer + ".csv")
            for y in range(len(layer_data)):
                for x in range(len(layer_data[0])):
                    if layer_data[y][x] != "-1":
                        if layer == "ladder_tile_map":
                            layer_data[y][x] = Tile(layer_data[y][x],int(x)*Settings.TILE_SIZE,int(y)*Settings.TILE_SIZE,tile_dict[layer_data[y][x]] , ladder = True)
                        else:
                            layer_data[y][x] = Tile(layer_data[y][x],int(x)*Settings.TILE_SIZE,int(y)*Settings.TILE_SIZE,tile_dict[layer_data[y][x]])
            self.data[layer] = layer_data

    


    
    def save(self):
        """
        Méthode qui permet de sauvegarder la carte
        """
    
        map_path = "assets/maps/" + self.name
    
        #___/Sauvegarde du fichier config\___
        config_data = {
            "width": self.size["width"],
            "height": self.size["height"],
            "spawn": self.spawn
        }
        File.export_json(map_path + "/config.json",config_data)

        #___/Sauvegarde des couches\___
        for layer in self.layers:
            layer_data = [["-1" for _ in range(len(self.data[layer][0]))] for _ in range(len(self.data[layer]))]
            for y in range(len(self.data[layer])):
                for x in range(len(self.data[layer][0])):
                    if self.data[layer][y][x] != "-1":
                        layer_data[y][x] = self.data[layer][y][x].name
                File.export_csv(map_path + "/" + layer + ".csv" , layer_data)


    def create(self,name,width,height,spawn=[0,0]):
        """
        Méthode qui permet de créer une map vierge 
        """
        map_path = "assets/maps/" + name
        
        if not os.path.exists(map_path):
            #___/Création des dossiers\___
            os.mkdir(map_path)
            os.mkdir(map_path + "/textures")
            os.mkdir(map_path + "/textures/tiles")

            #__/Copie du tileset\___
            tileset = "assets/tiles/tileset.png"
            shutil.copy(tileset, map_path + "/textures/tiles")

            #___/Création du fichier config\___
            config_data = {
                "width": width,
                "height": height,
                "spawn": spawn
                }
            File.export_json(map_path + "/config.json", config_data)


            #___/Création des fichiers csv\___
            empty_map = [[-1 for _ in range(width)] for _ in range(height)]
            for layer in self.layers:
                File.export_csv(map_path + "/" + layer + ".csv", empty_map)

        else:
            print(f"La carte {name} existe déjà")

    def delete(self):
        """
        Méthode qui permet de supprimer une carte, y compris tous ses fichiers associés.
        """
        map_path = "assets/maps/" + self.name
        
        if os.path.exists(map_path):
            try:
                shutil.rmtree(map_path) 
                print(f"La carte {self.name} a été supprimée avec succès.")
            except Exception as e:
                print(f"Erreur lors de la suppression de la carte {self.name}: {e}")
        else:
            print(f"La carte {self.name} n'existe pas.")


    def change_size(self, width, height):
        """
        Méthode qui met à jour la taille de la carte (Peut retirer des tiles)
        """
        # Mise à jour de la largeur
        for layer in self.layers:
            for y in range(len(self.data[layer])): 
                # Ajuste la largeur de chaque ligne
                if self.size["width"] < width:  # Augmenter la largeur
                    self.data[layer][y].extend(["-1"] * (width - self.size["width"]))
                elif self.size["width"] > width:  # Réduire la largeur
                    self.data[layer][y] = self.data[layer][y][:width]

            # Ajuste la hauteur de la couche
            if self.size["height"] < height:  # Ajouter des lignes
                for _ in range(height - self.size["height"]):
                    self.data[layer].append(["-1"] * width)
            elif self.size["height"] > height:  # Supprimer des lignes
                self.data[layer] = self.data[layer][:height]

        # Mise à jour des dimensions
        self.size["width"] = width
        self.size["height"] = height

        # Ajuste le spawn si nécessaire
        if self.spawn[0] >= width or self.spawn[1] >= height:
            self.spawn = [0, 0]

            
    def clear(self):
        """
        Méthode qui permet de retirer tous les tiles de toutes les couches
        """
        for layer in self.layers:
            self.data[layer] = [["-1" for _ in range(self.size["width"])] for _ in range(self.size["height"])]   



    def change_tile(self,layer,position,tile):
        """
        Méthode qui change le tile d'une couche en fonction d'une position
        """
        self.data[layer][position[1]][position[0]] = tile
        

    def change_spawn(self,position):
        """
        Méthode qui change le spawn
        """
        self.spawn = position

    def draw_gradient_borders(self, screen, scroll, color):
        """
        Méthode combinée pour dessiner les gradients sur les bords (gauche, droite, bas) et les bords hors map.
        """
        screen_height = Settings.SCREEN_RESOLUTION[1]
        screen_width = Settings.SCREEN_RESOLUTION[0]
        map_width = self.size["width"] * Settings.TILE_SIZE
        map_height = self.size["height"] * Settings.TILE_SIZE

        # Dessin des bords hors map
        top_border = pygame.Rect(scroll[0], scroll[1], screen_width, -scroll[1])
        left_border = pygame.Rect(scroll[0], scroll[1], -scroll[0], screen_height)
        right_border = pygame.Rect(map_width, scroll[1], screen_width + scroll[0], screen_height)
        bottom_border = pygame.Rect(scroll[0], map_height, screen_width, screen_height + scroll[1] - map_height + 10)

        # Dessiner les bordures
        pygame.draw.rect(screen, (255,255,255), (top_border.x - scroll[0], top_border.y - scroll[1], top_border.width, top_border.height))
        pygame.draw.rect(screen, color, (left_border.x - scroll[0], left_border.y - scroll[1], left_border.width, left_border.height))
        pygame.draw.rect(screen, color, (right_border.x - scroll[0], right_border.y - scroll[1], right_border.width, right_border.height))
        pygame.draw.rect(screen, color, (bottom_border.x - scroll[0], bottom_border.y - scroll[1], bottom_border.width, bottom_border.height))


        # Dessin des gradients
        gradient_size = 3 * Settings.TILE_SIZE

        # Gradient en haut
        top_gradient = pygame.Surface((map_width, gradient_size), pygame.SRCALPHA)
        for y in range(gradient_size):
            alpha = int((y / gradient_size) * 255)
            color = (255, 255, 255, alpha)  # Gradient blanc
            pygame.draw.line(top_gradient, color, (0, gradient_size -  y), (map_width, gradient_size -  y))
        screen.blit(top_gradient, (-scroll[0], -scroll[1] - 2))  # Dessiner le gradient en haut


        # Gradient en bas
        bottom_gradient = pygame.Surface((map_width, gradient_size), pygame.SRCALPHA)
        for y in range(gradient_size):
            alpha = int((y / gradient_size) * 255)
            color = (0, 0, 0, alpha)
            pygame.draw.line(bottom_gradient, color, (0, y), (map_width, y))
        screen.blit(bottom_gradient, (-scroll[0], map_height - gradient_size - scroll[1]))

        # Gradient à gauche
        left_gradient = pygame.Surface((gradient_size, screen_height), pygame.SRCALPHA)
        for x in range(gradient_size):
            alpha = int((x / gradient_size) * 255)
            color = (0, 0, 0, alpha)
            pygame.draw.line(left_gradient, color, ((gradient_size - x), 0), ((gradient_size - x), screen_height))
        screen.blit(left_gradient, (-scroll[0] - 2, 0))  # -2 car le bord est décalé (pourquoi ? bonne question)

        # Gradient à droite
        right_gradient = pygame.Surface((gradient_size, screen_height), pygame.SRCALPHA)
        for x in range(gradient_size):
            alpha = int((x / gradient_size) * 255)
            color = (0, 0, 0, alpha)
            pygame.draw.line(right_gradient, color, (x, 0), (x, screen_height))
        screen.blit(right_gradient, (map_width - gradient_size - scroll[0], 0))

        
 




    def draw_tile(self,screen,scroll,player = None, grid = False,map_layer = None):
        """
        Méthode qui permet de dessiner les tuiles (tile) sur le screen
        """
        tile_size = Settings.TILE_SIZE

        start_x = max(0,int(scroll[0] // tile_size)- 1)
        start_y = max(0,int(scroll[1] // tile_size)-1)
        
        end_x = min(self.size["width"], int((scroll[0] + Settings.SCREEN_RESOLUTION[0]) // tile_size) + 1)
        end_y = min(self.size["height"], int((scroll[1] + Settings.SCREEN_RESOLUTION[1]) // tile_size) + 1) 
        
        for layer in self.layers:
            self.collision_dict[layer].empty()
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    if grid:
                        border_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                        border_surface.fill((0, 0, 0, 0)) 
                        pygame.draw.rect(border_surface, (255, 255, 255, 2), (0, 0, tile_size, tile_size), 1)
                        screen.blit(border_surface, (x * tile_size - scroll[0], y * tile_size - scroll[1]))


                    if self.data[layer][y][x] != "-1":
                        tile = self.data[layer][y][x]
                        if map_layer:
                            if map_layer == layer:
                                tile.image.set_alpha(256)
                            else:
                                tile.image.set_alpha(128)
                            
                        
                        elif player:
                            player_x, player_y = int(player.position[0] // tile_size), int(player.position[1] // tile_size)
                            if self.data[layer][y][x] != "-1":
                                if abs(player_x - x) <= 2 and abs(player_y - y) <= 2:
                                    self.collision_dict[layer].add(tile)
                        tile.draw(screen, scroll)




    def draw_borders(self,screen,scroll):
        """
        Méthode qui permet de dessiner le bord de la carte
        """
        map_width = self.size["width"] * Settings.TILE_SIZE 
        map_height = self.size["height"] * Settings.TILE_SIZE
        
        pygame.draw.rect(screen, (255, 255, 255), (-scroll[0], -scroll[1] , map_width, map_height),1)
    







    