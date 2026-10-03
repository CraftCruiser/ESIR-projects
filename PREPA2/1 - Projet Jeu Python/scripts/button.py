import pygame

from settings import Settings


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, action, image_still, image_hovered=None, image_clicked=None, scale_factor=1.0, center=False, top_right= False,play_sound=False):
        super().__init__()

        # ___/action\___
        self.action = action
        
        # ___/Image/Rect\___
        self.images = {
            "image_still": pygame.transform.scale(image_still, (int(image_still.get_width() * scale_factor), int(image_still.get_height() * scale_factor))),
            "image_hovered": pygame.transform.scale(image_hovered, (int(image_hovered.get_width() * scale_factor), int(image_hovered.get_height() * scale_factor))) if image_hovered else None,
            "image_clicked": pygame.transform.scale(image_clicked, (int(image_clicked.get_width() * scale_factor), int(image_clicked.get_height() * scale_factor))) if image_clicked else None
        }

        self.image = self.images["image_still"]
        if center:
            self.rect = self.image.get_rect(center=[pos_x, pos_y])
           
        elif top_right:
            self.rect = self.image.get_rect(topright = [pos_x, pos_y])
        else:
            self.rect = self.image.get_rect(topleft=[pos_x, pos_y])
            
        
        # ___/Etat\___
        self.current_image = "image_still"
        self.is_clicked = False  # Initialisation de l'état 'non-cliqué'
        
        # ___/Son\___
        self.play_sound = play_sound
        self.hovered_sound = pygame.mixer.Sound("assets/sounds/selection1.wav")
        self.hovered_sound.set_volume(0.05)
        self.clicked_sound = pygame.mixer.Sound("assets/sounds/clicked.wav")
        self.clicked_sound.set_volume(0.1)

        # ___/Suivi des sons\___
        self.is_hovered_last = False
        self.is_clicked_last = False

    def update(self):
        """
        Méthode qui met à jour le bouton (Change l'image en fonction de l'action et vérifie si l'utilisateur clique dessus).
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_clicked = pygame.mouse.get_pressed()[0]

        mouse_x //= Settings.SCREEN_SCALE
        mouse_y //= Settings.SCREEN_SCALE

        is_hovered = self.rect.collidepoint(mouse_x, mouse_y)

        if is_hovered:
            # Si la souris entre dans la zone du bouton, changer l'image à 'hovered'
            if self.images["image_hovered"] and not is_clicked and self.current_image != "image_hovered":
                self.image = self.images["image_hovered"]
                self.current_image = "image_hovered"
                # Jouer le son de survol
                if self.play_sound and not self.is_hovered_last:
                    self.hovered_sound.play()

            # Si l'utilisateur clique sur le bouton, changer l'image à 'clicked'
            if is_clicked and self.images["image_clicked"]:
                self.image = self.images["image_clicked"]
                self.current_image = "image_clicked"
                # Jouer le son de clic
                if self.play_sound and not self.is_clicked_last:
                    self.clicked_sound.play()
        else:
            # Si la souris n'est plus sur le bouton, revenir à l'état "image_still"
            self.image = self.images["image_still"]
            self.current_image = "image_still"

        # Si le bouton est cliqué, exécuter l'action
        if is_hovered and not is_clicked and self.is_clicked:
            self.action()

        # Mettre à jour les états précédents pour éviter de jouer les sons en boucle
        self.is_hovered_last = is_hovered
        self.is_clicked_last = is_clicked

        # Mettre à jour l'état de pression
        self.is_clicked = is_clicked










class ToggleButton(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, action, image_still_not_pressed, image_still_pressed,
             image_hovered_not_pressed=None, image_hovered_pressed=None,  
             image_clicked_not_pressed=None, image_clicked_pressed=None, scale_factor=1.0,  
             center=False, play_sound=False, pressed_by_default=False):
        super().__init__()

        # ___/action\___
        self.action = action

        # ___/Images pour les deux états (enfoncé et non-enfoncé)\___
        self.images_not_pressed = {
            "image_still": pygame.transform.scale(image_still_not_pressed, (int(image_still_not_pressed.get_width() * scale_factor), int(image_still_not_pressed.get_height() * scale_factor))),
            "image_hovered": pygame.transform.scale(image_hovered_not_pressed, (int(image_hovered_not_pressed.get_width() * scale_factor), int(image_hovered_not_pressed.get_height() * scale_factor))) if image_hovered_not_pressed else None,
            "image_clicked": pygame.transform.scale(image_clicked_not_pressed, (int(image_clicked_not_pressed.get_width() * scale_factor), int(image_clicked_not_pressed.get_height() * scale_factor))) if image_clicked_not_pressed else None
        }

        self.images_pressed = {
            "image_still": pygame.transform.scale(image_still_pressed, (int(image_still_pressed.get_width() * scale_factor), int(image_still_pressed.get_height() * scale_factor))),
            "image_hovered": pygame.transform.scale(image_hovered_pressed, (int(image_hovered_pressed.get_width() * scale_factor), int(image_hovered_pressed.get_height() * scale_factor))) if image_hovered_pressed else None,
            "image_clicked": pygame.transform.scale(image_clicked_pressed, (int(image_clicked_pressed.get_width() * scale_factor), int(image_clicked_pressed.get_height() * scale_factor))) if image_clicked_pressed else None
        }

        # ___/Initialisation de l'image et du rect\___
        self.is_pressed = pressed_by_default
        self.current_image = "image_clicked" if self.is_pressed else "image_still"
        self.image = self.images_pressed["image_clicked"] if self.is_pressed else self.images_not_pressed["image_still"]

        if not center:
            self.rect = self.image.get_rect(topleft=[pos_x, pos_y])
        else:
            self.rect = self.image.get_rect(center=[pos_x, pos_y])

        # ___/Son\___
        self.play_sound = play_sound
        self.hovered_sound = pygame.mixer.Sound("assets/sounds/selection1.wav")
        self.hovered_sound.set_volume(0.05)
        self.clicked_sound = pygame.mixer.Sound("assets/sounds/clicked.wav")
        self.clicked_sound.set_volume(0.1)

        # ___/Action\___
        self.is_clicked = False

        # Variable pour vérifier si la souris a précédemment survolé le bouton
        self.is_hovered_last = False
        # Variable pour vérifier si le bouton a précédemment été pressé
        self.is_pressed_last = False

    def update(self):
        """
        Méthode qui met à jour le bouton (Change l'image en fonction de l'action et vérifie si l'utilisateur clique dessus).
        Le bouton alterne entre les états 'pressé' et 'relâché'.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_clicked = pygame.mouse.get_pressed()[0]

        mouse_x //= Settings.SCREEN_SCALE
        mouse_y //= Settings.SCREEN_SCALE

        is_hovered = self.rect.collidepoint(mouse_x, mouse_y)

        # Sélectionner les images en fonction de l'état
        if self.is_pressed:
            current_images = self.images_pressed
        else:
            current_images = self.images_not_pressed

        # Gestion de l'image de survol
        if is_hovered:
            if not is_clicked:  # Survol mais pas cliqué
                if current_images["image_hovered"]:
                    self.image = current_images["image_hovered"]
                    self.current_image = "image_hovered"
                    # Si la souris entre dans la zone du bouton, jouer le son
                    if self.play_sound and not self.is_hovered_last:
                        self.hovered_sound.play()
            else:  # Survol + cliqué
                if current_images["image_clicked"]:
                    self.image = current_images["image_clicked"]
                    self.current_image = "image_clicked"
                    # Si le bouton vient d'être pressé, jouer le son
                    if self.play_sound and not self.is_pressed_last:
                        self.clicked_sound.play()
        else:
            # Si la souris n'est pas sur le bouton, afficher l'état actuel
            if self.is_pressed:
                self.image = current_images["image_still"]
                self.current_image = "image_still"
            else:
                self.image = current_images["image_still"]
                self.current_image = "image_still"

        # Mettre à jour l'état du survol et de la pression
        self.is_hovered_last = is_hovered
        self.is_pressed_last = is_clicked

        # Changer l'état du bouton en fonction du clic
        if is_hovered and not self.is_clicked and is_clicked:
            self.is_pressed = not self.is_pressed
            self.current_image = "image_clicked" if self.is_pressed else "image_still"
            self.image = self.images_pressed["image_clicked"] if self.is_pressed else self.images_not_pressed["image_still"]
            self.action()

        self.is_clicked = is_clicked




