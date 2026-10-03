from scripts.map import Map



class GameConfig:
    #---/Movement Config\---

    WALKING_A_X  = 0.5
    FRICTION_GX = 0.3
    MAX_VELOCITY = WALKING_A_X / FRICTION_GX
    #Vitesse max = MAX_VELOCITY * 3.75 (cube / seconde)
    #Plus le rapport WALKING_A_X / MAX_VELOCITY est faible, plus le personnage mettra du temps à atteindre sa vitesse max

    FRICTION_AX = 0.07

    


    GRAVITY_A_Y = 0.3
    FRICTION_Y = 0.05

    
    MIN_VELOCITY = MAX_VELOCITY / 1000

    DASH_VELOCITY = 12.5
    JUMP_Y_VELOCITY = 7

    Y_SCROLLING = True
    X_SCROLLING = True
    SCROLLING_SMOOTHNESS = 10
        
    BACKGROUND_COLOR = (36,36,51)
    TUTORIAL_BACKGROUND_COLOR = (0,0,0)
    BORDER_COLOR = (0,0,0)
   


    

    

    


        


