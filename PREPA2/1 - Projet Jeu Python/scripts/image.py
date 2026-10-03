import pygame
import os

from settings import Settings

class Images():
    def extract_tile_from_tileset(tileset_path,tile_size,x,y):
        """
        Fonction qui permet de récuperer une tile d'un tileset en fonction de sa taille et de son emplacement dans le tileset
        """
        if os.path.exists(tileset_path):
            tileset_image = pygame.image.load(tileset_path).convert_alpha()
            rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
            return tileset_image.subsurface(rect)
        else:
            print(f"Fichier non trouvé lors du chargement des textures : {tileset_path} ")


    def extract_animation_line_from_sheet(sheet_path,animation_level,frame_number,symmetry, width,height):
        if os.path.exists(sheet_path):
            res = []
            tileset_image = pygame.image.load(sheet_path).convert_alpha()
            for x in range(frame_number):
                rect = pygame.Rect(x * width, animation_level * height, width, height)
                frame = tileset_image.subsurface(rect)
                if symmetry == "vertical":
                    frame = pygame.transform.flip(frame, False, True)
                elif symmetry == "horizontal":
                    frame = pygame.transform.flip(frame, True, False)

                res.append(frame)
            return res
        else:
            print(f"Fichier non trouvé : {sheet_path}")
            return []


    def extract_animations_from_sheet(sheet_path,animation_data,width,height):
        """
        Prend en paramètre le chemin du sheet et les animations à extraire et renvoie un dictionnaire contenant le en key le nom de l'animation et en valeur une liste contenant l'animation
        animation_data:
            { 
            "animation_name1" = [line_of_the_animation,frame_number,symmetry],
            "animation_name1" = [line_of_the_animation,frame_number,symmetry],    
            "animation_name2" = [line_of_the_animation,frame_number,symmetry],
            ...        
            }
        """
        if os.path.exists(sheet_path):
            return {name : Images.extract_animation_line_from_sheet(sheet_path,data[0],data[1],data[2],width,height) for name, data in animation_data.items()}
        else:
            print(f"Fichier non trouvé : {sheet_path} ")


    
    def is_tile_empty(tile):
        """
        Vérifie si tous les pixels du tile sont transparents
        """
        for x in range(tile.get_width()):
            for y in range(tile.get_height()):
                if tile.get_at((x, y))[3] != 0:  # Vérifie si le pixel a une opacité non nulle
                    return False
        return True



    def extract_tiles(tileset_path):
        """
        Permet d'extraire les tiles d'un tileset dans un dictionnaire, en ignorant les tiles vides.
        """
        
        tileset = pygame.image.load(tileset_path)
        
        # Dimensions du tileset
        tileset_width, tileset_height = tileset.get_size()

        # Dictionnaire pour stocker les tiles valides
        tiles = {}

        # Parcours du tileset
        for y in range(0, tileset_height, Settings.TILE_SIZE):
            for x in range(0, tileset_width, Settings.TILE_SIZE):
                # Extraire une sous-surface
                tile = tileset.subsurface((x, y, Settings.TILE_SIZE, Settings.TILE_SIZE))

                # Vérifier si le tile n'est pas complètement vide
                if not Images.is_tile_empty(tile):
                    key = f"tileset_{x//Settings.TILE_SIZE}_{y//Settings.TILE_SIZE}"
                    tiles[key] = tile

        return tiles
    


if __name__ == "__main__":
    
    
    print(Images.extract_tiles("assets/maps/test/textures/tiles/tileset.png", 16))