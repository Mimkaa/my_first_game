import pygame as pg
import sys
pg.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
GRAY=(220,220,220)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN=(0,255,255)
DARKBLUE=(0,0,49)
PURPLE=(172,79,198)
# game settings
WIDTH = pg.display.Info().current_w
HEIGHT =pg.display.Info().current_h  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Spirit`s Life"
BGCOLOR = DARKGREY
NIGHTCOLOR=(20, 20, 20)
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
# Layers
WALL_LAYER=4
PLAYER_LAYER=3
DECORATION_LAYER1=1
DECORATION_LAYER2=2
DECORATION_LAYER3=3
DECORATION_LAYER4=4
THE_HEIGHEST=5
#Toyya
Toyya_HAUSE=['Toyya-Home.png','Toyya-Home_open.png']
TOYYA_ANIMATION=['TOYYA1.png','TOYYA2.png','TOYYA3.png','TOYYA4.png','TOYYA5.png','TOYYA6.png','TOYYA7.png','TOYYA8.png','TOYYA9.png','TOYYA10.png','Toyya_head.png',"TOYYA_LATERAL_LOOK.png","TOYYA11.png","TOYYA12.png","TOYYA_HAPPY_LATERAL.png"]
TOYYA_WALKING_ANIMATION=['TOYYA_WALK_FORWARD1.png','TOYYA_WALK_FORWARD2.png','TOYYA_WALK_FORWARD3.png','TOYYA_WALK_FORWARD2.png','TOYYA_WALK_FORWARD1.png','TOYYA_WALK_FORWARD4.png','TOYYA_WALK_FORWARD5.png','TOYYA_WALK_FORWARD4.png']
TOYYA_WALKING_ANIMATION_LEFT=['TOYYA_LATERAL_LOOK.png','TOYYA_WALK_LEFT2.png','TOYYA_WALK_LEFT3.png','TOYYA_WALK_LEFT2.png','TOYYA_LATERAL_LOOK.png','TOYYA_WALK_LEFT4.png','TOYYA_WALK_LEFT5.png','TOYYA_WALK_LEFT4.png']
TOYYA_WALKING_ANIMATION_BACK=["TOYYA10.png","TOYYA_WALK_BACK2.png","TOYYA_WALK_BACK3.png","TOYYA_WALK_BACK2.png","TOYYA10.png","TOYYA_WALK_BACK4.png","TOYYA_WALK_BACK5.png","TOYYA_WALK_BACK4.png"]
TOYYA_SPEED=150
# Player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 50)
PLAYER_ADDITIONS=['EAT_FORWARD.png']
PLAYER_STAY=['front_idle_animation1.png','front_idle_animation2.png','front_idle_animation3.png','front_idle_animation4.png','front_idle_animation5.png']
PLAYER_MOVE_FORWARD=['interpolation_for_going_forward_animetion.png','front_going_animation1.png','front_going_animation2.png','front_idle_animation3.png','front_going_animation3.png',"front_going_animation4.png"]
PLAYER_MOVE_BACK=['interpolation_for_going_backward_animetion.png','back_going_animation1.png','back_going_animation2.png','back_idle_animation3.png','back_going_animation3.png',"back_going_animation4.png"]
PLAYER_MOVE_LEFT=['left_idle_animation3.png','left_going_animation1.png','left_going_animation2.png','left_idle_animation3.png','left_going_animation3.png','left_going_animation4.png']
PLAYER_STAY_BACK=['back_idle_animation1.png','back_idle_animation2.png','back_idle_animation3.png','back_idle_animation4.png','back_idle_animation5.png']
PLAYER_STAY_LEFT=['left_idle_animation1.png','left_idle_animation2.png','left_idle_animation3.png','left_idle_animation4.png','left_idle_animation5.png']
PLAYER_GLATTONY_FORWARD_ANIMATION=['glattony_forward1.png','glattony_forward2.png','glattony_forward3.png','glattony_forward4.png','glattony_forward5.png']
PLAYER_GLATTONY_BACKWARD_ANIMATION=['standing_back1.png','standing_back2.png','glattony_backward1.png','glattony_backward2.png','glattony_backward3.png']
PLAYER_GLATTONY_RIGHT_ANIMATION=['glattony_right1.png','glattony_right2.png','glattony_right3.png','glattony_right4.png','glattony_right5.png']
PLAYER_HOLDING_LEFT_ANIMATION=['left_holding_animation1.png',"left_holding_animation2.png",'left_holding_animation3.png','left_holding_animation4.png','left_holding_animation5.png']
PLAYER_HOLDING_GOING_LEFT_ANIMATION=['left_holding_animation3.png','left_holding_going_animation1.png','left_holding_going_animation2.png','left_holding_animation2.png',"left_holding_going_animation3.png","left_holding_going_animation4.png"]
PLAYER_HOLDING_FRONT_ANIMATION=['front_holding_animation1.png',"front_holding_animation2.png","front_holding_animation1.png","front_holding_animation3.png","front_holding_animation4.png","front_holding_animation5.png"]
PLAYER_HOLDING_FRONT_GOING_ANIMATION=['front_holding_going_animation1.png','front_holding_going_animation2.png','front_holding_animation3.png','front_holding_going_animation3.png','front_holding_going_animation4.png','interpolation_for_going_forward_holding_animetion.png']
PLAYER_HOLDING_BACK_ANIMATION=['back_holding_animation1.png','back_holding_animation2.png','back_holding_animation1.png','back_holding_animation3.png','back_holding_animation4.png','back_holding_animation5.png']
PLAYER_HOLDING_GOING_BACK_ANIMATION=['interpolation_for_holding_going_backward_animetion.png','back_holding_going_animation1.png','back_holding_going_animation2.png','back_holding_animation3.png','back_holding_going_animation3.png','back_holding_going_animation4.png']
# Other animations
MENU_ANIMATION=['menu_sleep1.png','menu_sleep2.png','menu_sleep3.png','menu_sleep4.png','menu_sleep5.png']
UNSLEEP_MENU_ANIMATION=['menu_not_sleep1.png','menu_not_sleep2.png','menu_not_sleep3.png','menu_not_sleep4.png','menu_not_sleep5.png']
MASHROOM=['mashroom1.png','mashroom2.png','mashroom3.png']
ABBYSS_ANIMATION=['color_1 (2).png','color_2 (2).png','color_3 (2).png','color_4 (2).png','color_5 (2).png','color_6 (2).png','color_7 (2).png','color_8 (2).png','color_9 (2).png']
FIREFLY_ANIMATION=['filefly1.png','filefly2.png','filefly3.png']
FLOWER_ANIMATION=['flower2.png','flower3.png','flower4.png','flower5.png','flower6.png','flower.png']
GRASS_ANIMATION=['pos1.png','pos2.png']
ORDINARY_GRASS_ANIMATION=['grass11.png','grass22.png']
WATER_ANIMATION=['water1.png','water2.png','waves.png','waves2.png','interpolation.png']
TREE_ANIMATION=['tree1.png','tree2.png','tree3.png']
CHECKPOINT_ANIMATION=['checkpoint1.png','checkpoint2.png','checkpoint3.png','checkpoint4.png','checkpoint5.png']
CRYSRAL_ANIMATION=['crystal_0000_Layer-1-copy.png','crystal_0001_Layer-1-copy-2.png','crystal_0002_Layer-1-copy-3.png','crystal_0003_Layer-1-copy-4.png','crystal_0004_Layer-1-copy-5.png','crystal_0005_Layer-1.png']
WALLS_IMAGES=['wallcolor1.png','interpolation1.png','interpolation2.png']
PINE=['PINE.png']
APPLE=["apple.png","apple1.png","apple2.png","apple3.png","apple4.png"]
# Decorations settings

BOB_RANGE=50
BOB_RANGE2=18
BOB_SPEED=0.6
# MUSIC
MENU='menu.ogg'
CAVE='CAVE.ogg'
#Other
WIND_SPEED=1000
#check_point
CP_FILE='checkpoint.txt'

# MOBS
RABBIT=['rabbit.png']
RABBIT_MOVE_FORWARD=['rabbit_move_front1.png','rabbit_move_front2.png','rabbit_move_front3.png','rabbit_move_front4.png','rabbit_move_front5.png']
RABBIT_MOVE_BACKWARD=['rabbit_move_back1.png','rabbit_move_back2.png','rabbit_move_back3.png','rabbit_move_back4.png','rabbit_move_back5.png']
RABBIT_MOVE_LEFT=['rabbit.png','rabbit_move_left.png','rabbit_move_left1.png','rabbit_move_left2.png','rabbit_move_left3.png']