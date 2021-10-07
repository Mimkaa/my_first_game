import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2
from settings import *
from functions import image_bottom_height,get_key
from math import acos


def sort_vect_length(v):
    return v.length()

class Mob(pg.sprite.Sprite):
    def __init__(self,game,pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game=game
        self.wander_ring_distance=150
        self.wander_ring_radius = 50
        self.flee_distance=250
        self.max_force=0.4
        self.max_speed=300*self.game.dt
        self.image = self.game.rabbit_image[0]
        self.rect = self.image.get_rect()

        self.start_width, self.wall_height, self.wall_width = image_bottom_height(self.image, 0.7)
        self.hit_rect=pg.Rect((self.rect.left + self.start_width, self.rect.bottom - self.wall_height,
                             self.wall_width, self.wall_height))

        self.pos = vec(pos)
        self.vel = vec(self.max_speed, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.hit_rect.center = self.pos
        self.rect.bottom=self.hit_rect.bottom
        self.rect.centerx=self.hit_rect.centerx
        self.last_update = 0
        self.target = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self._layer = self.rect.bottom
        self.stop=False
        self.last_stop=0
        self.fleeing=False
        self.time_between_frames=100
        self.current_frame=0
        self.walking=True
        self.vec_pointing_right=vec(1,0)
        self.vel_buff=vec(0,0)
        self.angle_buff=0
        self.dict_of_animations={tuple(self.game.rabbit_move_forward):False,
                                tuple(self.game.rabbit_move_backward):False,
                                 tuple(self.game.rabbit_move_left):False,
                                 tuple(self.game.rabbit_move_right):False
                                 }
        self.objects_to_avoid=[i for i in self.game.characters ].append([i for i in self.game.decorations])

    def seek(self, target):
        self.desired = (target - self.pos)
        self.desired.normalize_ip()
        if not self.stop:
            self.desired *=self.max_speed

        steer = (self.desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer

    def wander_improved(self):
        future = self.pos + self.vel.normalize() * self.wander_ring_distance
        target = future + vec(self.wander_ring_radius, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)
    def check_if_near_a_character(self):
        for ch in self.game.characters:
            if (self.pos-ch.pos).length()<self.flee_distance:
                return ch

    def flee(self, list_of_targets):
        dict_of_dist={}
        steer = vec(0, 0)
        for target in list_of_targets:

                distt = self.pos - target.pos
                dict_of_dist[target]=distt
        dist=sorted(dict_of_dist.values(),key=sort_vect_length,reverse=False)[0]
        if  not self.check_if_near_a_character():
            target=get_key(dist,dict_of_dist)
        else:
            target=self.check_if_near_a_character()
        if target in self.game.decorations :
            flee_distance=75
        else:
            flee_distance=self.flee_distance
        if dist.length() < flee_distance:
            self.fleeing=True
            self.desired = (self.pos - target.pos).normalize() * self.max_speed
        else:
            self.fleeing=False
            self.desired = self.vel.normalize() * self.max_speed
        steer = (self.desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer

    def animation(self):
        angle=acos(round((self.vec_pointing_right*self.vel)/(self.vec_pointing_right.length()*self.vel.length()),2))
        angle_in_degrees=(angle*180)/3.14
        now=pg.time.get_ticks()
        if self.vel.y!=0 and self.vel.length()>1 or self.vel.x!=0 and self.vel.length()>1:
            self.walking=True
        else:

            self.walking=False

        if self.walking:

                if now - self.last_update > self.time_between_frames:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(RABBIT_MOVE_FORWARD)
                    if self.vel.y>0 and angle_in_degrees>60 and angle_in_degrees<120:
                        self.image = self.game.rabbit_move_forward[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.dict_of_animations={tuple(self.game.rabbit_move_forward):True,
                                tuple(self.game.rabbit_move_backward):False,
                                 tuple(self.game.rabbit_move_left):False,
                                 tuple(self.game.rabbit_move_right):False
                                 }
                    elif self.vel.y<0 and angle_in_degrees>60 and angle_in_degrees<120:
                        self.image = self.game.rabbit_move_backward[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.dict_of_animations={tuple(self.game.rabbit_move_forward):False,
                                tuple(self.game.rabbit_move_backward):True,
                                 tuple(self.game.rabbit_move_left):False,
                                 tuple(self.game.rabbit_move_right):False
                                 }
                    elif self.vel.x<0:
                        self.image = self.game.rabbit_move_left[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.dict_of_animations={tuple(self.game.rabbit_move_forward):False,
                                tuple(self.game.rabbit_move_backward):False,
                                 tuple(self.game.rabbit_move_left):True,
                                 tuple(self.game.rabbit_move_right):False
                                 }
                    elif self.vel.x>0:
                        self.image = self.game.rabbit_move_right[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.dict_of_animations={tuple(self.game.rabbit_move_forward):False,
                                tuple(self.game.rabbit_move_backward):False,
                                tuple(self.game.rabbit_move_left):False,
                                 tuple(self.game.rabbit_move_right):True
                                 }
        else:
            for key,value in self.dict_of_animations.items():
                if value:
                    self.image=key[0]


    def update(self):
        self.animation()
        now=pg.time.get_ticks()
        if now- self.last_stop>randint(500,2000):
            self.last_stop=now
            self.stop=not self.stop

        list=[sp for sp in self.game.all_sprites if sp not in self.game.list_of_mobs]
        self.acc=self.flee(list)

        if not self.fleeing :

            self.acc = self.wander_improved()


        # equations of motion
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        if self.vel.length()>1:
            self.pos += self.vel
        if self.game.which_map!=2:
            if self.pos.x > self.game.map_rect.right:
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = self.game.map_rect.right
            if self.pos.y > self.game.map_rect.bottom:
                self.pos.y = 0
            if self.pos.y < 0:
                self.pos.y = self.game.map_rect.bottom
        else:
            if self.pos.x > self.game.map_rect.right-7*TILESIZE:
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = self.game.map_rect.right-7*TILESIZE
            if self.pos.y > self.game.map_rect.bottom:
                self.pos.y = 0
            if self.pos.y < 0:
                self.pos.y = self.game.map_rect.bottom
        self.hit_rect.center = self.pos
        self.rect.bottom=self.hit_rect.bottom
        self.rect.centerx=self.hit_rect.centerx