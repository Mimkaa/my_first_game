import math
import random
import pygame as pg
from settings import *
from pathfinding import *
from other_helping_classes import *
from random import uniform,choice
import sprites
import weakref
import inspect
from sprites import Obstacle
from decorational_sprites import Heart
from interactable_objects import Simp_Apple
TILESIZEE=64












def dialogue(cut_scene , phrase,character, *simple_pass,step_in_step=False,time=0):
    cut_scene.regulations["standard_phrase"] = True
    cut_scene.regulations['actual_phrase']=phrase
    cut_scene.regulations['character_name']=character.name
    cut_scene.regulations["name_color"]=character.name_color
    cut_scene.regulations["head"]=character.head
    cut_scene.regulations["rect_for_head"]=character.head.get_rect()
    cut_scene.field_drawing=True
    now = pg.time.get_ticks()
    pressed = pg.key.get_pressed()
    space = pressed[pg.K_SPACE]
    if int(cut_scene.text_counter) < len(cut_scene.text[phrase]) :
        if not space:
            cut_scene.var_for_time = pg.time.get_ticks()
        cut_scene.text_counter += cut_scene.rate_of_text
        cut_scene.skipped_text = False
        if space:
            if wait(cut_scene,250):
                cut_scene.text_counter = len(cut_scene.text[phrase])
    else:
        if space:
            if wait(cut_scene,250):
                cut_scene.skipped_text = True
        if simple_pass:
            if not simple_pass[0]:
                    if cut_scene.skipped_text:
                        cut_scene.text_counter = 0
                        cut_scene.step += 1
                        cut_scene.step_in_step=0
            else:
                if cut_scene.skipped_text:
                    cut_scene.step_in_step = 0
                    cut_scene.cut_scene_running = False
        elif step_in_step:
            cut_scene.time=cut_scene.var_for_time
            #print(f"{now}:{cut_scene.time}")
            if now -cut_scene.time>time:
                cut_scene.time = now
                cut_scene.text_counter = 0
                cut_scene.step_in_step += 1
        else:
            return True






# walk_directions
# finish later(more interesting solution)

# def get_default_args(func):
#     signature = inspect.signature(func)
#     return {
#         k: v.default
#         for k, v in signature.parameters.items()
#         if v.default is not inspect.Parameter.empty
#     }
#
# def set_point_of_rect(fun):
#     def _(*args, **kwargs,):
#         for a, v in zip(fun.__code__.co_varnames, args):
#             if v =="right" or v =="left":
#                 if not get_default_args(fun)["point_of_rect"]:
#                     print("has to be centerx")
#             elif v =="up" or v =="down":
#                 if get_default_args(fun)["point_of_rect"] :
#                     print("has to be centery")
#
#         return fun(*args,**kwargs)
#     return _
# @set_point_of_rect
def move(cut_scene,diraction, character, point, character_speed, next_step=False,step_in_step=False,time=0,point_of_rect=None,animation=True,do_not_turn_off_drawing=False,perceive_space=True,erase_cell_mathced_with_the_chr=True):

    if hasattr(character,"animation"):
            character.animation=animation
    if not do_not_turn_off_drawing:
        cut_scene.field_drawing=False
    now = pg.time.get_ticks()
    if perceive_space:
        pressed = pg.key.get_pressed()
        space = pressed[pg.K_SPACE]
    if diraction=="right" or diraction=="left":
        cut_scene.pos_remember[character] = vec(point, character.pos.y)
        if point_of_rect==None:
            point_of_rect = 'centerx'
    else:
        cut_scene.pos_remember[character] = vec(character.pos.x, point)
        if point_of_rect==None:
            point_of_rect = 'centery'

    if diraction=="right":
        if getattr(character.hit_rect, point_of_rect) < point:
            character.vel.x = character_speed
            character.pos += character.vel * cut_scene.game.dt
            character.hit_rect.center = character.pos
        elif getattr(character.hit_rect, point_of_rect) >= point:
            setattr(character.hit_rect, point_of_rect, point)
            character.pos = vec(character.hit_rect.center)


    elif diraction=="left":
        if getattr(character.hit_rect, point_of_rect) > point:
            character.vel.x = -character_speed
            character.pos += character.vel * cut_scene.game.dt
            character.hit_rect.center = character.pos
        elif getattr(character.hit_rect, point_of_rect) <= point:
            setattr(character.hit_rect, point_of_rect, point)
            character.pos = vec(character.hit_rect.center)

    elif diraction=='down':
        if getattr(character.hit_rect, point_of_rect) < point:
            character.vel.y = character_speed
            character.pos += character.vel * cut_scene.game.dt
            character.hit_rect.center = character.pos
        elif  getattr(character.hit_rect, point_of_rect) >=point:
            setattr(character.hit_rect, point_of_rect, point)
            character.pos = vec(character.hit_rect.center)

        #print(f"{getattr(character.rect, point_of_rect)}:{point}")

    elif diraction=='up':
        if getattr(character.hit_rect, point_of_rect) > point:
            character.vel.y = -character_speed
            character.pos += character.vel * cut_scene.game.dt
            character.hit_rect.center = character.pos
        elif getattr(character.hit_rect, point_of_rect) <= point:
            setattr(character.hit_rect, point_of_rect, point)
            character.pos = vec(character.hit_rect.center)


    if getattr(character.hit_rect, point_of_rect) == point:

        cut_scene.tile_on.clear()
        if next_step:
                cut_scene.field_drawing = True
                cut_scene.step += 1
                cut_scene.step_in_step = 0
                cut_scene.time = now

        elif step_in_step:
            #print(cut_scene.step_in_step)
            if wait(cut_scene,time):
                cut_scene.time = now
                cut_scene.step_in_step += 1
        else:
            return True

    elif perceive_space and space:
        if now - cut_scene.time > 300:
            cut_scene.time = now
            setattr(character.hit_rect, point_of_rect, point)
            character.pos = vec(character.hit_rect.center)







# waiting
def get_time(time,time2,dictt):
    dictt[time]=time2
    return time,dictt

def wait(cut_scene,time):
    dictt={}
    now=pg.time.get_ticks()
    cut_scene.time,dictt=get_time(cut_scene.time, now,dictt)
    res = list(dictt.keys())[0]
    cut_scene.time=res
    if now-cut_scene.time>time:
        cut_scene.time=now
        return True

#distance culculation
def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist
def distance_checker(ch1,x1,y1,ch2,x2,y2):
    dist=math.sqrt((getattr(ch1.rect,x1)-getattr(ch2.rect,x2))**2+((getattr(ch1.rect,y1)-getattr(ch2.rect,y2))**2))
    return dist
#variants to choose
def variants(list,game):
    button_list=[]
    for el in list:
        button_list.append(For_variants(el,game))
    return button_list
def limits(on,button_list):
    if on > len(button_list) - 1:
        on = 0
    if on < 0:
        on = len(button_list) - 1
    return on
def movement(cutscene):
    keys = pg.key.get_pressed()
    if keys[pg.K_DOWN] :
        if wait(cutscene,200):
            cutscene.on+=1
            cutscene.go=False
    elif keys[pg.K_UP]:
        if wait(cutscene,200):
            cutscene.on -= 1
            cutscene.go=False
    elif keys[pg.K_RETURN]:
            cutscene.choice=True


class For_variants:
    def __init__(self,text,game):
        self.text = text
        self.game=game
        self.color=WHITE
    def draw(self,x,y):
        self.x=x
        self.y=y
        self.game.draw_text(self.text, self.game.title_font, 20, self.color, self.x,
                         self.y,
                         align='sw')

    def On(self):
        self.color=PURPLE




class Apple(Simp_Apple,metaclass=Numberton):
    number=1
    def __init__(self,cutscene,game,pos,step=0):

        super().__init__(cutscene,game,pos,step)




#cutscence
class First_Cutscene:
    def __init__(self,game,player,Toyya):
        self.game=game
        self.grid_for_pathfinding = WeightedGrid(self.game.map_rect.width, self.game.map_rect.height)
        self.path={}
        self.pos1=(0,0)
        self.list_of_tiles_centers=[i.tile_rect.center for i in self.game.dict_of_tiles.keys()]
        self.list_of_tiles_not_coord_representation=[tuple([j//TILESIZE for j in i.tile_rect.topleft]) for i in self.game.dict_of_tiles.keys()]
        self.tiles_and_centers_dict=dict(zip(self.list_of_tiles_centers,self.list_of_tiles_not_coord_representation))
        self.grid_for_pathfinding.walls=[sp.tile_on().tup_coords for sp in game.decorations]
        self.end_pathfinding_loop=False
        self.last_vel=vec(0,0)
        #self.grid_for_pathfinding.walls=[( j // self.constant_for_division for j in i) for i in self.grid_for_pathfinding.walls]


        self.tile_on={}

        self.subcription = Subscription( self,self.game, "Press Enter to choose")
        self.subcription1=Subscription( self,self.game, "Press Space to Continue")
        self.name='The first meeting'
        self.all_steps=[]
        self.decisions_on_those_steps=[6,12]
        self.step=0
        self.step_in_step=0
        self.timer=pg.time.get_ticks()
        self.cut_scene_running=True
        self.field_drawing=True
        self.dialog_time=2000
        self.skipped_text=False
        self.var_for_time=0
        self.pos_keeper=0
        # for_variants
        self.button_list=[]
        self.on=0
        self.time=0
        self.choice=False
        self.variant=0
        self.decisions={}
        # if we need to control the player and MPC
        self.player=player
        self.Toyya=Toyya
        self.regulations={"standard_phrase":False,
                          "actual_phrase":'',
                          "variants":False,
                          "character_name":"",
                          "name_color":WHITE,
                          "head":self.Toyya.head,
                          "rect_for_head":self.Toyya.rect_for_head

                          }
        self.pos_remember={}
        self.step_pos_remember={}
        self.step_in_step_pos_remember={}
        self.step_in_steps=[0]
        # Dialogue
        self.text={
            "one":"hi there",
            "two":'who are you?',
            "three":'you look kinda weird',
            "fourth":"how can I call you?",
            "fifth":"Hm...",
            "sixth":"It looks like you are not very speakable",
            'seventh':"ok,anyway...",
            'eighth':"HEY!!! WHAT WAS THAT FOR???",
            "ninth":"WHAT IS YOUR PROBLEM????",
            "tenth":"Ok,maybe you are so angry because I asked your name before I had introduced myself ",
            'eleventh':"It is quite easy to fix",
            "twelve":"My name is Toyya",
            "thirteen":"And my introduction did not make anything better...",
            'fourteen':"OK, what about that then",
            "fifteen":"Hmm,someone likes sweeties here",
            "sixteen":"Look, comparing to this, My taste is terrible, so I do not even deserve an effort",
            "seventeen":"And if you do not eat me, I will give you more of these sweet, juicy, shiny apples",
            "eighteen":"There is an apple tree near my home, so you can eat as much as you wish",
            'nineteen':"So, what do you think?",
            "twenty1":"Good!!! Let's go then",
            "twenty2":"Here we are",
            "twenty3":"The apple tree is on the right,as promised",
            "twenty4":"Enjoy!!!",
            "twenty5":"I need to clean up something inside the house, so please wait for a little while",
            "twenty11": "Good!!! Let's go the...",


            "twenty":"What? Are you afraid or something?",
            "twenty_one":"Hey wait, I have something for you",
            "twenty_two":"Hmm, someone is purchasable here",
            "twenty_three":"Hold on, do not go, here it is",
            "twenty_four":"If you do not run, I will give you more of these sweet, juicy, shiny apples",
        }
        self.text_counter=0
        self.name_ch=True
        self.do_not_show_name=True
        self.rate_of_text=0.7
        self.apple=None
        self.heart=[]
        self.flipped=False
        self.dist=[]





    def find_path(self,home, goal,points_for_home,points_for_goal,constant_for_division):

        path, c = a_star_search(self.grid_for_pathfinding, vec(goal), vec(home))

        return path, c
    def move_to_the_object(self, home,home_speed, goal, *limitation,next_step=False, goal_pos_rectifying_x=(0,'centerx',"centerx"), goal_pos_rectifying_y=(0,'centery',"centery"),
                           step_in_step=False,points_for_home=("centerx","centery"),points_for_goal=("centerx","centery"),animation=True,constant_for_division=64,dist_to_apply_before_an_object=100):
        if hasattr(home,'animation'):
            home.animation=animation
        goall=goal.tile_on().tup_coords
        homee=home.tile_on().tup_coords


        self.path, c = self.find_path(homee, goall,points_for_home,points_for_goal,constant_for_division=constant_for_division)


        if len(limitation)>0 and limitation[0]:
            if len(self.path) > limitation[0]:
                self.pos_remember[home] = vec([i * constant_for_division for i in list(self.path.keys())[limitation[0]]])
        else:
            self.pos_remember[home] = vec([i *constant_for_division for i in list(self.path.keys())[0]])

        # simple variation
        # if vec([int(i) for i in home.pos])!=vec([int(i) for i in goal.pos]):
        # if path[vec2int(pos1)]!=None:
        # pos1 = pos1 + path[vec2int(pos1)]
        # home.rect.center = home.pos
        # home.pos = vec(pos1) * TILESIZE
        # else:
        # cutscene.cut_scene_running=False
        checking_coords2 =goall
        checking_coords=homee
        if distance(goal.hit_rect.centerx,goal.hit_rect.centery,home.hit_rect.centerx,home.hit_rect.centery)<dist_to_apply_before_an_object:
            if limitation and checking_coords:
                for i in range(limitation[0]):
                    if self.path[vec2int(vec(checking_coords))]!=None:
                        checking_coords=checking_coords+self.path[vec2int(vec(checking_coords))]
            if type(checking_coords)==vec:
                checking_coords=vec2int(checking_coords)

        if checking_coords== checking_coords2:
            self.end_pathfinding_loop=True

        proceed=False
        if  not self.end_pathfinding_loop :

                #print(f"{checking_coords}:{checking_coords2}")
                if self.path[checking_coords] == vec(1, 0) and home.allowed_to_fpf:
                    home.allowed_to_fpf=False
                    home.move_right_fp=True
                if not home.allowed_to_fpf and home.move_right_fp:
                    if self.path[checking_coords]!=None:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) + self.path[checking_coords])][0]
                    else:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) )][0]
                    if move(self, "right", home, point , home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):

                            home.allowed_to_fpf=True
                            home.move_right_fp=False

                    # if (i//constant_for_division for i in home.pos) != self.pos1 + self.path[vec2int(self.pos1)]:
                    #
                    #     home.vel.x = home_speed
                    #     home.pos += home.vel * self.game.dt
                    #     home.hit_rect.center = home.pos



                if self.path[checking_coords] == vec(-1, 0) and home.allowed_to_fpf:
                    home.allowed_to_fpf=False
                    home.move_left_fp=True
                if not home.allowed_to_fpf and home.move_left_fp:
                    if self.path[checking_coords]!=None:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) + self.path[checking_coords])][0]
                    else:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) )][0]
                    if move(self, "left", home, point, home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):

                            home.allowed_to_fpf=True
                            home.move_left_fp=False

                    # if (i//constant_for_division for i in home.pos) != self.pos1 + self.path[vec2int(self.pos1)]:
                    #     home.vel.x = -home_speed
                    #     home.pos += home.vel * self.game.dt
                    #     home.hit_rect.center = home.pos



                if self.path[checking_coords] == vec(0, 1) and home.allowed_to_fpf :
                    home.allowed_to_fpf=False
                    home.move_down_fp=True
                if not home.allowed_to_fpf and home.move_down_fp:
                    if self.path[checking_coords]!=None:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) + self.path[checking_coords])][1]
                    else:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) )][1]
                    if move(self, "down", home, point, home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):

                            home.allowed_to_fpf=True
                            home.move_down_fp=False


                    #if (i//constant_for_division for i in home.pos) != self.pos1 + self.path[vec2int(self.pos1)]:
                        # home.vel.y = home_speed
                        # home.pos += home.vel * self.game.dt
                        # home.hit_rect.center = home.pos



                if self.path[checking_coords] == vec(0, -1) and home.allowed_to_fpf:
                    home.allowed_to_fpf=False
                    home.move_up_fp=True
                if not home.allowed_to_fpf and home.move_up_fp:
                    if self.path[checking_coords]!=None:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) + self.path[checking_coords])][1]
                    else:
                        point=self.game.dict_of_tup_coords_cell[vec2int(vec(checking_coords) )][1]
                    if move(self, "up", home, point, home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):
                            home.allowed_to_fpf=True
                            home.move_up_fp=False



                    # if (i//constant_for_division for i in home.pos) != self.pos1 + self.path[vec2int(self.pos1)]:
                    #     home.vel.y = -home_speed
                    #     home.pos += home.vel * self.game.dt
                    #     home.hit_rect.center = home.pos

                if home.vel!=vec(0,0):
                    self.last_vel=home.vel
                home.pos=vec(home.hit_rect.center)
                #home.hit_rect.center=vec2int(home.pos)

        # adjustment to be in the center of a tile in the end


        elif home.hit_rect.center!=self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))]:
            if self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][0]-home.hit_rect.centerx<0 and self.last_vel.x<0 and home.allowed_to_adjust:
                home.allowed_to_adjust=False
                home.move_left_ad=True
            if not home.allowed_to_adjust and home.move_left_ad:
                if move(self,'left',home,self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][0],home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):
                    home.allowed_to_adjust=True
                    home.move_left_ad=False
                    proceed=True

            if self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][0]-home.hit_rect.centerx>0 and self.last_vel.x>0 and home.allowed_to_adjust:
                home.allowed_to_adjust=False
                home.move_right_ad=True
            if not home.allowed_to_adjust and home.move_right_ad:
                if move(self,'right',home,self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][0],home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):
                    home.allowed_to_adjust=True
                    home.move_right_ad=False
                    proceed=True

            if self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][1]-home.hit_rect.centery>0 and self.last_vel.y>0 and home.allowed_to_adjust:
                home.allowed_to_adjust=False
                home.move_down_ad=True
            if not home.allowed_to_adjust and home.move_down_ad:
                if move(self,'down',home,self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][1],home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):
                    home.allowed_to_adjust=True
                    home.move_down_ad=False
                    proceed=True

            elif self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][1]-home.hit_rect.centery<0 and self.last_vel.y<0 and home.allowed_to_adjust:
                home.allowed_to_adjust=False
                home.move_up_ad=True
            if not home.allowed_to_adjust and home.move_up_ad:
                if move(self,'up',home,self.game.dict_of_tup_coords_cell[vec2int(vec(home.tile_on().tup_coords))][1],home_speed,animation=animation,perceive_space=False,erase_cell_mathced_with_the_chr=False):
                    home.allowed_to_adjust=True
                    home.move_up_ad=False
                    proceed=True


        if proceed:

                self.end_pathfinding_loop=False
                if goal_pos_rectifying_x[0] < 0:
                    move(self, "right", home, getattr(goal.hit_rect,goal_pos_rectifying_x[2]) + goal_pos_rectifying_x[0], home_speed,next_step=next_step,
                         step_in_step=step_in_step,point_of_rect=goal_pos_rectifying_x[1],perceive_space=False)

                elif goal_pos_rectifying_x[0] > 0:
                    move(self, "left", home, getattr(goal.hit_rect,goal_pos_rectifying_x[2]) + goal_pos_rectifying_x[0], home_speed,next_step=next_step,
                         step_in_step=step_in_step,point_of_rect=goal_pos_rectifying_x[1],perceive_space=False)

                elif goal_pos_rectifying_y[0] > 0:
                    move(self, "up", home, getattr(goal.hit_rect,goal_pos_rectifying_y[2]) + goal_pos_rectifying_y[0], home_speed,next_step=next_step,
                         step_in_step=step_in_step,point_of_rect=goal_pos_rectifying_y[1],perceive_space=False)


                elif goal_pos_rectifying_y[0] < 0:
                    move(self, "down", home,  getattr(goal.hit_rect,goal_pos_rectifying_y[2]) + goal_pos_rectifying_y[0], home_speed,next_step=next_step,
                         step_in_step=step_in_step,point_of_rect=goal_pos_rectifying_y[1],perceive_space=False)



                else:
                    if next_step :
                        self.step+=1
                        self.step_in_step = 0
                    elif step_in_step:
                        self.step_in_step += 1
                    else:
                        return True


    def return_characters(self):
        return [self.Toyya,self.player]


    def choices(self,list,*end):

        self.button_list = variants(list, self.game)
        self.regulations["variants"] = True
        if not self.choice:
            if self.regulations["variants"]:
                movement(self)
                self.on = limits(self.on, self.button_list)
                self.button_list[self.on].On()
        else:
            if not end:
                self.choice = False
                self.step += 1
                self.on=0
            else:
                self.choice = False
                self.on=0
                self.cut_scene_running=False


    def decision(self,num,check):
        if self.step>num:
            if self.decisions[num] == check:
                return True
            else:
                return False





    def player_turn_left(self):
        self.player.turn_left = True
        self.player.turn_back = False
        self.player.turn_right = False
        self.player.turn_forth = False

    def player_turn_right(self):
        self.player.turn_left = False
        self.player.turn_back = False
        self.player.turn_right = True
        self.player.turn_forth = False

    def player_turn_forth(self):
        self.player.turn_left = False
        self.player.turn_back = False
        self.player.turn_right = False
        self.player.turn_forth = True

    def player_turn_back(self):
        self.player.turn_left = False
        self.player.turn_back = True
        self.player.turn_right = False
        self.player.turn_forth = False

    def Toyya_turn_left(self):
        self.Toyya.turn_left = True
        self.Toyya.turn_back = False
        self.Toyya.turn_right = False
        self.Toyya.turn_forth = False

    def Toyya_turn_right(self):
        self.Toyya.turn_left = False
        self.Toyya.turn_back = False
        self.Toyya.turn_right = True
        self.Toyya.turn_forth = False

    def Toyya_turn_forth(self):
        self.Toyya.turn_left = False
        self.Toyya.turn_back = False
        self.Toyya.turn_right = False
        self.Toyya.turn_forth = True

    def Toyya_turn_back(self):
        self.Toyya.turn_left = False
        self.Toyya.turn_back = True
        self.Toyya.turn_right = False
        self.Toyya.turn_forth = False

    # def create_if_step(self, num, *functions):
    #     for step in functions:
    #         if step not in self.list_to_determine_if_function_was_used:
    #             self.list_to_determine_if_function_was_used.append(step)
    #     if num not in self.all_steps:
    #         self.all_steps.append(num)
    #     if self.step == num:
    #         return True

    def find_the_tile_on(self,obj):
        if obj not in self.tile_on or not self.tile_on[obj]:

            for cell in self.game.dict_of_tiles.keys():
                if pg.Rect.colliderect(obj.hit_rect,cell.tile_rect):
                    self.tile_on[obj]=cell


        return self.tile_on[obj]
    def set_the_offset(self,obj,offset):
        if obj not in self.tile_on:
            self.tile_on[obj]=obj.tile_on().tup_coords
        if offset[0]==0:

            return self.game.dict_of_tup_coords_cell[self.tile_on[obj]][1]+offset[1]*TILESIZE
        elif offset[1]==0:
            return self.game.dict_of_tup_coords_cell[self.tile_on[obj]][0]+offset[0]*TILESIZE

    def update(self):

        self.step_in_steps=[0]
        now=pg.time.get_ticks()
        if self.do_not_show_name:
            self.Toyya.name="..."
        # recording decisions
        if self.regulations["variants"]:
            self.decisions[self.step]=self.on
        #action
        self.regulations["standard_phrase"]=False
        self.regulations["variants"]=False
        if self.step==0:
            self.field_drawing=False
            if self.player.hit_rect.x < self.Toyya.hit_rect.x+100:
                self.Toyya.image = self.game.Toyya_animation[1]

            move(self,"left",self.player,self.set_the_offset(self.player,(-25,0)), PLAYER_SPEED,next_step=True)
        # First cut scene step (dialogue)
        if self.step==1:
            dialogue(self,'one',self.Toyya,False)

        # Second step of cutscene
        if self.step==2:
            move(self,"right",self.player,self.Toyya.rect.centerx,PLAYER_SPEED,next_step=True)
            self.player_turn_back()

        # Third step
        if self.step==3:
            self.player_turn_back()
            dialogue(self,'two',self.Toyya,False)

        # Fourth step
        if self.step==4:
            self.Toyya.image=self.game.Toyya_animation[3]
            dialogue(self,'three',self.Toyya,False)

        # fifth step
        if self.step==5:
            self.Toyya.image=self.game.Toyya_animation[1]
            dialogue(self,'fourth',self.Toyya,False)

        # sixth step
        if self.step==6:
            self.choices(["...",'...',"..."])

        # seventh step
        if self.step==7:
            self.Toyya.image = self.game.Toyya_animation[4]
            dialogue(self,'fifth',self.Toyya,False)

        # eights step
        if self.step==8:
            dialogue(self,'sixth',self.Toyya,False)

        if self.step==9:
            self.Toyya.image = self.game.Toyya_animation[1]
            dialogue(self,"seventh",self.Toyya,False)

        if self.step==10:
            self.Toyya.image = self.game.Toyya_animation[0]
            if now-self.time>300:
                self.Toyya.image = self.game.Toyya_animation[2]
                if now - self.time > 600:
                    self.time = now
                    self.step += 1

        if self.step==11:
            move(self,"down",self.Toyya,self.set_the_offset(self.player,(0,-1)),TOYYA_SPEED,next_step=True)

        if self.step==12:
            self.Toyya.turn_forward = True
            self.choices(['eat her','move back'])

        # diversity
        if self.step>12:
            self.Toyya_turn_forth()
        if self.decision(12,0):
            if self.step==13:
                self.step_in_steps=[0,1,2]
                if self.step_in_step==0:
                    move(self,"up",self.player,self.set_the_offset(self.Toyya,(0,1)),self.player.speed,step_in_step=True)

                    #move(self,"up",self.player,self.Toyya.rect.bottom+self.player.rect.height/2,self.player.speed,step_in_step=True)
                if self.step_in_step==1:
                    self.player.eating()
                    if wait(self,300):
                        self.step_in_step=2
                if self.step_in_step==2:
                            self.Toyya.turn_forward = False
                            self.Toyya.image = self.game.Toyya_animation[5]
                            move(self,"left",self.Toyya, self.set_the_offset(self.player,(-3,0)), TOYYA_SPEED * 4,next_step=True,animation=False)

            if self.step==14:
                now=pg.time.get_ticks()
                self.field_drawing=False
                if now-self.time>500:
                    self.time = now
                    self.Toyya.image = self.game.Toyya_animation[6]
                    self.step+=1

            if self.step==15:
                now = pg.time.get_ticks()
                if now-self.time>200:
                    self.time=now
                    self.field_drawing = True
                self.time=0
                dialogue(self, "eighth",self.Toyya,False)

            if self.step==16:
                self.step_in_steps = [0, 1,2]
                if self.step_in_step == 0:
                    move(self, "up", self.player, self.Toyya.hit_rect.centery, self.player.speed, step_in_step=True)
                if self.step_in_step==1:
                    self.move_to_the_object(self.player,self.player.speed,self.Toyya,1, step_in_step=True)
                if self.step_in_step==2:
                    self.player_turn_left()
                    #if int(distance_checker(self.player,"centerx","centery",self.Toyya,'right','centery'))==TILESIZE/2:
                    self.player.eating()
                    if self.player.rect.left<self.Toyya.rect.right:
                        self.step+=1
                        self.step_in_step=0

            if self.step==17:
                self.step_in_steps = [0, 1, 2,3,4,5]
                if self.step_in_step==0:
                    self.pos_keeper = self.player.rect.centery + TILESIZE*2
                    self.Toyya.image = self.game.Toyya_animation[7]
                    move(self,"down",self.Toyya,self.set_the_offset(self.player,(0,2)),self.Toyya.speed*4,step_in_step=True,animation=False)
                if self.step_in_step==1:
                    if wait(self,800):
                        self.Toyya.image = self.game.Toyya_animation[9]
                        self.step_in_step=2
                if self.step_in_step==2:
                    dialogue(self, "ninth", self.Toyya, step_in_step=True, time=250)
                if self.step_in_step==3:
                    move(self,"left",self.player, self.Toyya.rect.centerx, self.player.speed, step_in_step=True)
                if self.step_in_step==4:
                    self.move_to_the_object( self.player,self.player.speed, self.Toyya,1,step_in_step=True)
                if self.step_in_step==5:
                            self.player.eating()
                            if self.player.rect.bottom>self.Toyya.rect.centery:
                                self.step += 1
                                self.step_in_step=0


            if self.step==18:
                self.step_in_steps = [0, 1]
                if self.step_in_step==0:
                    self.pos_keeper = self.player.rect.centerx + TILESIZE*3
                    self.Toyya.image = self.game.Toyya_animation[5]
                    self.Toyya.image=pg.transform.flip(self.Toyya.image,True,False)
                    move(self,"right",self.Toyya,self.pos_keeper,self.Toyya.speed*4,step_in_step=True,animation=False)
                if self.step_in_step==1:
                    if wait(self,200):
                        self.step_in_step=-2
                        self.step+=1

            if self.step==19:
                self.step_in_steps = [-2,-1,0, 1, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
                self.rate_of_text=0.8
                if self.step_in_step==-2:
                    self.Toyya.image = self.game.Toyya_animation[11]
                    if wait(self, 200):
                        self.step_in_step=-1

                if self.step_in_step==-1:
                    self.player_turn_right()
                    if move(self,"down",self.player, self.Toyya.rect.bottom, self.player.speed, point_of_rect='bottom'):
                        self.player_turn_right()
                        if wait(self, 200):
                            self.step_in_step = 0
                if self.step_in_step==0:
                    dialogue(self,'tenth',self.Toyya,False)
                    self.step_in_step=0
            if self.step==20:
                    dialogue(self,'eleventh',self.Toyya,False)
            if self.step==21:
                    self.do_not_show_name=False
                    self.Toyya.name = 'Toyya'
                    dialogue(self, 'twelve', self.Toyya,False)

            if self.step==22:
                if self.step_in_step==0:
                    self.move_to_the_object( self.player,self.player.speed, self.Toyya,1,step_in_step=True)
                if self.step_in_step==1:
                    self.player.eating()
                    if self.player.rect.right>self.Toyya.rect.left:
                        self.step_in_step=2
                if self.step_in_step==2:
                    self.Toyya.image = self.game.Toyya_animation[5]
                    self.Toyya.image = pg.transform.flip(self.Toyya.image, True, False)
                    move(self,"right",self.Toyya,self.set_the_offset(self.player,(3,0)),TOYYA_SPEED*4,step_in_step=True,animation=False)
                if self.step_in_step==3:
                        if wait(self,800):
                                self.step_in_step=4
                if self.step_in_step==4:
                    self.Toyya.image=self.game.Toyya_animation[11]
                    self.Toyya.rect.bottom = self.player.rect.bottom
                    dialogue(self,'thirteen',self.Toyya,False)

            if self.step==23:
                    dialogue(self,'fourteen',self.Toyya,False)
            if self.step==24:
                if self.step_in_step==0:
                    self.apple = Apple(self, self.game, (self.Toyya.rect.centerx,self.Toyya.rect.centery + 7 + self.game.for_eating.sprites()[0].hit_rect.height))
                    self.apple[0].frontal=True
                    if wait(self, 1000):
                        self.apple[0].stop=False
                        self.step_in_step=1
                if self.step_in_step == 1:

                    if self.apple[0].var_for_flight and self.apple[0].vel==vec(0,0):
                        self.apple[0].type_of_physics={"on_the_ground":False,
                              "over_the_ground":True
                              }
                        self.apple[0].vel.x=-300*self.game.dt
                        self.apple[0].vel.y = -600*self.game.dt
                    if  self.player.hit_rect.right > self.apple[0].hit_rect.left-20 and self.apple in self.game.for_eating:
                        self.apple[0].frontal=False
                        self.player.eating()
                        if pg.sprite.spritecollide(self.player, self.game.for_eating, False):
                            if self.player.rect.centery < self.apple[0].rect.top:
                                self.apple[0].kill()
                                Apple.clear()
                    if not self.apple in self.game.for_eating:
                                self.step_in_step = 2
                if self.step_in_step==2:
                    if self.apple not in self.game.all_sprites:
                        self.step_in_step=3
                if self.step_in_step==3:
                    if not self.heart:
                        self.heart=[Heart(self,self.game) for i in range(3)]
                    if wait(self,500):
                        self.step_in_step=4
                if self.step_in_step==4:
                    self.Toyya.image = self.game.Toyya_animation[12]
                    dialogue(self,"fifteen",self.Toyya,False)

            if self.step==25:
                    self.Toyya.image = self.game.Toyya_animation[11]
                    dialogue(self, "sixteen", self.Toyya,False)
            if self.step==26:
                    dialogue(self, "seventeen", self.Toyya,False)
            if self.step==27:
                    dialogue(self, "eighteen", self.Toyya,False)
            if self.step==28:
                    dialogue(self,'nineteen',self.Toyya,False)
            if self.step==29:

                if self.step_in_step==0:
                    for num,heart in enumerate(self.heart):
                        self.heart[num].kill()

                    if self.heart not in self.game.all_sprites:
                        self.step_in_step=1
                if self.step_in_step==1:

                    self.choices(['accept the invitation','still eat her'])


            if self.decision(29,0):
                if self.step==30:
                    self.Toyya.image = self.game.Toyya_animation[14]
                    dialogue(self, 'twenty1', self.Toyya, False)
                if self.step==31:
                    if len(self.dist)<1:
                        dist=distance(self.Toyya.hit_rect.centerx,self.Toyya.hit_rect.centery,self.player.hit_rect.centerx,self.player.hit_rect.centery)
                        self.dist.append(dist)

                    #move(self,"left",self.Toyya,self.game.T_hause.rect.centerx,self.Toyya.speed*2,False)
                    self.Toyya.animation=True
                    self.move_to_the_object(self.Toyya, self.player.speed, self.game.T_hause,4, next_step=True,constant_for_division=64,points_for_goal=('centerx','bottom'),dist_to_apply_before_an_object=self.game.T_hause.rect.height)
                    if distance(self.Toyya.hit_rect.centerx,self.Toyya.hit_rect.centery,self.player.hit_rect.centerx,self.player.hit_rect.centery)>self.dist[0]:
                        self.move_to_the_object(self.player,self.player.speed, self.Toyya,constant_for_division=64)


                if self.step==32:
                    self.Toyya_turn_forth()
                    self.player_turn_back()
                    move(self, "left", self.player, self.Toyya.rect.centerx, self.player.speed)
                    dialogue(self, 'twenty2', self.Toyya, False)
                if self.step==33:
                    self.Toyya_turn_right()
                    dialogue(self, 'twenty3', self.Toyya, False)
                if self.step==34:
                    self.Toyya_turn_forth()
                    dialogue(self, 'twenty4', self.Toyya, False)
                if self.step==35:
                    self.Toyya.do_not_change_the_image=True
                    self.Toyya.image = self.game.Toyya_animation[13]
                    dialogue(self, 'twenty5', self.Toyya, False)
                if self.step==36:
                    self.game.T_hause.image = self.game.Toyya_Hause_animation[1]
                    if move(self,'up',self.Toyya,self.game.T_hause.rect.bottom-10,self.Toyya.speed,point_of_rect='bottom'):
                        self.game.T_hause.image = self.game.Toyya_Hause_animation[0]
                        self.step+=1
                if self.step==37:
                    self.cut_scene_running=False
            elif self.decision(29,1):
                if self.step == 30:
                    self.Toyya.image = self.game.Toyya_animation[14]
                    dialogue(self, 'twenty11', self.Toyya)
                    move(self, "right", self.player, self.Toyya.rect.left - self.player.rect.width - 5,
                         self.player.speed // 2.5, next_step=True, do_not_turn_off_drawing=True)

                if self.step == 31:
                    self.field_drawing = False
                    self.player.eating()
                    if pg.Rect.colliderect(self.player.rect, self.Toyya.rect):
                        self.Toyya.kill()
                        self.cut_scene_running = False





        if self.decision(12,1):
            if self.step==13:
                #print(f"{self.Toyya.rect.bottom}:{self.player.rect.bottom}")
                self.step_in_steps=[i for i in range(15)]
                if self.step_in_step==0:
                    move(self,"down",self.player,self.set_the_offset(self.player,(0,3)),self.player.speed,step_in_step=True)
                if self.step_in_step==1:
                    self.player_turn_back()
                    self.step_in_step=2
                if self.step_in_step==2:
                    dialogue(self,"twenty",self.Toyya,False)
            if self.step==14:
                if self.step_in_step==0:
                    move(self,"left",self.player,self.set_the_offset(self.Toyya,(-10,0)),self.player.speed)
                    if self.Toyya.pos.x-self.player.pos.x>50:
                            if move(self,"down",self.Toyya,self.player.rect.bottom,self.Toyya.speed,point_of_rect="bottom"):
                                self.Toyya.do_not_change_the_image=True
                                self.Toyya.image=self.Toyya.image = self.game.Toyya_animation[11]
                                dialogue(self,"twenty_one",self.Toyya,step_in_step=True,time=500)
                if self.step_in_step==1:
                    self.player_turn_right()
                    if wait(self,500):
                        self.step_in_step=2
                if self.step_in_step==2:
                    self.Toyya.image = self.game.Toyya_animation[12]
                    dialogue(self, "twenty_two", self.Toyya,False)
            if self.step==15:
                if self.step_in_step==0:
                    self.player_turn_left()
                    move(self,"left", self.player, self.set_the_offset(self.player,(-3,0)), self.player.speed,step_in_step=True)
                if self.step_in_step==1:
                    if self.Toyya.pos.x - self.player.pos.x > TILESIZE * 11:
                        self.Toyya.image = self.Toyya.image = self.game.Toyya_animation[11]
                        dialogue(self,"twenty_three",self.Toyya,False)
            if self.step==16:
                if self.step_in_step==0:
                    self.player_turn_right()
                    self.apple = Apple(self, self.game, (self.Toyya.rect.centerx , self.Toyya.rect.centery + 7+self.game.for_eating.sprites()[0].hit_rect.height),
                                       step=9)
                    self.apple[0].frontal = True
                    if wait(self,1000):
                        self.step_in_step=1
                if self.step_in_step==1:
                    move(self,"right",self.player,self.set_the_offset(self.Toyya,(-3,0)),self.player.speed,step_in_step=True)
                    self.apple[0].frontal = True
                if self.step_in_step==2:

                    if self.apple[0].var_for_flight and self.apple[0].vel == vec(0, 0):
                        self.apple[0].type_of_physics = {"on_the_ground": False,
                                                         "over_the_ground": True
                                                         }
                        self.apple[0].vel.x = -300 * self.game.dt
                        self.apple[0].vel.y = -550 * self.game.dt
                    if self.player.rect.right > self.apple[0].rect.left - 20 and self.apple in self.game.for_eating:
                        self.player.eating()
                        if pg.sprite.spritecollide(self.player, self.game.for_eating, False):
                            if self.player.rect.centery < self.apple[0].rect.top:
                                self.apple[0].kill()
                                Apple.clear()
                    if self.apple not in self.game.all_sprites:
                        self.step_in_step = 3

                if self.step_in_step==3:
                    if not self.heart:
                        self.heart=[Heart(self,self.game) for i in range(3)]
                    if wait(self,200):
                        self.step_in_step=4
                if self.step_in_step==4:
                    self.Toyya.image = self.game.Toyya_animation[12]
                    dialogue(self, "fifteen", self.Toyya, False)
            if self.step==17:
                    self.Toyya.image = self.game.Toyya_animation[11]
                    dialogue(self, "twenty_four", self.Toyya,False)
            if self.step==18:
                    dialogue(self, "eighteen", self.Toyya, False)
            if self.step==19:
                    dialogue(self, 'nineteen', self.Toyya, False)
            if self.step==20:
                for num, heart in enumerate(self.heart):
                    self.heart[num].kill()

                self.choices(['accept the invitation', 'eat her'])
            if self.decision(20,0):
                if self.step==21:
                    self.Toyya.image = self.game.Toyya_animation[14]
                    dialogue(self, 'twenty1', self.Toyya, False)
                    if len(self.dist) < 1:
                        dist = distance(self.Toyya.rect.centerx, self.Toyya.rect.centery,
                                        self.player.rect.centerx, self.player.rect.centery)
                        self.dist.append(dist)
                if self.step == 22:
                    self.Toyya.do_not_change_the_image = False

                    # move(self,"left",self.Toyya,self.game.T_hause.rect.centerx,self.Toyya.speed*2,False)
                    self.Toyya.animation = True
                    self.move_to_the_object(self.Toyya, self.player.speed, self.game.T_hause,4,points_for_goal=('centerx', 'bottom'), next_step=True)
                    if distance(self.Toyya.rect.centerx, self.Toyya.rect.centery, self.player.rect.centerx,self.player.rect.centery) > self.dist[0]+100:
                        self.move_to_the_object(self.player, self.player.speed, self.Toyya, 2)


                if self.step == 23:
                    self.Toyya_turn_forth()
                    self.player_turn_back()
                    move(self, "left", self.player, self.Toyya.rect.centerx, self.player.speed)
                    dialogue(self, 'twenty2', self.Toyya, False)
                if self.step == 24:
                    self.Toyya_turn_right()
                    dialogue(self, 'twenty3', self.Toyya, False)
                if self.step == 25:
                    self.Toyya_turn_forth()
                    dialogue(self, 'twenty4', self.Toyya, False)
                if self.step == 26:
                    self.Toyya.do_not_change_the_image = True
                    self.Toyya.image = self.game.Toyya_animation[13]
                    dialogue(self, 'twenty5', self.Toyya, False)
                if self.step == 27:
                    self.game.T_hause.image = self.game.Toyya_Hause_animation[1]
                    if move(self, 'up', self.Toyya, self.game.T_hause.rect.bottom - 10, self.Toyya.speed,
                            point_of_rect='bottom'):
                        self.game.T_hause.image = self.game.Toyya_Hause_animation[0]
                        self.step += 1
                if self.step == 28:
                    self.cut_scene_running = False
            elif self.decision(20,1):
                if self.step==21:
                    self.Toyya.image=self.game.Toyya_animation[14]
                    dialogue(self,'twenty11',self.Toyya)
                    move(self,"right",self.player,self.Toyya.rect.left-self.player.rect.width-5,self.player.speed//2.5,next_step=True,do_not_turn_off_drawing=True)

                if self.step==22:
                    self.field_drawing=False
                    self.player.eating()
                    if pg.Rect.colliderect(self.player.rect, self.Toyya.rect):
                        self.Toyya.kill()
                        self.cut_scene_running=False




        return self.cut_scene_running








    def draw(self):

        if self.field_drawing :
            if not self.regulations["variants"]:
                self.regulations['rect_for_head'].center=(self.regulations['rect_for_head'].width/2+20,(HEIGHT*3)/4+self.regulations['rect_for_head'].height/2+20)
                self.game.screen.blit(self.regulations['head'],self.regulations['rect_for_head'])
            else:
                self.regulations['rect_for_head'].centery=HEIGHT*0.8
                self.regulations['rect_for_head'].centerx=self.regulations['rect_for_head'].width/10
            self.character_name=self.game.draw_text(self.regulations['character_name']+":", self.game.title_font, 30, self.regulations['name_color'],
                            self.regulations['rect_for_head'].right,  self.regulations['rect_for_head'].top+self.regulations['rect_for_head'].width/2, align='sw')

        if self.regulations['standard_phrase'] :
                self.standart_draw(self.regulations["actual_phrase"])
                self.subcription1.update(self.regulations['variants'],self.step_in_steps,self.step_in_step)



        if self.regulations['variants']:
            self.regulations['character_name']=self.player.name
            self.regulations["name_color"]=self.player.name_color
            self.draw_variants()
            self.subcription.update(self.regulations['standard_phrase'],self.step_in_steps,self.step_in_step)






    def standart_draw(self,number):
        if self.field_drawing:
            self.game.draw_text(self.text[number][0:int(self.text_counter)], self.game.title_font, 20, WHITE,
                            self.character_name.right+5, self.character_name.y + self.character_name.height,
                            align='sw')
    def draw_variants(self):
        if self.field_drawing:
            point = self.character_name.y + self.character_name.height
            for button in self.button_list:
                button.draw(self.character_name.right + 10, point)
                point += 50

        return True


class Subscription:
    def __init__(self,cutscene,game,text):
        self.text=text
        self.time=0
        self.game=game
        self.cutscene=cutscene
        self.stopper=False
    def update(self,var,step_in_steps,step_in_step):
        pressed = pg.key.get_pressed()
        space = pressed[pg.K_SPACE]
        enter = pressed[pg.K_RETURN]
        if  space or enter :
            self.stopper = False
        if not var and step_in_steps[-1] == step_in_step:
            if wait(self.cutscene,5000):
                self.stopper=True
            if self.stopper :
                self.game.draw_text(self.text, self.game.title_font, 20, WHITE,
                                WIDTH / 2, HEIGHT - 40, align='center')

class CutSceneManager:

    def __init__(self, game):
        self.game=game
        self.cut_scenes_complete = []
        self.cut_scene = None
        self.keep_track_of_cutscenes=[]
        self.cut_scene_running = False

        # Drawing variables
        self.window_size = 0

    def start_cut_scene(self, cut_scene):
        if cut_scene.name not in self.cut_scenes_complete:
            self.cut_scenes_complete.append(cut_scene.name)
            self.cut_scene = cut_scene
            self.keep_track_of_cutscenes.append(self.cut_scene)
            self.cut_scene_running = True

    def end_cut_scene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self):

        if self.cut_scene_running:
            if self.window_size < self.game.screen.get_height() * 0.3 and self.cut_scene.field_drawing:
                self.window_size += 6
            self.cut_scene_running = self.cut_scene.update()
        else:
            self.end_cut_scene()

    def draw(self):
        if self.cut_scene_running:
            # Draw rect generic to all cut scenes
            if self.cut_scene.field_drawing:
                pg.draw.rect(self.game.screen, DARKGREY, (0, HEIGHT-HEIGHT/4, self.game.screen.get_width(), self.window_size))
            # Draw specific cut scene details
            self.cut_scene.draw()


