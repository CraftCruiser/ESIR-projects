
from scripts.map import File

class Settings():
        

    def init():
        #___/Configuration modifiable par le joueur\___
        #La configuration modifiable par le joueur est contenue dans "settings.json"
        settings_data = File.import_json("settings.json")
        for setting,value in settings_data.items():
            if setting == "display_resolution":
                Settings.DISPLAY_RESOLUTION = value
            elif setting == "fullscreen":
                Settings.FULLSCREEN = bool(value)
            elif setting == "show_fps":
                Settings.SHOW_FPS = bool(value)
            elif setting == "play_intro":
                Settings.PLAY_INTRO = bool(value)
            elif setting == "play_music":
                Settings.PLAY_MUSIC = bool(value)
            elif setting == "music_volume":
                Settings.MUSIC_VOLUME = value
        
        #___/Configuration inmodifiable par le joueur\___
        Settings.SCREEN_SCALE = Settings.DISPLAY_RESOLUTION[0] // 400
        Settings.SCREEN_RESOLUTION = [x // Settings.SCREEN_SCALE for x in Settings.DISPLAY_RESOLUTION]
        Settings.TILE_SIZE = 16
        Settings.GAME_FPS = 60
        
        



    def change_intro_state():
        Settings.PLAY_INTRO = not Settings.PLAY_INTRO
        data = File.import_json("settings.json")
        data["play_intro"] = Settings.PLAY_INTRO
        File.export_json("settings.json",data)
        


    def change_show_fps():
        Settings.SHOW_FPS = not Settings.SHOW_FPS
        data = File.import_json("settings.json")
        data["show_fps"] = Settings.SHOW_FPS
        File.export_json("settings.json",data)


    def change_full_screen():
        Settings.FULLSCREEN = not Settings.FULLSCREEN
        data = File.import_json("settings.json")
        data["fullscreen"] = Settings.FULLSCREEN
        File.export_json("settings.json",data)

    def change_play_music():
        Settings.PLAY_MUSIC = not Settings.PLAY_MUSIC
        data = File.import_json("settings.json")
        data["play_music"] = Settings.PLAY_MUSIC
        File.export_json("settings.json",data)

    def change_volume(value):
        if value == "up":
            Settings.MUSIC_VOLUME = min(1,Settings.MUSIC_VOLUME + 0.1)
        elif value == "down":
            Settings.MUSIC_VOLUME = max(0.1,Settings.MUSIC_VOLUME - 0.1)
        
        data = File.import_json("settings.json")
        data["music_volume"] = Settings.MUSIC_VOLUME
        File.export_json("settings.json",data)