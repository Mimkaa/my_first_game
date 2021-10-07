import pygame as pg
from settings import *
from tile_map import*
import sprites
from PIL import Image
vec=pg.math.Vector2
import pytweening as tween

def change_size_with_the_same_quality_rotation(surf,var):
    changed_surf=pg.transform.rotate(surf,var)
    return changed_surf
# apple
class Simp_Apple(pg.sprite.Sprite):
    def __init__(self,cutscene,game,pos,*index,step=0):
        self.groups = game.all_sprites,game.for_eating,game.for_colliding_with
        pg.sprite.Sprite.__init__(self, self.groups)
        if index:
            self.index=index
        # to be taken
        self.size_for_F=15
        self.taken=[False,None]

        self.game=game
        self.image=game.apples[0]
        self.rect=self.image.get_rect()
        self.pos=vec(pos)
        self.picture=game.apples[0]
        self.rect.center=self.pos
        self.hit_rect=pg.Rect(self.rect.left,self.rect.height*0.25,self.rect.width,self.rect.height/2)
        self.hit_rect.center=(self.rect.centerx,self.rect.bottom-self.hit_rect.height/2)
        self._layer = self.rect.bottom
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.step=step
        self.num=0
        self.cutscene=cutscene
        self.var_for_flight=True
        self.stop=True
        self.val_for_rot=0
        self.bouncing_times=0
        self.idle=True
        self.moveable=True
        self.allow_in_x_diraction=True
        self.allow_in_y_diraction=True
        self.pseudo_vel=vec(0,0)
        self.touched=0
        self.can_change_layer=False
        self.frontal=False
        self.figure="circle"
        self.current_frame=0
        self.last_update=0
        self.height = self.rect.height
        self.not_change_layer=False
        self.type_of_physics={"on_the_ground":True,
                              "over_the_ground":False
                              }
        self.bottom_after_being_dropped=99999999
    def update(self):
        self.height = self.rect.height
        if  not self.taken[0] :
            hits = pg.sprite.spritecollide(self, self.game.characters, False)
            if not hits:
                self.allow_in_x_diraction = True
                self.allow_in_y_diraction = True

            hit_with_walls = pg.sprite.spritecollide(self, self.game.walls, False, sprites.collide_hit_rect_only)
            if hit_with_walls and self.pseudo_vel.x!=0:
                self.allow_in_y_diraction=True
                self.allow_in_x_diraction=False
            elif hit_with_walls and self.pseudo_vel.y!=0:
                self.allow_in_y_diraction = False
                self.allow_in_x_diraction = True
            hit_with_eq=pg.sprite.spritecollide(self, self.game.for_eating, False, sprites.collide_hit_rect_only)
            if self in hit_with_eq:
                hit_with_eq.remove(self)
            if len(hit_with_eq)>0 and not hit_with_eq[0].allow_in_y_diraction or len(hit_with_eq)>0 and not hit_with_eq[0].allow_in_x_diraction:
                if  self.pseudo_vel.x != 0:
                    self.allow_in_y_diraction = True
                    self.allow_in_x_diraction = False
                elif  self.pseudo_vel.y != 0:
                    self.allow_in_y_diraction = False
                    self.allow_in_x_diraction = True


            if self.type_of_physics['over_the_ground']:
                if self.hit_rect.bottom>self.bottom_after_being_dropped:
                    self.vel.y=-self.vel.y
                    self.pos.y = self.bottom_after_being_dropped - self.hit_rect.height / 2
                    if abs(self.vel.y) < 1:
                        self.type_of_physics = {"on_the_ground": True,
                                                  "over_the_ground": False}
                if not self.stop:

                    self.acc=vec(0, 21*self.game.dt)

                    self.acc.x += self.vel.x *  -self.game.dt
                    self.vel+=self.acc
                    self.hit_rect.center = self.pos
                    self.rect.bottom = self.hit_rect.bottom
                    self.rect.centerx = self.hit_rect.centerx
                    self.pos+=self.vel+0.5*self.acc






            elif self.type_of_physics['on_the_ground'] :
                if self.acc==vec(0,0):
                    self.stop=False
                self.frontal = False
                self.acc = vec(0, 0)
                self.acc += self.vel * (-10 * self.game.dt)
                self.vel += self.acc
                self.pos += self.vel + 0.5 * self.acc


            self.collisions()


            #rotation

            if self.figure == "circle":
                self.rotation()

        else :
            self.touched=-1
            self.taken_behaviour()
            if not self.taken[1].turn_back:
                self.bottom_after_being_dropped=self.taken[1].hit_rect.bottom+10
            else:
                self.bottom_after_being_dropped = self.taken[1].hit_rect.bottom

    def rotation(self):

            if  self.pseudo_vel.x > 0 :
                self.val_for_rot -= 300 * self.game.dt
                self.image = change_size_with_the_same_quality_rotation(self.picture, self.val_for_rot)
                self.rect = self.image.get_rect(center=self.pos)
                self.rect.bottom = self.hit_rect.bottom
            elif  self.pseudo_vel.x < 0 :
                self.val_for_rot += 300 * self.game.dt
                self.image = change_size_with_the_same_quality_rotation(self.picture, self.val_for_rot)
                self.rect = self.image.get_rect(center=self.pos)
                self.rect.bottom = self.hit_rect.bottom
            elif  self.pseudo_vel.y > 0 :
                now = pg.time.get_ticks()
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(APPLE)
                    self.image = self.game.apples[self.current_frame]
                    self.picture = self.game.apples[self.current_frame]
                    self.rect = self.image.get_rect(center=self.pos)
                    self.rect.bottom = self.hit_rect.bottom
            elif  self.pseudo_vel.y < 0 :
                now = pg.time.get_ticks()
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame - 1) % len(APPLE)
                    self.image = self.game.apples[self.current_frame]
                    self.picture = self.game.apples[self.current_frame]
                    self.rect = self.image.get_rect(center=self.pos)
                    self.rect.bottom = self.hit_rect.bottom



    def taken_behaviour(self):

        self.not_change_layer=True
        if self.taken[1].turn_forth:
            self.pos = vec(self.taken[1].rect.centerx,
                           self.taken[1].rect.centery + self.hit_rect.height)
            #self.game.all_sprites.change_layer(self, self.game.all_sprites.get_layer_of_sprite(self.taken[1]) + 1)
            self.frontal=True
        if self.taken[1].turn_back:
            self.pos = vec(self.taken[1].rect.centerx,
                           self.taken[1].rect.centery + self.hit_rect.height)
            #self.game.all_sprites.change_layer(self, self.game.all_sprites.get_layer_of_sprite(self.taken[1]) - 1)
            self.frontal=False
        if self.taken[1].turn_right:
            self.pos = vec(self.taken[1].hit_rect.right + self.hit_rect.width / 2, self.taken[1].rect.centery + self.hit_rect.height * 1.3)
            #self.game.all_sprites.change_layer(self, self.game.all_sprites.get_layer_of_sprite(self.taken[1]) - 1)
            self.frontal = False
        if self.taken[1].turn_left:
            self.pos = vec(self.taken[1].hit_rect.left - self.hit_rect.width / 2, self.taken[1].rect.centery + self.hit_rect.height * 1.3)
            #self.game.all_sprites.change_layer(self, self.game.all_sprites.get_layer_of_sprite(self.taken[1]) - 1)
            self.frontal = False
        self.hit_rect.center = self.pos
        self.rect.top = self.hit_rect.bottom - self.height
        self.rect.centerx = self.hit_rect.centerx
    def collisions(self):

        self.hit_rect.centerx = self.pos.x
        if self.allow_in_x_diraction:
            self.collide_with_equals('x')
            sprites.collide_with_objects(self, self.game.characters, 'x')
        else:
            sprites.collide_with_objects(self, self.game.walls, 'x')
            group = [i for i in self.game.for_eating]
            group.remove(self)
            hits_with_the_same = pg.sprite.spritecollide(self, group, False, sprites.collide_hit_rect_only)
            if hits_with_the_same and hits_with_the_same[0].touched > self.touched:
                sprites.collide_with_objects(self, group, 'x')


        self.hit_rect.centery = self.pos.y
        if self.allow_in_y_diraction:
            self.collide_with_equals('y')
            sprites.collide_with_objects(self, self.game.characters, 'y')
        else:
            sprites.collide_with_objects(self, self.game.walls, 'y')
            group=[i for i in self.game.for_eating]
            group.remove(self)
            hits_with_the_same=pg.sprite.spritecollide(self,group,False,sprites.collide_hit_rect_only)
            if hits_with_the_same and hits_with_the_same[0].touched>self.touched:
                sprites.collide_with_objects(self, group, 'y')


        self.rect.bottom = self.hit_rect.bottom
        self.rect.centerx = self.hit_rect.centerx

    def throw(self,x=0,jump=0,num=None):
        if num:
            self.num=num
        self.vel.y=jump
        self.vel.x=x
    def get_layer(self):
        return self._layer
    def collide_with_equals(self,dir):
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.for_eating, False, sprites.collide_hit_rect_only)

            if hits:
                if self in hits:
                    hits.remove(self)
                for spr in hits:
                    # if pg.sprite.groupcollide(self.game.characters, self.game.for_eating, False, False) and len(hits)>0  and self not in self.game.for_eating_keep_track_layers  and hits[0].touched < self.touched:
                    #     self.game.for_eating_keep_track_layers[hits[0]]=self
                    if spr.pseudo_vel.y > 0 and spr.touched < self.touched and not spr.taken[0]:
                        self.pos.y = spr.hit_rect.bottom + self.hit_rect.height / 2
                    if spr.pseudo_vel.y < 0 and spr.touched < self.touched :
                        self.pos.y = spr.hit_rect.top - self.hit_rect.height / 2
            self.hit_rect.centery = self.pos.y


        if dir=='x':

            hits = pg.sprite.spritecollide(self, self.game.for_eating, False, sprites.collide_hit_rect_only)



            if hits :
                if self in hits:
                    hits.remove(self)
                for spr in hits:
                    if spr.pseudo_vel.x>0  and spr.touched<self.touched and not spr.taken[0] :
                        self.pos.x = spr.hit_rect.right + self.hit_rect.width / 2
                    if spr.pseudo_vel.x<0  and spr.touched<self.touched and not spr.taken[0] :
                        self.pos.x = spr.hit_rect.left - self.hit_rect.width / 2
                    # if pg.sprite.groupcollide(self.game.characters, self.game.for_eating, False, False) and len(hits) > 0 and self not in self.game.for_eating_keep_track_layers  and hits[0].touched < self.touched:
                    #     self.game.for_eating_keep_track_layers[hits[0]] = self
            self.hit_rect.centerx = self.pos.x



    def __repr__(self):
        return str(self.index)
