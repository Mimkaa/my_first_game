import random

import pygame as pg
from pygame.locals import *
import sys
import time
from os import path
from settings import *
from sprites import *
from tile_map import *
from other_objects import *
from decorational_sprites import*
from other_helping_classes import*
from cutscenes import *
from quests import *
from random import randint
import json
from mobs import *

flags=FULLSCREEN|DOUBLEBUF
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.pre_init(44100, -16, 1, 2048)
        self.sounds=True
        self.screen = pg.display.set_mode((WIDTH,HEIGHT), flags)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.using_menu = True
        self.posed=False
        self.in_front_of_choice=False
        self.continuee=False
        self.check_point=0
        self.current_time=0
        self.which_map=0
        # for timer
        self.sec = 0
        self.min = 0
        self.hour = 0
        self.min_checkpoint=0
        self.sec_checkpoint = 0
        self.hour_checkpoint = 0
        #DATA LOADING
        self.all_tiles_set = False
        self.load_data()
        # for menu and premenu
        self.menu_sprites = pg.sprite.LayeredUpdates()
        self.for_menu_image = pg.sprite.Group()
        self.flying_things_maker(30)
        self.customize = Menu_img(self,WIDTH / 2, HEIGHT / 4 + 100)
        self.button_1 = Button(self)
        self.button_2 = Button(self)
        self.button_3=Button(self)
        self.button_4=Button(self)
        self.button_5=Button(self)
        self.button_list = [self.button_2,self.button_3,self.button_4,self.button_5]
        self.button_listt= [self.button_2,self.button_3,self.button_4,self.button_5,self.button_5]
        self.button_list1=[self.button_1, self.button_2,self.button_3]
        # for checkpoint menu
        self.wbutton_1 = Wight_Button(self)
        self.wbutton_2 = Wight_Button(self)
        self.wbutton_list = [self.wbutton_1, self.wbutton_2]
        # jumping through cutscenes
        self.captured_text=''
        self.skip_to_point=False
        self.choice_keeper=0
        # debugging
        self.draw_debag_just_rect=False
        self.draw_debag = False
        self.enumerate_sprites=False
        self.draw_tiles=False
        # drawing_F
        self.draw_F=True

        # cutscene_manager
        self.cutscene_manager = CutSceneManager(self)

        # quest_manager
        self.quest_manager=QuestManager(self)

        # for division of the map by tiles for pathfinding
        self.dict_of_tup_coords_cell = {}
        self.dict_of_tiles=self.make_dict_of_tiles()

    # loads animation
    def load_animation(self, folder, frames, resize=(1, 1),resize_buy_changing_size_completely=(),flip=False):
        folder=path.join(self.img_folder, folder)
        animation = []
        for img in frames:
            animation.append(pg.image.load(path.join(folder,img)).convert_alpha())
        if not resize_buy_changing_size_completely:
            for num, img in enumerate(animation):
                animation[num] = pg.transform.scale(img, (img.get_width() * resize[0], img.get_height() * resize[1]))
        elif len(resize_buy_changing_size_completely)>1:
            for num, img in enumerate(animation):
                animation[num] = pg.transform.scale(img, (int(resize_buy_changing_size_completely[0]), int(resize_buy_changing_size_completely[1])))
        if flip:
            for num, img in enumerate(animation):
                animation[num]=pg.transform.flip(animation[num], True, False)

        return animation

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        #CHECK_POINT
        #data=''
        with open(path.join(self.game_folder, CP_FILE), 'r') as f:
            try:
                self.lines=f.readlines()
                for line in self.lines:
                    self.check_point = int(line[0])
                    splited = line.split(":")
                    self.hour=int(splited[2])
                    self.min=int(splited[3])
                    self.sec=int(splited[4])
                    self.hour_checkpoint=int(splited[5])
                    self.min_checkpoint = int(splited[6])
                    self.sec_checkpoint = int(splited[7])
                    self.sounds=json.loads(splited[8].lower())

            except:
                self.check_point=0

        self.which_map=self.check_point
        self.img_folder = path.join(self.game_folder, 'images')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.others_folder=path.join(self.img_folder,'others')
        self.abyss_folder=path.join(self.img_folder,'abyss')
        self.flower_folder=path.join(self.img_folder,'flower')
        self.water_folder=path.join(self.img_folder,'cave water')
        self.grass_folder=path.join(self.img_folder,'grass')
        self.ordinary_grass_folder=path.join(self.img_folder,'vegetation')
        self.tree_folder=path.join(self.img_folder,'tree')
        self.checkpoint_folder=path.join(self.img_folder,'checkpoint')
        self.crystal_folder=path.join(self.img_folder,'crystal')
        self.wall_folder=path.join(self.img_folder,'wall interapolation')
        self.vegetation_folder=path.join(self.img_folder,'vegetation')
        self.Toyya_folder=path.join(self.img_folder,'Toyya')
        self.player_folder=path.join(self.img_folder,'player')
        self.menu_folder=path.join(self.img_folder,'menu')
        snd_folder = path.join(self.game_folder, 'sound')
        self.music_folder =path.join(self.game_folder, 'music')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        #maps
        self.map_list=[]
        self.map = TiledMap(path.join(self.map_folder,'start.tmx'))
        self.map_list.append(self.map)
        self.map1 = TiledMap(path.join(self.map_folder, 'cave_exit.tmx'))
        self.map_list.append(self.map1)
        self.map2 = TiledMap(path.join(self.map_folder, 'first_location.tmx'))
        self.map_list.append(self.map2)
        self.map_img=self.map_list[self.which_map].make_map()
        self.map_rect=self.map_img.get_rect()
        # font
        self.title_font = path.join(self.img_folder, 'PixelColeco-4vJW.ttf')
        # buttons for menu
        self.button=pg.image.load(path.join(self.img_folder,'button.png')).convert_alpha()
        self.button2 = pg.image.load(path.join(self.img_folder, 'button2.png')).convert_alpha()
        # animations
        # main stuff
        self.Toyya_animation=[]
        for img in TOYYA_ANIMATION:
            self.Toyya_animation.append(pg.image.load(path.join(self.Toyya_folder, img)).convert_alpha())
        for num,img in enumerate(self.Toyya_animation):
            self.Toyya_animation[num]=pg.transform.scale(img,(img.get_width()*2,img.get_height()*2))

        self.Toyya_walking_animation = []
        for img in TOYYA_WALKING_ANIMATION:
            self.Toyya_walking_animation.append(pg.image.load(path.join(self.Toyya_folder, img)).convert_alpha())
        for num,img in enumerate(self.Toyya_walking_animation):
            self.Toyya_walking_animation[num]=pg.transform.scale(img,(img.get_width()*2,img.get_height()*2))

        self.Toyya_move_left_animation = self.load_animation("Toyya", TOYYA_WALKING_ANIMATION_LEFT,
                                                             resize=(2, 2))
        self.Toyya_move_back_animation=self.load_animation("Toyya", TOYYA_WALKING_ANIMATION_BACK,
                                                             resize=(2, 2))
        self.Toyya_move_right_animation=[]
        for img in self.Toyya_move_left_animation:
            self.Toyya_move_right_animation.append(pg.transform.flip(img,True,False))
        # Player
        self.player_additional_img=[]
        for img in PLAYER_ADDITIONS:
            self.player_additional_img.append(pg.image.load(path.join(self.player_folder,img)).convert_alpha())





        self.player_glattony_forward_animation=[]
        for img in PLAYER_GLATTONY_FORWARD_ANIMATION:
            self.player_glattony_forward_animation.append(pg.image.load(path.join(self.player_folder, img)).convert_alpha())
        self.player_glattony_backward_animation = []
        for img in PLAYER_GLATTONY_BACKWARD_ANIMATION:
            self.player_glattony_backward_animation.append(pg.image.load(path.join(self.player_folder, img)).convert_alpha())
        self.player_glattony_right_animation = []
        for img in PLAYER_GLATTONY_RIGHT_ANIMATION:
            self.player_glattony_right_animation.append(pg.image.load(path.join(self.player_folder, img)).convert_alpha())
        self.player_glattony_left_animation=[]
        for img in self.player_glattony_right_animation:
            self.player_glattony_left_animation.append(pg.transform.flip(img, True, False))
        self.player_left_holding_animation=self.load_animation("re_player",PLAYER_HOLDING_LEFT_ANIMATION,resize=(3, 3))
        self.player_right_holding_animation = self.load_animation("re_player", PLAYER_HOLDING_LEFT_ANIMATION,flip=True,resize=(3, 3))
        self.player_left_holding_going_animation = self.load_animation("re_player", PLAYER_HOLDING_GOING_LEFT_ANIMATION,resize=(3, 3))
        self.player_right_holding_going_animation = self.load_animation("re_player", PLAYER_HOLDING_GOING_LEFT_ANIMATION, flip=True,resize=(3, 3))
        self.player_front_holding_animation=self.load_animation("re_player", PLAYER_HOLDING_FRONT_ANIMATION,resize=(3, 3))
        self.player_front_going_holding_animation = self.load_animation("re_player", PLAYER_HOLDING_FRONT_GOING_ANIMATION,resize=(3, 3))
        self.player_back_holding_animation=self.load_animation("re_player", PLAYER_HOLDING_BACK_ANIMATION,resize=(3, 3))
        self.player_back_going_holding_animation = self.load_animation("re_player",PLAYER_HOLDING_GOING_BACK_ANIMATION,resize=(3, 3))
        self.stay_animation = self.load_animation("re_player", PLAYER_STAY, resize=(3, 3))
        self.move_forward_animation = self.load_animation("re_player", PLAYER_MOVE_FORWARD, resize=(3, 3))
        self.stay_animation_back = self.load_animation("re_player", PLAYER_STAY_BACK, resize=(3, 3))
        self.move_back_animation = self.load_animation("re_player", PLAYER_MOVE_BACK, resize=(3, 3))
        self.stay_left_animation = self.load_animation("re_player", PLAYER_STAY_LEFT, resize=(3, 3))
        self.stay_right_animation = self.load_animation("re_player", PLAYER_STAY_LEFT, resize=(3, 3),flip=True)
        self.move_left_animation = self.load_animation("re_player", PLAYER_MOVE_LEFT, resize=(3, 3))
        self.move_right_animation = self.load_animation("re_player", PLAYER_MOVE_LEFT, resize=(3, 3),flip=True)

        # additions
        self.menu_animation=[]
        for img in MENU_ANIMATION:
            self.menu_animation.append(pg.image.load(path.join(self.menu_folder, img)).convert_alpha())
        self.unsleep_menu_animation=[]
        for img in UNSLEEP_MENU_ANIMATION:
            self.unsleep_menu_animation.append(pg.image.load(path.join(self.menu_folder, img)).convert_alpha())
        self.mashroom_animation=[]
        for img in MASHROOM:
            self.mashroom_animation.append(pg.image.load(path.join(self.vegetation_folder, img)).convert_alpha())
        self.abyss_animation=[]
        for img in ABBYSS_ANIMATION:
            self.abyss_animation.append(pg.image.load(path.join(self.abyss_folder, img)).convert_alpha())
        self.firefly_animation = []
        for img in FIREFLY_ANIMATION:
            self.firefly_animation.append(pg.image.load(path.join(self.abyss_folder, img)).convert_alpha())
        self.flower_animation = []
        for img in FLOWER_ANIMATION:
            self.flower_animation.append(pg.image.load(path.join(self.flower_folder, img)).convert_alpha())
        self.grass_animation=[]
        for img in GRASS_ANIMATION:
            self.grass_animation.append(pg.image.load(path.join(self.grass_folder, img)).convert_alpha())
        self.water_animation = []
        for img in WATER_ANIMATION:
            self.water_animation.append(pg.image.load(path.join(self.water_folder, img)).convert_alpha())
        self.tree_animation=[]
        for img in TREE_ANIMATION:
            self.tree_animation.append(pg.image.load(path.join(self.tree_folder, img)).convert_alpha())
        self.checkpoint_animation=[]
        for img in CHECKPOINT_ANIMATION:
            self.checkpoint_animation.append(pg.image.load(path.join(self.checkpoint_folder, img)).convert_alpha())
        self.crystal_animation=[]
        for img in CRYSRAL_ANIMATION:
            self.crystal_animation.append(pg.image.load(path.join(self.crystal_folder, img)).convert_alpha())
        self.wall_images=[]
        for img in WALLS_IMAGES:
            self.wall_images.append(pg.image.load(path.join(self.wall_folder, img)).convert_alpha())
        self.ordinary_grass=[]
        for img in ORDINARY_GRASS_ANIMATION:
            self.ordinary_grass.append(pg.image.load(path.join(self.ordinary_grass_folder, img)).convert_alpha())
        self.pine=[]
        for img in PINE:
            self.pine.append(pg.image.load(path.join(self.vegetation_folder, img)).convert_alpha())
        #apple
        self.apples=[]
        for apple in APPLE:
            self.apples.append(pg.image.load(path.join(self.vegetation_folder, apple)).convert_alpha())
        for num,img in enumerate(self.apples):
            self.apples[num] =pg.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))

        #heart
        self.heart=pg.image.load(path.join(self.others_folder, 'heart.png')).convert_alpha()
        self.heart=pg.transform.scale(self.heart,(self.heart.get_width() * 2, self.heart.get_height() * 2))



    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect



    def new(self):

        # map_name
        self.map_name = path.basename(str(self.map_list[self.which_map].tmxdata))
        self.map_name = path.splitext(self.map_name)[0]

        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.decorations=pg.sprite.Group()
        self.fireflys=pg.sprite.Group()
        self.for_changing_location=pg.sprite.Group()
        self.for_returning=pg.sprite.Group()
        self.moving_and_invisible=pg.sprite.Group()

        # for something that acts only like a background
        self.others=pg.sprite.Group()


        self.waves=pg.sprite.Group()
        self.for_reflecting=pg.sprite.Group()
        self.not_for_reflection=pg.sprite.Group()
        self.for_colliding=pg.sprite.Group()
        self.for_colliding_with=pg.sprite.Group()
        self.for_eating=pg.sprite.Group()
        self.characters=pg.sprite.Group()
        self.for_eating_keep_track=[]
        self.for_eating_keep_track_layers={}
        self.matched_with_for_eating=pg.sprite.Group()
        self.list_of_mobs=pg.sprite.Group()
        #for row, tiles in enumerate(self.map.data):
            #for col, tile in enumerate(tiles):
                #if tile == '1':
                    #Wall(self, col, row)
                #if tile == 'P':
                    #self.player = Player(self, col, row)

        # randomizing grass location of
        randomizer = randint(5, 20)
        count = 0
        self.all_tiles_set = False
        for tile_object in self.map_list[self.which_map].tmxdata.objects:
            obj_center=vec(tile_object.x+tile_object.width/2,tile_object.y+tile_object.height/2)
            if tile_object.name == 'Toyya':
                self.Toyya=Toyya(self, obj_center)
            if tile_object.name=='player':
                self.player=Player(self,obj_center)

            #ather stuff
            if tile_object.name=='wall':
                Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name=='mashroom':
                Mashroom(self,obj_center)
            if tile_object.name=='abyss':
                Abyss(self,obj_center,tile_object.width,tile_object.height)
            if tile_object.name=='firefly':
                Firefly(self,obj_center)
            if tile_object.name=='flower':
                Flower(self,obj_center,tile_object.width,tile_object.height)
            if tile_object.name=='teleport':
                Teleport(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name=='back':
                Teleport_Back(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name=='wind':
                Wind(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)


            if tile_object.name=="grass":
                CaveGrassUp(self,(tile_object.x,tile_object.y))
            if self.which_map == 1:
                if not self.all_tiles_set:
                    ti = self.map_list[self.which_map].tmxdata.get_tile_image_by_gid
                    layer = self.map_list[self.which_map].tmxdata.get_layer_by_name("Tile Layer 1")
                    if layer:
                        for x, y, gid in layer:
                            tile = ti(gid)
                            if tile:
                                CaveGrass(self, (x * self.map_list[self.which_map].tmxdata.tilewidth,
                                                 y * self.map_list[self.which_map].tmxdata.tileheight))
                        self.all_tiles_set = True



            if tile_object.name=='water':
                Water(self,tile_object.x,tile_object.y,tile_object.width, tile_object.height)
            if tile_object.name=='wave':
                Wave(self,tile_object.x,tile_object.y,tile_object.width, tile_object.height)
            if tile_object.name=='inter':
                Interpolation(self,tile_object.x,tile_object.y,tile_object.width, tile_object.height)
            if tile_object.name=='tree':
                Tree(self,obj_center,tile_object.width, tile_object.height)


            if tile_object.name=='check_point':
                Check_point(self,tile_object.x,tile_object.y,tile_object.width, tile_object.height)
            if tile_object.name=='crystal':
                Crystal(self,obj_center,tile_object.width, tile_object.height)
            if tile_object.name == 'under':
                Wall_Interpolation(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,1)
            if tile_object.name == 'under1':
                Wall_Interpolation(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,2)
            if tile_object.name == 'under2':
                Wall_Interpolation(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,3)

            if self.which_map == 2:
                if not self.all_tiles_set:
                    ti = self.map_list[self.which_map].tmxdata.get_tile_image_by_gid
                    layer = self.map_list[self.which_map].tmxdata.get_layer_by_name("GRASS")
                    if layer:
                        for x, y, gid in layer:
                            tile = ti(gid)
                            if tile :
                                count += 1
                                if count==randomizer:
                                    Ordinary_Grass(self, x*self.map_list[self.which_map].tmxdata.tilewidth, y*self.map_list[self.which_map].tmxdata.tileheight, self.map_list[self.which_map].tmxdata.tilewidth, self.map_list[self.which_map].tmxdata.tileheight)
                                    randomizer = randint(5, 20)
                                    count = 0
                        self.all_tiles_set = True


            if tile_object.name == 'o_grass':
                Ordinary_Grass(self,obj_center.x,obj_center.y, tile_object.width, tile_object.height)
            if tile_object.name == 'pine':
                Pine(self, obj_center, tile_object.width, tile_object.height)
            if tile_object.name=='Toyya-home':
                self.Toyya_Hause_animation=self.load_animation('Toyya',Toyya_HAUSE,resize_buy_changing_size_completely=(tile_object.width,tile_object.height))
                self.Toyya_Hause = pg.image.load(path.join(self.Toyya_folder, 'Toyya-Home.png')).convert_alpha()
                self.T_hause=Toyya_Hause(self, obj_center, tile_object.width, tile_object.height)
            if tile_object.name=="appletree":
                self.AppleTree=pg.image.load(path.join(self.vegetation_folder, 'AppleTree.png')).convert_alpha()
                AppleTree(self, obj_center, tile_object.width, tile_object.height)

        # rabbits
        if self.which_map == 2:
            self.rabbit_image = self.load_animation("mobs", RABBIT, resize=(3, 3))
            self.rabbit_move_forward=self.load_animation("mobs", RABBIT_MOVE_FORWARD, resize=(3, 3))
            self.rabbit_move_backward=self.load_animation("mobs", RABBIT_MOVE_BACKWARD, resize=(3, 3))
            self.rabbit_move_left=self.load_animation('mobs',RABBIT_MOVE_LEFT, resize=(3, 3))
            self.rabbit_move_right=self.load_animation('mobs',RABBIT_MOVE_LEFT, resize=(3, 3),flip=True)
            for i in range(random.randint(10,20)):
                self.list_of_mobs.add(Mob(self,choice([i.tile_rect.center for i in self.dict_of_tiles])))
        self.adjust_sprites_positions()




        self.camera = Camera(self.map_list[self.which_map].width, self.map_list[self.which_map].height)


    def adjust_sprites_positions(self):
        dict={}
        for spr in self.all_sprites:
            dict[spr]=[]
            for cell in self.dict_of_tiles.keys():
                if pg.Rect.colliderect(spr.hit_rect,cell.tile_rect)  :
                    dict[spr].append(cell)

        for key in dict.keys():
            dict_for_cells={}
            for cell in dict[key]:
                dict_for_cells[distance(key.hit_rect.centerx, key.hit_rect.centery, cell.tile_rect.centerx, cell.tile_rect.centery)]=cell
            if key not in self.decorations:
                key.pos=vec(dict_for_cells[min(dict_for_cells.keys())].tile_rect.center)
            else:
                key.pos=vec(dict_for_cells[min(dict_for_cells.keys())].tile_rect.center)
                key.hit_rect.center=key.pos
                if hasattr(key,'start_width'):
                    key.rect.left=key.hit_rect.left-key.start_width
                key.rect.bottom=key.hit_rect.bottom




    def run(self):
        # game loop - set self.playing = False to end the game
        self.using_menu=False
        self.playing=True
        pg.mixer.music.load(path.join(self.music_folder, 'CAVE.ogg'))
        if self.sounds:
            pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.second_culculation()
            self.minutes_culculation()
            self.hour_culculation()
            if not self.posed:
                self.update()
                self.draw()

    def second_culculation(self):
        now = pg.time.get_ticks()
        if now - self.current_time > 1000:
            self.current_time = now
            self.sec_checkpoint+=1
        return self.sec_checkpoint
    def minutes_culculation(self):
        if  self.sec_checkpoint>59:
            self.sec_checkpoint=0
            self.min_checkpoint+=1
        return self.min_checkpoint
    def hour_culculation(self):
        if self.min_checkpoint>59:
            self.min_checkpoint=0
            self.hour_checkpoint+=1
        return self.hour_checkpoint

    def quit(self):
        pg.quit()
        sys.exit()
    # makes_list_of_tiles
    def make_dict_of_tiles(self):
        dict= {}
        for i in range(0,self.map_rect.height,TILESIZE):
            for j in range(0,self.map_rect.width,TILESIZE):
                dict[Tile((j,i))]=Tile((j,i)).tile_rect.center
                self.dict_of_tup_coords_cell[Tile((j,i)).tup_coords]=Tile((j,i)).tile_rect.center
        return dict
    #Map changing
    def map_change_forward(self):

        self.which_map += 1
        self.map_img = self.map_list[self.which_map].make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites.empty()
        self.dict_of_tiles=self.make_dict_of_tiles()
        self.new()

        for spr in self.all_sprites:
            if hasattr(spr,'pos_back_up'):
                spr.pos=spr.pos_back_up


    def map_change_backward(self):

        self.which_map -= 1
        self.map_img = self.map_list[self.which_map].make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites.empty()
        self.dict_of_tiles = self.make_dict_of_tiles()
        self.new()

        for spr in self.all_sprites:
            if hasattr(spr,'pos_back_up'):
                spr.pos=spr.pos_back_up



    def update(self):

        # update portion of the game loop

        # handling sprites in for_eating


        hittt = pg.sprite.spritecollide(self.player,self.for_eating, False)
        if self.player.holding[1] in hittt:
                hittt.remove(self.player.holding[1])

        # if self.player.holding[1] in self.for_eating_keep_track:
        #         self.for_eating_keep_track.remove(self.player.holding[1])


        if not hittt  :
            self.for_eating_keep_track.clear()
            self.for_eating_keep_track_layers.clear()
            for spr in self.for_eating:
                spr.pseudo_vel = vec(0, 0)
                spr.touched=0


        if self.player.vel==vec(0,0):
            for spr in self.for_eating:
                spr.pseudo_vel = vec(0, 0)
        else:
            if len(self.for_eating_keep_track) > 0:

                hitt = pg.sprite.spritecollide(self.for_eating_keep_track[-1], self.for_eating, False,collide_hit_rect_only)

                if hitt:
                    for spr in hitt:
                        if spr not in self.for_eating_keep_track and spr not in self.for_eating_keep_track_layers :

                                self.for_eating_keep_track.append(spr)

                                self.for_eating_keep_track_layers[self.for_eating_keep_track[-1]] = spr



        for i, spr in enumerate(self.for_eating_keep_track):

            spr.touched = i
            for sprr in self.characters:
                hits=pg.sprite.spritecollide(sprr,self.for_eating,False)
                if hits :
                    spr.pseudo_vel = self.player.vel


        # map_change
        hits = pg.sprite.spritecollide(self.player, self.for_changing_location, True)
        if hits:
            self.map_change_forward()
        hits = pg.sprite.spritecollide(self.player, self.for_returning, True)
        if hits:
            self.map_change_backward()

        #  cutscenes update

        # self.cutscene_manager.update()
        # if self.which_map==2 and self.cutscene_manager.cut_scene==None and 'The first meeting' not in self.cutscene_manager.cut_scenes_complete:
        #      self.cutscene_manager.start_cut_scene(First_Cutscene(self,self.player,self.Toyya))
        #print(self.cutscene_manager.cut_scene.grid_for_pathfinding.walls)

        # quest_update:
        self.quest_manager.update()
        if len(self.cutscene_manager.keep_track_of_cutscenes)>0 and not self.cutscene_manager.keep_track_of_cutscenes[0].cut_scene_running:
            self.quest_manager.start_quest(FirstQuest(self))

        # layer management
        for spr in self.all_sprites:
            if hasattr(spr, "frontal") and spr.frontal:
                self.all_sprites.move_to_front(spr)
            elif not hasattr(spr,"not_changing_layer") or hasattr(spr,"not_changing_layer") and not spr.not_changing_layer:
                self.all_sprites.change_layer(spr, spr.rect.bottom)
            elif spr in self.fireflys:
                self.all_sprites.move_to_front(spr)

        #sprites update
        for sprite in self.all_sprites:
            if  sprite not in self.for_eating and sprite not in self.matched_with_for_eating:
                sprite.update()
            else:
                if pg.Rect.colliderect(self.camera.apply(sprite),self.camera.apply_rect(self.player.rect_update)):
                    sprite.update()
            # method = getattr(sprite, "layer_management", None)
            # if callable(method):
            #     sprite.layer_management()
        self.moving_and_invisible.update()

        for sprite in self.others:
            if pg.Rect.colliderect(self.camera.apply(sprite), self.camera.apply_rect(self.player.rect_update)):
                sprite.update()


        # only solution I found to stabilize interaction with interactable sprites
        hits_play_f_e = pg.sprite.spritecollide(self.player, self.for_eating, False, collide_hit_rect_only)

        if hits_play_f_e :
            for spr in hits_play_f_e:
                if  spr.type_of_physics['on_the_ground'] and not spr.taken[0]:

                    self.player.collisions()
                    spr.collisions()
        for spr,val in list(self.for_eating_keep_track_layers.items()):
            if not val:
                del self.for_eating_keep_track_layers[spr]

            self.for_eating_keep_track_layers[spr].collisions()

        if self.player.holding[1]:
            self.player.holding[1].taken_behaviour()





        # camera
        self.camera.update(self.player)










    def check_groups(self,spritee):
        if spritee not in self.others and spritee not in self.moving_and_invisible and spritee not in self.fireflys:
            return True
        else:
            return False



    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))



    def draw(self):

        self.screen.blit(self.map_img,self.camera.apply_rect(self.map_rect))

        #self.draw_grid()
        #pg.draw.rect(self.screen, RED, self.camera.apply_rect(self.player.rect), 1)
        for sprite in self.others:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debag:
                pg.draw.rect(self.screen,CYAN,self.camera.apply_rect(sprite.hit_rect),1)
            if self.draw_debag_just_rect:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.rect), 1)

        # draws tile grid
        for spr in self.dict_of_tiles.keys():
            if self.draw_tiles:
                pg.draw.rect(self.screen, PURPLE, self.camera.apply_rect(spr.tile_rect), 1)

        # enumerates interactable sprites
        if self.enumerate_sprites:
            for num,sprite in enumerate(self.for_eating):
                    self.draw_text(str(num),self.title_font,10,WHITE,self.camera.apply_rect(sprite.rect).left+self.camera.apply_rect(sprite.rect).width/2,self.camera.apply_rect(sprite.rect).top-self.camera.apply_rect(sprite.rect).height/2,align="center")
                    self.draw_text( "  t="+str(sprite.pseudo_vel), self.title_font, 10, WHITE,
                                   self.camera.apply_rect(sprite.rect).left + self.camera.apply_rect(
                                       sprite.rect).width / 2,
                                   self.camera.apply_rect(sprite.rect).bottom + self.camera.apply_rect(
                                       sprite.rect).height / 2, align="center")
            self.draw_text(str(self.for_eating_keep_track_layers), self.title_font, 20, WHITE,WIDTH/2,HEIGHT*0.9, align="center")
            pg.draw.rect(self.screen,DARKBLUE,self.camera.apply_rect(self.player.rect_update),10)
        if self.draw_debag:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.hit_rect), 1)
            for teleport in self.for_changing_location:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(teleport.hit_rect), 1)
            for teleport_back in self.for_returning:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(teleport_back.hit_rect), 1)
            for obj in self.moving_and_invisible:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(obj.rect), 1)



        #cutscene
        self.cutscene_manager.draw()
        #quest
        self.quest_manager.draw()
        #for poping up massege : if you want to choose
        for sp in self.for_colliding_with :
            hits = pg.sprite.spritecollide(sp, self.characters, False)
            hits2=pg.sprite.groupcollide(self.characters,self.for_eating,False,False)
            if not hits2:
                self.draw_F = True
            if hits and not hasattr(sp,"taken"):
                self.draw_text("Press F ", self.title_font, sp.size_for_F, WHITE, self.camera.apply_rect(sp.rect).centerx, self.camera.apply_rect(sp.rect).top-self.camera.apply_rect(sp.rect).height,
                                   align='center')
            if hasattr(sp,"taken") and sp.taken[0] :
                self.draw_F=False
            if hits and self.draw_F and hasattr(sp,'bouncing_times') and sp.type_of_physics['on_the_ground'] and not self.cutscene_manager.cut_scene:
                self.draw_text("Press F ", self.title_font, sp.size_for_F, WHITE,
                               self.camera.apply_rect(sp.rect).centerx,
                               self.camera.apply_rect(sp.rect).top - self.camera.apply_rect(sp.rect).height,
                               align='center')




        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.title_font, 20, WHITE, 50, 50, align="center")
        pg.display.flip()


    def jumping_through_cutscene(self):
        surf = pg.Surface((WIDTH / 2, HEIGHT / 2))
        surf.fill(BLACK)
        self.skip_to_point = not self.skip_to_point
        self.posed = not self.posed
        cutscene = self.cutscene_manager.cut_scene
        while self.skip_to_point:
            self.screen.blit(surf, (WIDTH / 4, HEIGHT / 4))
            self.draw_text("step,variants,step_in_step:"+self.captured_text,self.title_font,30,WHITE,WIDTH/2,HEIGHT/2,align="center")
            self.draw_text("current variant:"+str(self.choice_keeper),self.title_font,30,WHITE,WIDTH/2,HEIGHT/2+30,align="center")
            self.draw_text("variants on these steps:"+str(cutscene.decisions_on_those_steps),self.title_font,20,WHITE,WIDTH/2,HEIGHT/2+60,align="center")
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.skip_to_point = not self.skip_to_point
                        self.posed = not self.posed
                    if event.key==pg.K_BACKSPACE:
                        self.captured_text=self.captured_text[:-1]
                    else:
                        self.captured_text+=event.unicode
                    if event.key==pg.K_RETURN:
                        self.captured_text=self.captured_text.split(",")
                        cutscene.step=int(self.captured_text[0])

                        for step in range(self.cutscene_manager.cut_scene.step):
                            cutscene.step=step
                            cutscene.player.eat = False
                            cutscene.update()
                            for character in self.cutscene_manager.cut_scene.return_characters():
                                character.update()

                            # dialog
                            if cutscene.regulations['variants']:
                                if len(self.captured_text) > 1:
                                    cutscene.on = int(self.captured_text[1][0])
                                    self.choice_keeper = int(self.captured_text[1][0])
                                else:
                                    cutscene.on = self.choice_keeper
                                cutscene.update()

                            cutscene.step_pos_remember[step] = cutscene.pos_remember

                            for stepp in cutscene.step_pos_remember:
                                if stepp == step:
                                    for sprite in list(cutscene.step_pos_remember[stepp].keys()):
                                                cutscene.update()
                                                sprite.rect.center = sprite.pos
                                                sprite.pos = cutscene.step_pos_remember[stepp][sprite]

                            for step_in_step in cutscene.step_in_steps:
                                cutscene.step_in_step = step_in_step
                                cutscene.player.eat = False
                                if wait(cutscene,1):
                                    cutscene.update()
                                for character in self.cutscene_manager.cut_scene.return_characters():
                                    character.update()


                                # position
                                cutscene.step_in_step_pos_remember[cutscene.step_in_step] = cutscene.pos_remember
                                cutscene.step_pos_remember[step] = cutscene.step_in_step_pos_remember

                                for stepp in cutscene.step_pos_remember:
                                    if stepp == step:
                                        for step_in_stepp in list(cutscene.step_pos_remember[stepp].keys()):
                                            if step_in_stepp==step_in_step:
                                                for sprite in list(cutscene.step_in_step_pos_remember[step_in_stepp].keys()):
                                                    cutscene.update()
                                                    sprite.rect.center = sprite.pos
                                                    sprite.pos=cutscene.step_in_step_pos_remember[step_in_stepp][sprite]

                        self.skip_to_point = not self.skip_to_point
                        self.posed = not self.posed

            pg.display.flip()
            self.clock.tick(FPS)

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_j] and keys[pg.K_z] and keys[pg.K_x] and keys[pg.K_c]:
                    self.captured_text=''
                    self.jumping_through_cutscene()
                if event.key==pg.K_h:
                    self.draw_debag=not self.draw_debag
                if event.key==pg.K_r:
                    self.draw_debag_just_rect=not self.draw_debag_just_rect
                if event.key==pg.K_t:
                    self.draw_tiles=not self.draw_tiles
                if event.key==pg.K_n:
                    self.enumerate_sprites=not self.enumerate_sprites
                if event.key==pg.K_f:
                    hits=pg.sprite.spritecollide(self.player,self.for_eating,False)
                    if hits:
                        if self.player.holding[0]:


                            for spr in self.for_eating:
                                spr.taken=[False,None]
                            self.player.holding=[False,None]
                        else:

                            hits[0].taken[0] = True
                            hits[0].taken[1] = self.player
                            self.player.holding[0] = True
                            self.player.holding[1] = hits[0]
                            self.player.holding[1].type_of_physics['over_the_ground'] = True
                            self.player.holding[1].type_of_physics['on_the_ground'] = False

                    for sp in self.for_colliding_with:
                        hits = pg.sprite.spritecollide(sp, self.characters, False)

                        if hits:
                            if sp not in self.for_eating:
                                self.posed=not self.posed
                                self.menu_for_checkpoint()



                if event.key == pg.K_ESCAPE:
                    pg.mouse.set_visible(True)
                    self.posed=not self.posed
                    self.premenu()


    def menu_for_checkpoint(self):
        click = False
        count = 0
        self.screen.blit(self.dim_screen, (0, 0))
        pg.mouse.set_visible(True)
        saved=False
        deleted=False
        while self.posed:
            second = time.strftime("%S")
            hourr = time.strftime("%H")
            minute = time.strftime("%M")
            surf = pg.Surface((WIDTH / 2, HEIGHT / 2))
            surf.fill(WHITE)
            self.screen.blit(surf, (WIDTH / 4, HEIGHT / 4))
            pg.draw.rect(self.screen,RED,[WIDTH / 4, HEIGHT / 4,WIDTH / 2, HEIGHT / 2],8)
            height = surf.get_height()
            width=surf.get_width()
            # buttons
            if not saved:
                self.wbutton_1.draw_button("SAVE", WIDTH/4+self.wbutton_1.rect.width, height+HEIGHT/4-self.wbutton_1.rect.height*1.5)
                pg.draw.rect(self.screen,BLACK,[WIDTH/4+self.wbutton_1.rect.width, height+HEIGHT/4-self.wbutton_1.rect.height*1.5,100,50],6)
                self.wbutton_2.draw_button("RETURN", width+width/3.5, height+HEIGHT/4-self.wbutton_2.rect.height*1.5)
                pg.draw.rect(self.screen, BLACK,[width+width/3.5, height+HEIGHT/4-self.wbutton_2.rect.height*1.5,100, 50], 6)
            #map_name
            self.draw_text(self.map_name, self.title_font, 40, BLACK, WIDTH/ 2, HEIGHT / 2-height/4, align='center')
            #clock
            sec=self.second_culculation()
            min=self.minutes_culculation()
            hour=self.hour_culculation()
            if not saved:
                self.draw_text("TIME_IN:"+str(hour)+":"+str(min)+":"+str(sec), self.title_font, 20, BLACK, WIDTH/2,HEIGHT/2-height/6, align='center')
                #real time
                self.draw_text("REAL_TIME:" + hourr + ":" + minute + ":" + second, self.title_font, 20, BLACK,WIDTH / 2, HEIGHT / 2 - height / 9, align='center')
            #last update
            data = ' '
            with open(path.join(self.game_folder, CP_FILE), 'r') as f:
                lines = f.readlines()
                for line in lines:
                        splited = line.split(":")
                        for num,el in enumerate(splited[1:5]):
                            data+=el+":"
                data=data[:-1]
            if len(data)>1:
                self.draw_text("LAST UPDATE:"+data,self.title_font, 20,BLACK, WIDTH/2,HEIGHT/2,align='center')
            if not saved:
                self.draw_text("WOULD YOU LIKE ME TO SAVE YOUR PROGRESS?",self.title_font, 25, BLACK,WIDTH/2,HEIGHT/2+60, align='center')
            else:
                self.draw_text("SAVED! :)", self.title_font, 25, BLACK, WIDTH / 2, HEIGHT / 2+60,align='center')
                self.draw_text("PRESS ANY KEY TO CONTINUE", self.title_font, 25, BLACK, WIDTH / 2, HEIGHT / 2+120,align='center')

            mx, my = pg.mouse.get_pos()
            # highlighting without mouse
            if count < 0:
                count = len(self.wbutton_list) - 1
            if count <= len(self.wbutton_list) - 1:
                self.wbutton_list[count].on_button(deleted)
            else:
                count = 0
            # clicks:
            #SAVE
            if self.wbutton_list[0].rect.collidepoint((mx, my)) or count == 0:
                count = 0
                for button in self.wbutton_list:
                    button.off_button()
                if click:
                    pg.mouse.set_visible(False)
                    with open(path.join(self.game_folder, CP_FILE), 'w') as f:
                        self.sec=self.sec_checkpoint
                        self.min=self.min_checkpoint
                        self.hour=self.hour_checkpoint
                        self.check_point = self.which_map
                        f.write(str(self.which_map)+":"+" "+self.map_name+" "+"TIME:"+str(self.hour)+":"+str(self.min)+':'+str(self.sec))
                    saved=True
                    deleted=True
            # DO NOT SAVE
            if self.wbutton_list[1].rect.collidepoint((mx, my)) or count == 1:
                count = 1
                for button in self.wbutton_list:
                    button.off_button()
                if click:
                    pg.mouse.set_visible(False)
                    self.posed = not self.posed
            click = False
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if saved:
                        self.wait_for_key_for_checkpoint()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.posed = not self.posed
                    if event.key == K_RIGHT:
                        count += 1


                    if event.key == K_LEFT:
                        count -= 1


                    if event.key == K_RETURN:
                        click = not click
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = not click
            pg.display.flip()
            self.clock.tick(FPS)

    def wait_for_key_for_checkpoint(self):
        pg.event.wait()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                    self.posed=not self.posed
            pg.display.flip()
            self.clock.tick(60)


    def premenu(self):
        now=pg.time.get_ticks()
        click = False
        count=0
        self.screen.blit(self.dim_screen, (0, 0))
        surf=pg.Surface((WIDTH/4,HEIGHT))
        surf.fill(DARKBLUE)
        self.screen.blit(surf,(0,0))
        while self.posed:
            self.button_1.draw_button("CONTINUE", 50, 100)
            self.button_2.draw_button("MAIN_MENU", 50, 200)
            self.button_3.draw_button("QUIT", 50, 300)
            mx, my = pg.mouse.get_pos()
            # highlighting without mouse
            if count < 0:
                count = len(self.button_list1) - 1
            if count <= len(self.button_list1) - 1:
                self.button_list1[count].on_button()
            else:
                count = 0
            # clicks:
            # CONTINUE
            if self.button_list1[0].rect.collidepoint((mx, my)) or count == 0:
                count = 0
                for button in self.button_list1:
                    button.off_button()
                if click:
                    pg.mouse.set_visible(False)
                    self.posed=not self.posed
            #MAIN_MENU CALL
            if self.button_list1[1].rect.collidepoint((mx, my)) or count == 1:
                count = 1
                for button in self.button_list1:
                    button.off_button()
                if click:
                    pg.mouse.set_visible(False)
                    self.posed = not self.posed
                    self.using_menu=not self.using_menu
                    self.continuee=True
                    self.menu()
            # LEAVE
            if self.button_list1[2].rect.collidepoint((mx, my)) or count == 2:
                count = 2
                for button in self.button_list1:
                    button.off_button()
                if click:
                    with open(path.join(self.game_folder, CP_FILE), 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            splited = line.split(":")
                        if len(lines) == 0:
                            splited = []
                        # empty list in python-False
                        if len(splited) > 1:
                            self.map_name = path.basename(str(self.map_list[self.check_point].tmxdata))
                            self.map_name = path.splitext(self.map_name)[0]
                            with open(path.join(self.game_folder, CP_FILE), 'w') as f:
                                a, b, c = self.hour_checkpoint, self.min_checkpoint, self.sec_checkpoint
                                f.write(str(self.check_point) + ":" + " " + self.map_name + " " + "TIME:" + str(
                                    self.hour) + ":" + str(self.min) + ':' + str(self.sec) + ":" + str(a) + ":" + str(
                                    b) + ":" + str(c)+ ":" +str(self.sounds))
                    self.quit()
            click = False
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key==K_ESCAPE:
                        self.posed = not self.posed
                    if event.key == K_DOWN:
                        cur=0
                        if now-cur>500:
                            cur=now
                            count += 1
                            self.button_list1[count - 1].off_button()

                    if event.key == K_UP:
                        cur=0
                        if now-cur>500:
                            cur=now
                            count -= 1
                            self.button_list1[count + 1].off_button()

                    if event.key == K_RETURN:
                        click = not click
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = not click
            pg.display.flip()
            g.clock.tick(FPS)

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text('Spirit`s Life', self.title_font, 100, WHITE, WIDTH/ 2, HEIGHT / 2, align='center')
        pg.display.flip()
        time.sleep(1)
        self.wait_for_key()
    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        count=0
        while waiting:
            count+=1
            if count%2==0:
                self.draw_text("Press a key to start", self.title_font, 50, WHITE, WIDTH / 2, HEIGHT * 3 / 4,
                           align='center')
            else:
                self.draw_text("Press a key to start", self.title_font, 50, BLACK, WIDTH / 2, HEIGHT * 3 / 4,
                               align='center')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
            pg.display.flip()
            self.clock.tick(5)

    def show_go_screen(self):
        pass


    def flying_things_maker(self,num):
        list_of_them=[]
        for i in range(num):
            list_of_them.append(Main_fire_fly(self,(WIDTH+randint(-WIDTH+30,0),randint(HEIGHT+100,HEIGHT*2))))
        return list_of_them

    def menu(self):
        self.dt = self.clock.tick(FPS) / 1000
        click = False
        if not self.continuee:
            count = 1
            if count==0:
                count=1
            self.button_list = OneList(self.button_listt)

        else:
            count = 0
            self.button_list=[self.button_1,self.button_2,self.button_3,self.button_4,self.button_5]
        #sound
        pg.mixer.music.load(path.join(self.music_folder, MENU))
        if self.sounds:
            pg.mixer.music.play(loops=-1)
        while self.using_menu:
            pg.mouse.set_visible(True)
            self.screen.fill(DARKBLUE)
            self.menu_sprites.draw(self.screen)
            self.menu_sprites.update()

            if not self.continuee:
                self.button_2.draw_button("LAST UPDATE", 50, 200)
                self.button_3.draw_button("NEW GAME", 50, 300)
                self.button_4.draw_button("LEAVE", 50, 400)
                if self.sounds:
                    self.button_5.draw_button("SOUND:on",50, 500)
                else:
                    self.button_5.draw_button("SOUND:off", 50, 500)
            else:
                self.button_1.draw_button("CONTINUE", 50, 100)
                self.button_2.draw_button("LAST UPDATE", 50, 200)
                self.button_3.draw_button("NEW GAME", 50, 300)
                self.button_4.draw_button("LEAVE", 50, 400)
                if self.sounds:
                    self.button_5.draw_button("SOUND:on", 50, 500)
                else:
                    self.button_5.draw_button("SOUND:off", 50, 500)
            mx, my = pg.mouse.get_pos()
            # highlighting without mouse
            if not self.continuee:
                if count < 1:
                    count = len(self.button_list) - 1
            else:
                if count < 0:
                    count = len(self.button_list) - 1
            if count <= len(self.button_list) - 1:
                self.button_list[count].on_button()
            else:
                if not self.continuee:
                    count=1
                else:
                    count = 0
            # clicks:
            #CONTINUE
            if self.button_list[0].rect.collidepoint((mx, my)) or count == 0:
                count = 0
                for button in self.button_list:
                    button.off_button()
                if click:
                    pg.mouse.set_visible(False)
                    self.continuee=not self.continuee
                    self.using_menu=not self.using_menu
                    pg.mixer.music.load(path.join(self.music_folder, CAVE))
                    if self.sounds:
                        pg.mixer.music.play(loops=-1)
            #LAST UPDATE
            if self.button_list[1].rect.collidepoint((mx, my)) or count == 1:
                count = 1
                for button in self.button_list:
                    button.off_button()
                if click:
                    pg.mouse.set_visible(False)
                    self.using_menu=False
                    self.which_map=self.check_point
                    self.map_img = self.map_list[self.which_map].make_map()
                    self.new()
                    self.run()
            # NEW GAME
            if self.button_list[2].rect.collidepoint((mx, my)) or count == 2:
                count = 2
                for button in self.button_list:
                    button.off_button()
                if click:
                    pg.mouse.set_visible(False)
                    with open(path.join(self.game_folder, CP_FILE), 'r+') as f:
                        f.truncate(0)
                        self.check_point=0
                        self.sec = 0
                        self.min = 0
                        self.hour = 0
                        self.min_checkpoint = 0
                        self.sec_checkpoint = 0
                        self.hour_checkpoint = 0
                    self.load_data()
                    self.new()
                    self.run()
            # LEAVE
            if self.button_list[3].rect.collidepoint((mx, my)) or count == 3:
                count = 3
                for button in self.button_list:
                    button.off_button()
                if click:
                    with open(path.join(self.game_folder, CP_FILE), 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            splited = line.split(":")
                        if len(lines)==0:
                            splited=[]
                    # empty list in python-False
                        if len(splited)>1:
                            self.map_name = path.basename(str(self.map_list[self.check_point].tmxdata))
                            self.map_name = path.splitext(self.map_name)[0]
                            with open(path.join(self.game_folder, CP_FILE), 'w') as f:
                                a,b,c=self.hour_checkpoint,self.min_checkpoint,self.sec_checkpoint
                                f.write(str(self.check_point)+":"+" "+self.map_name+" "+"TIME:"+str(self.hour)+":"+str(self.min)+':'+str(self.sec)+":"+str(a)+":"+str(b)+":"+str(c)+":"+str(self.sounds))
                    self.quit()
            #SOUND
            if self.button_list[4].rect.collidepoint((mx, my)) or count == 4:
                count = 4
                for button in self.button_list:
                    button.off_button()
                if click:
                    self.sounds=not self.sounds
                    if self.sounds:
                        pg.mixer.music.play(loops=-1)
                    else:
                        pg.mixer.music.stop()

            click = False
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.posed = not self.posed
                    if event.key == K_DOWN:
                        count += 1
                        self.button_list[count - 1].off_button()

                    if event.key == K_UP:
                        count -= 1
                        self.button_list[count + 1].off_button()

                    if event.key == K_RETURN:
                        click = not click
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = not click
            pg.display.flip()
            self.clock.tick(FPS)


# create the game object
g = Game()
g.show_start_screen()
#menu
g.menu()








