import pygame as pg
from settings import *
from tile_map import*
from functions import image_bottom_height
from PIL import Image
vec=pg.math.Vector2
import pytweening as tween
import math
def cropping(image):
    raw_str = pg.image.tostring(image, "RGBA", False)
    img = Image.frombytes("RGBA", image.get_size(), raw_str)
    cropped_image=img.crop((0,0,img.width,img.height/1.5))
    image= pg.image.fromstring(cropped_image.tobytes(), cropped_image.size, "RGBA")
    return image

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_hit_rect_reverse(one,two):
    return one.rect.colliderect(two.hit_rect)

def collide_hit_rect_only(one,two):
    return one.hit_rect.colliderect(two.hit_rect)

def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist





def collide_with_objects(sprite,group,dir):
        if dir == 'x':

            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect_only)
            if hits  :
                    if hasattr(hits[0],'vel')  and hits[0] in sprite.game.characters:
                        if hasattr(sprite,"pseudo_vel"):
                            sprite.pseudo_vel.x = hits[0].vel.x



                        if not sprite.taken[0]  and sprite not in sprite.game.for_eating_keep_track :
                            sprite.game.for_eating_keep_track.append(sprite)
                        if hits[0].vel.x > 0  :
                                sprite.pos.x = hits[0].hit_rect.right + sprite.hit_rect.width/2
                        if hits[0].vel.x < 0  :
                                sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.width/2
                        sprite.hit_rect.centerx = sprite.pos.x
                    #mostly with a wall
                    else:
                                    if sprite.vel.x > 0 or hasattr(sprite,'pseudo_vel') and sprite.pseudo_vel.x>0 or hasattr(sprite,'eat') and sprite.eat and sprite.turn_right:
                                        sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.width / 2
                                    if sprite.vel.x < 0 or hasattr(sprite,'pseudo_vel') and sprite.pseudo_vel.x<0 or hasattr(sprite,'eat') and sprite.eat and sprite.turn_left:
                                        sprite.pos.x = hits[0].hit_rect.right + sprite.hit_rect.width / 2
                                    sprite.hit_rect.centerx = sprite.pos.x



        if dir == 'y':
            hits  = pg.sprite.spritecollide(sprite, group, False , collide_hit_rect_only)
            if hits   :
                    if   hasattr(hits[0],'vel')  and hits[0] in sprite.game.characters:
                        if hasattr(sprite, "pseudo_vel"):
                            sprite.pseudo_vel.y = hits[0].vel.y

                        if  not sprite.taken[0] and  sprite not in sprite.game.for_eating_keep_track :
                            sprite.game.for_eating_keep_track.append(sprite)
                        if hits[0].vel.y > 0:#and distance(sprite.hit_rect.centerx,sprite.hit_rect.centery,hits[0].hit_rect.centerx,hits[0].hit_rect.centery)<sprite.hit_rect.height/2 + hits[0].hit_rect.height/2 :
                            sprite.pos.y = hits[0].hit_rect.bottom+sprite.hit_rect.height/2
                        if hits[0].vel.y < 0  :
                            sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.height / 2
                        sprite.hit_rect.centery = sprite.pos.y


                    #mostly with a wall
                    else:
                                    if sprite.vel.y > 0 or hasattr(sprite,'pseudo_vel') and sprite.pseudo_vel.y>0 or hasattr(sprite,'eat') and sprite.eat and sprite.turn_forth:
                                        sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.height/2
                                    if sprite.vel.y < 0 or hasattr(sprite,'pseudo_vel') and sprite.pseudo_vel.y<0 or hasattr(sprite,'eat') and sprite.eat and sprite.turn_back:
                                        sprite.pos.y = hits[0].hit_rect.bottom +sprite.hit_rect.height/2
                                    sprite.hit_rect.centery = sprite.pos.y










class Player(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites,game.for_colliding,game.characters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(self.game.stay_animation[0],(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()

        self.start_width, self.wall_height, self.wall_width = image_bottom_height(self.image, 0.85)
        self.hit_rect = pg.Rect((self.rect.left + self.start_width, self.rect.bottom - self.wall_height,
                                 self.wall_width, self.wall_height))
        self.hit_rect.center=pos
        self.height = self.rect.height
        self.rect.top = self.hit_rect.bottom - self.height
        self.rect.centerx = self.hit_rect.centerx
        self.rect_update=pg.Rect(0,0,WIDTH,HEIGHT)
        self.rect_update.center=self.rect.center
        self.holding=[False,None]
        self.number_taken=0
        #layer
        self._layer = self.rect.bottom

        self.vel = vec(0, 0)
        self.pos = vec(pos)
        self.name="YOU"
        self.name_color=PURPLE
        self.walking=False
        self.current_frame = 0
        self.last_update = 0
        self.turn_back=False
        self.turn_right=False
        self.turn_left=False
        self.turn_forth=True
        self.speed = PLAYER_SPEED
        self.time_between_frames = 100
        # everything for gluttony
        self.eat=False
        self.bottom=self.rect.bottom
        self.left=self.rect.left
        self.right=self.rect.right
        self.top=self.rect.top

        self.loops=0
        self.gluttony_animations=[self.game.player_glattony_left_animation,self.game.player_glattony_right_animation,self.game.player_glattony_forward_animation,self.game.player_glattony_backward_animation]
        self.third_frame_of_gluttony_forward=False
        # pathfinding
        self.allowed_to_fpf=True#fpf- follow the path further
        self.move_right_fp=False
        self.move_left_fp=False
        self.move_up_fp=False
        self.move_down_fp=False

        self.allowed_to_adjust=True
        self.move_right_ad=False
        self.move_left_ad=False
        self.move_up_ad=False
        self.move_down_ad=False

    def get_keys(self):
        self.vel = vec(0, 0)
        if not self.eat and self.game.cutscene_manager.cut_scene==None:
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel.x = -self.speed
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel.x = self.speed
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel.y = -self.speed
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel.y = self.speed
            if keys[pg.K_TAB]  :
                self.current_frame = -1
                self.eating()
            if keys[pg.K_RSHIFT] or keys[pg.K_LSHIFT]:
                self.speed=PLAYER_SPEED+150
                self.time_between_frames = 70
            else:
                self.speed = PLAYER_SPEED
                self.time_between_frames = 100

    def animate(self):
        if self.vel.x<0:
            self.turn_forth = False
            self.turn_back = False
            self.turn_right = False
            self.turn_left = True
        elif self.vel.x>0:
            self.turn_forth = False
            self.turn_back = False
            self.turn_right = True
            self.turn_left = False
        elif self.vel.y>0:
            self.turn_forth = True
            self.turn_back = False
            self.turn_right = False
            self.turn_left = False
        elif self.vel.y<0:
            self.turn_forth = False
            self.turn_back = True
            self.turn_right = False
            self.turn_left = False

        now = pg.time.get_ticks()
        # animation of up, down movement
        if self.vel.y!=0 or self.vel.x!=0:
            self.walking=True
        else:
            self.walking=False

        if self.walking:
            if not self.holding[0]:
                if now - self.last_update > self.time_between_frames:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(PLAYER_MOVE_FORWARD)
                    if self.vel.y>0:
                        self.image=self.game.move_forward_animation[self.current_frame]
                        self.rect=self.image.get_rect()

                    if self.vel.y<0:
                        self.image = self.game.move_back_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.vel.x>0 :
                        self.image = self.game.move_right_animation[self.current_frame]
                        self.rect=self.image.get_rect()

                    if self.vel.x<0 :
                        self.image = self.game.move_left_animation[self.current_frame]
                        self.rect = self.image.get_rect()
            else:
                if now - self.last_update > self.time_between_frames:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(PLAYER_HOLDING_FRONT_GOING_ANIMATION)
                    if self.vel.y>0:
                        self.image = self.game.player_front_going_holding_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.vel.y<0:
                        self.image = self.game.player_back_going_holding_animation [self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.vel.x>0:
                        self.image = self.game.player_right_holding_going_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.vel.x<0:
                        self.image = self.game.player_left_holding_going_animation[self.current_frame]
                        self.rect = self.image.get_rect()


        if not self.eat :
            if not self.holding[0] :
                if not self.walking and  self.turn_back:
                    if now-self.last_update>self.time_between_frames:
                        self.last_update=now
                        self.current_frame=(self.current_frame+1)%len(PLAYER_STAY_BACK)
                        self.image=self.game.stay_animation_back[self.current_frame]
                        self.rect = self.image.get_rect()
                if not self.walking and  self.turn_right:
                    if now-self.last_update>self.time_between_frames:
                        self.last_update=now
                        self.current_frame=(self.current_frame+1)%len(PLAYER_STAY_LEFT)
                        self.image=self.game.stay_right_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                if not self.walking and  self.turn_left:
                    if now-self.last_update>100:
                        self.last_update=now
                        self.current_frame=(self.current_frame+1)%len(PLAYER_STAY_LEFT)
                        self.image=self.game.stay_left_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                if  not self.walking and self.turn_forth:
                    if now-self.last_update>self.time_between_frames:
                        self.last_update=now
                        self.current_frame=(self.current_frame+1)%len(PLAYER_STAY)
                        self.image=self.game.stay_animation[self.current_frame]
                        self.rect = self.image.get_rect()
            elif not self.walking:
                if now - self.last_update > self.time_between_frames:
                    self.last_update = now
                    if self.turn_right:
                        self.current_frame = (self.current_frame + 1) % len(PLAYER_HOLDING_LEFT_ANIMATION)
                        self.image = self.game.player_right_holding_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.turn_left:
                        self.current_frame = (self.current_frame + 1) % len(PLAYER_HOLDING_LEFT_ANIMATION)
                        self.image = self.game.player_left_holding_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.turn_forth:
                        self.current_frame = (self.current_frame + 1) % len(PLAYER_HOLDING_FRONT_ANIMATION)
                        self.image = self.game.player_front_holding_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.turn_back:
                        self.current_frame = (self.current_frame + 1) % len(PLAYER_HOLDING_BACK_ANIMATION)
                        self.image = self.game.player_back_holding_animation[self.current_frame]
                        self.rect = self.image.get_rect()

        #shit-code of eating animation
        if self.eat:
            hits=pg.sprite.spritecollide(self,self.game.all_sprites,False)
            if len(hits)>1 and self.current_frame==3:
                for sprite in hits:
                    if sprite!=self and sprite in self.game.for_eating:
                        sprite.kill()
            self.eating()

    def eating(self):
        if not self.eat:
            self.current_frame = -1
        self.eat=True
        now=pg.time.get_ticks()
        if self.turn_left:
            images=self.game.player_glattony_left_animation
        elif self.turn_right:
            images=self.game.player_glattony_right_animation
        elif self.turn_forth:
            images=self.game.player_glattony_forward_animation
        elif self.turn_back:
            images=self.game.player_glattony_backward_animation
        if self.turn_right or self.turn_left:
            images[2]=pg.transform.scale(images[2],(TILESIZE,int(TILESIZE*1.25)))
            images[3]=pg.transform.scale(images[3], (int(TILESIZE * 1.5),TILESIZE))
            images[4]= pg.transform.scale(images[4], (TILESIZE , TILESIZE))
            images[0:2]=[pg.transform.scale(i,(int(TILESIZE/2)+10, TILESIZE)) for i in images[0:2] ]
        if self.turn_forth or self.turn_back:
            images[2] = pg.transform.scale(images[2],(TILESIZE,int(TILESIZE*1.4)))
            images[3]  = pg.transform.scale(images[3], (TILESIZE,int(TILESIZE * 2)))
            images[4] = pg.transform.scale(images[4], (TILESIZE, int(TILESIZE*1.1)))
            images[0:2] = [pg.transform.scale(i, (TILESIZE, TILESIZE)) for i in images[0:2]]

        if now - self.last_update >self.time_between_frames:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(images)
                self.image =images[self.current_frame]
                if self.image==images[3]:
                    self.third_frame_of_gluttony_forward=True
                self.rect = self.image.get_rect(center=self.pos)

                if self.image == images[0] :
                    self.top = self.rect.top
                    self.bottom = self.rect.bottom
                    self.left=self.rect.left
                    self.right= self.rect.right

                if self.image==images[0]:
                    self.loops+=1
                if self.loops==2 :
                    self.third_frame_of_gluttony_forward=False
                    self.eat=False
                    self.loops=0



    def update(self):
        self.animate()
        self.get_keys()

        self.pos+=self.vel*self.game.dt
        self.collisions()





        self.rect_update.center=self.hit_rect.center




    def collisions(self):
        collide_with_for_eating = pg.sprite.spritecollide(self, self.game.for_eating, False, collide_hit_rect)
        self.hit_rect.centerx = self.pos.x
        collide_with_objects(self, self.game.walls, 'x')
        if len(collide_with_for_eating) > 0 and not collide_with_for_eating[0].allow_in_x_diraction:
            collide_with_objects(self, self.game.for_eating, 'x')

        self.hit_rect.centery = self.pos.y
        collide_with_objects(self, self.game.walls, 'y')
        if len(collide_with_for_eating) > 0 and not collide_with_for_eating[0].allow_in_y_diraction:
            collide_with_objects(self, self.game.for_eating, 'y')
        if not self.eat:

            self.rect.top = self.hit_rect.bottom-self.height
            self.rect.centerx = self.hit_rect.centerx

        elif self.turn_back :
            self.rect.bottom=self.hit_rect.bottom
        elif self.turn_right:
            self.rect.bottom = self.hit_rect.bottom
            self.rect.left=self.hit_rect.left
        elif self.turn_left:
            self.rect.bottom = self.hit_rect.bottom
            self.rect.right=self.hit_rect.right
        elif   self.turn_forth and not self.third_frame_of_gluttony_forward:

                self.rect.bottom = self.hit_rect.bottom
        elif self.third_frame_of_gluttony_forward :
                self.rect.top = self.hit_rect.bottom - self.height


    def get_layer(self):
        return self._layer
    def tile_on(self):
        list=[]
        for cell in self.game.dict_of_tiles.keys():
            if pg.Rect.colliderect(self.hit_rect,cell.tile_rect)  :
                list.append(cell)
        dict={}
        for cell in list:
            dict[cell]=distance(self.hit_rect.centerx, self.hit_rect.centery, cell.tile_rect.centerx, cell.tile_rect.centery)
        keys = [k for k, v in dict.items() if v == min(dict.values())]

        return keys[0]

class Tile:
    def __init__(self,pos):
        self.tile_rect=pg.Rect(pos,(TILESIZE,TILESIZE))
        self.tup_coords=tuple([i//TILESIZE for i in self.tile_rect.topleft])
    def __repr__(self):
        return f"({self.tile_rect.x//TILESIZE},{self.tile_rect.y//TILESIZE})"

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y,):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.hit_rect=self.rect
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self._layer = WALL_LAYER
        self.groups =  game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.hit_rect=self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self._layer = WALL_LAYER
        self.groups =  game.for_changing_location
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.hit_rect=self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Teleport_Back(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self._layer = WALL_LAYER
        self.groups =  game.for_returning
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.hit_rect=self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Check_point(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self.groups =  game.all_sprites,game.for_colliding_with
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size_for_F = 20
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.checkpoint_animation[0]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self._layer = self.rect.bottom
        self.pos = vec(x, y)
        self.rect.topleft = self.pos
        self.last_update = 0
        self.current_frame = 0
        self.step=0
        self.tween = tween.easeInOutSine
        self.dir = 1
    def update(self):
        now=pg.time.get_ticks()
        if now-self.last_update>100:
            self.last_update=now
            self.current_frame = (self.current_frame + 1) % len(CHECKPOINT_ANIMATION)
            self.image=self.game.checkpoint_animation[self.current_frame]
            self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        offset = BOB_RANGE2 * (self.tween(self.step / BOB_RANGE2) - 0.5)
        self.rect.y= self.pos.y + offset * self.dir
        self.hit_rect.y = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step>BOB_RANGE2:
            self.step=0
            self.dir*=-1

    def get_layer(self):
        return self._layer


class Toyya(Player):
    def __init__(self, game, pos):
        super().__init__(game,pos)
        self.name = "Toyya"
        self.name_color = CYAN
        self.head = cropping(self.image)
        self.head = pg.transform.scale(self.head, (self.head.get_width() * 2, self.head.get_height() * 2))
        self.rect_for_head = self.head.get_rect()
        self.image = game.Toyya_animation[0]
        self.rect=self.image.get_rect()
        self.height = self.rect.height
        self.speed=TOYYA_SPEED
        self.animation=True
        self.start_width, self.wall_height, self.wall_width = image_bottom_height(self.image, 0.85)
        self.hit_rect=pg.Rect((self.rect.left + self.start_width, self.rect.bottom - self.wall_height,
                             self.wall_width, self.wall_height))
        self.hit_rect.bottom = self.rect.bottom
        self.hit_rect.centerx = self.rect.centerx
        self.hit_rect.center=self.pos
        self.turn_forth = False
        self.do_not_change_the_image=False
        self.pos_back_up=vec(0,0)
    def animate(self):
        if self.vel.x<0:
            self.turn_forth = False
            self.turn_back = False
            self.turn_right = False
            self.turn_left = True
        elif self.vel.x>0:
            self.turn_forth = False
            self.turn_back = False
            self.turn_right = True
            self.turn_left = False
        elif self.vel.y>0:
            self.turn_forth = True
            self.turn_back = False
            self.turn_right = False
            self.turn_left = False
        elif self.vel.y<0:
            self.turn_forth = False
            self.turn_back = True
            self.turn_right = False
            self.turn_left = False
        now = pg.time.get_ticks()
        if self.vel.y!=0 or self.vel.x!=0:
            self.walking=True
        else:
            self.walking=False
        if self.walking:
            if self.image!=self.game.Toyya_animation[7]:
                if now - self.last_update > 100:
                    self.last_update = now
                    if self.vel.y>0:
                        self.current_frame = (self.current_frame + 1) % len(TOYYA_WALKING_ANIMATION)
                        self.image = self.game.Toyya_walking_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.vel.x<0:
                        self.current_frame = (self.current_frame + 1) % len(TOYYA_WALKING_ANIMATION_LEFT)
                        self.image = self.game.Toyya_move_left_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.vel.y<0:
                        self.current_frame = (self.current_frame + 1) % len(TOYYA_WALKING_ANIMATION_BACK)
                        self.image = self.game.Toyya_move_back_animation[self.current_frame]
                        self.rect = self.image.get_rect()
                    if self.vel.x>0:
                        self.current_frame = (self.current_frame + 1) % len(TOYYA_WALKING_ANIMATION_LEFT)
                        self.image = self.game.Toyya_move_right_animation[self.current_frame]
                        self.rect = self.image.get_rect()
        elif not self.do_not_change_the_image:
            if self.turn_left:
                self.image=self.game.Toyya_move_left_animation[0]
            if self.turn_right:
                self.image = self.game.Toyya_move_right_animation[0]
            if self.turn_back:
                self.image=self.game.Toyya_move_back_animation[0]
            if self.turn_forth:
                self.image=self.game.Toyya_animation[2]
    def update(self):
        self.pos_back_up = self.pos
        self.rect = self.image.get_rect()
        #head update
        self.head = cropping(self.image)
        self.head = pg.transform.scale(self.head, (self.head.get_width() * 2, self.head.get_height() * 2))
        self.rect_for_head = self.head.get_rect()

        if self.animation:
            self.animate()

        # hit_rect_resizing
        self.start_width, self.wall_height, self.wall_width = image_bottom_height(self.image, 0.85)
        self.hit_rect = pg.Rect((self.rect.left + self.start_width, self.rect.bottom - self.wall_height,
                                 self.wall_width, self.wall_height))
        self.height = self.rect.height
        #self.get_keys()
        self.vel=vec(0,0)
        self.pos+=self.vel*self.game.dt
        self.collisions()
        self.rect.top = self.hit_rect.bottom - self.height
        self.rect.centerx = self.hit_rect.centerx





















