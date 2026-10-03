import pygame

pygame.init()

class Timer:





    def __init__(self):
        self.is_paused = False
        self.is_timer_on = False
        self._start_time = 0
        self._pause_time = 0
        self._total_paused_time = 0 


    def start_timer(self):
        """
        Démarre le timer, permet également de le redemarrer
        """
        self.start_time = pygame.time.get_ticks()
        self.is_paused = False
        self.total_paused_time = 0
        self.is_timer_on = True


    def get_time(self):
        """
        Méthode qui permet d'avoir le temps du Timer
        """
        if self.is_paused:
            return (self.pause_time - self.start_time - self.total_paused_time) / 1000
        else:
            return (pygame.time.get_ticks() - self.start_time - self.total_paused_time) / 1000

    def pause_timer(self):
        """
        Méthode qui permet de mettre en pause le timer
        """
        if not self.is_paused:
            self.pause_time = pygame.time.get_ticks()
            self.is_paused = True

    def resume_timer(self):
        """
        Méthode qui permet de reprendre le timer
        """
        if self.is_paused:
            self.total_paused_time += pygame.time.get_ticks() - self.pause_time
            self.is_paused = False
