import pygame as pg
from tile_map import*
from settings import *
from sprites import*
import pytweening as tween
from random import choice,randrange,uniform
from interactable_objects import Simp_Apple
from random import randint, uniform,choice
from functions import image_bottom_height
from PIL import *
vec=pg.math.Vector2

# one more piece of a shit code
#def find_coords_of_pixel_with_this_color(color,image):

    #for x in range(image.get_size()[0]):
        #for y in range(image.get_size()[1]):
            #r, g, b = image.get_at((x, y))[:3]
            #if (r, g, b) == color:
                #return x,y

def change_size_with_the_same_quality(surf,var):
    changed_surf=pg.transform.scale(surf,(int(surf.get_width()*var),int(surf.get_height()*var)))
    return changed_surf




class Parent_Decoration(pg.sprite.Sprite):
    def __init__(self,pos,game,image,having_bottom,groups,point_of_rect="center",set_layer=()):
        self.groups=game.decorations,groups
        super().__init__(self.groups)
        self.pos=vec(pos)
        self.game=game
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.__setattr__(point_of_rect,pos)

        self.current_frame = 0
        self.last_update = 0
        if set_layer:
            if set_layer[0]:
                self._layer = set_layer[1]

        else:
            self._layer = self.rect.bottom
        if having_bottom[0]:
            self.start_width, self.wall_height, self.wall_width = image_bottom_height(self.image,having_bottom[1])
            self.wall = Obstacle(self.game, self.rect.left + self.start_width, self.rect.bottom - self.wall_height,
                             self.wall_width, self.wall_height)
            self.hit_rect=self.wall.rect
        else:
            self.hit_rect=self.rect


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

class Mashroom(Parent_Decoration):
    def __init__(self,game,pos):
        self.have_bottom=[True,0.7]
        super().__init__(pos,game,game.mashroom_animation[0],self.have_bottom,game.all_sprites)


    def update(self):
        now=pg.time.get_ticks()
        if now-self.last_update>2000:
            self.last_update=now
            self.current_frame = (self.current_frame + 1) % len(MASHROOM)
            self.image = self.game.mashroom_animation[self.current_frame]

class Abyss(Parent_Decoration):
    def __init__(self,game,pos,w,h):
        self.image=game.abyss_animation[0]
        self.img_width = int(w)
        self.img_height = int(h)
        self.image=pg.transform.scale(self.image,(self.img_width,self.img_height))
        self.have_bottom=[False]
        super().__init__(pos,game,self.image,self.have_bottom,(game.others))

    def update(self):
        now=pg.time.get_ticks()
        if now-self.last_update>200:
            self.last_update=now
            self.current_frame = (self.current_frame + 1) % len(ABBYSS_ANIMATION)
            self.image = self.game.abyss_animation[self.current_frame]
            self.image=pg.transform.scale(self.image,(self.img_width,self.img_height))

class Firefly(Parent_Decoration):
    def __init__(self, game, pos):
        self.image = game.firefly_animation[0]
        self.have_bottom=[False]
        self.not_changing_layer=True
        super().__init__(pos, game, self.image, self.have_bottom,(game.all_sprites,game.fireflys,game.for_reflecting))
        self.my_images=[image for image in game.firefly_animation]

        self.tween=tween.easeInOutSine
        self.step=0
        self.dir=1
        self.vel=randrange(50,200)
        self.num=1
        self.num = uniform(0.25,1.25)
        for num, img in enumerate(self.my_images):
            self.my_images[num] = (pg.transform.scale(self.my_images[num],
                                                      (int(self.rect.width / self.num),
                                                       int(self.rect.height / self.num))))
        self.original_width=self.rect.width
    def update(self):
        self.check()
        self.animate()
        self.pos.x-= self.vel*self.game.dt
        self.rect.centerx=self.pos.x
        self.hit_rect.centerx=self.pos.x
        #bobing motion
        offset=BOB_RANGE*(self.tween(self.step/BOB_RANGE)-0.5)
        self.rect.centery=self.pos.y+offset*self.dir
        self.hit_rect.centery = self.pos.y + offset * self.dir
        self.step+=BOB_SPEED
        if self.step>BOB_RANGE:
            self.step=0
            self.dir*=-1



        hits=pg.sprite.spritecollide(self,self.game.moving_and_invisible,False)
        if hits:
            self.pos.x+=3
    def check(self):
        if self.rect.right<0:
            self.stop = True
            self.vel = randrange(50, 200)
            self.num=uniform(0.65,3)
            self.pos.x=self.game.map_rect.right
            self.my_images=[change_size_with_the_same_quality(image,self.num) for image in self.game.firefly_animation]



    def animate(self):

            #self.my_images=[image for image in self.game.firefly_animation]
        now = pg.time.get_ticks()
        if now - self.last_update > 400:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(FIREFLY_ANIMATION)
            self.image = self.my_images[self.current_frame]
            self.rect = self.image.get_rect()
            self.hit_rect = self.rect



class Flower(Parent_Decoration):
    def __init__(self, game, pos,w,h):
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.flower_animation[0]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.have_bottom=[True,0.9]
        super().__init__(pos, game, self.image, self.have_bottom,game.all_sprites)
        self.current_frame = 0
        self.last_update = 0
        self.last_update2=0
        self.wait=False
        self.rewind=False

    def update(self):
        now = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self, self.game.fireflys, False)
        if not self.wait and self.rewind:
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame - 1) % len(FLOWER_ANIMATION)
                bottom = self.rect.bottom
                right = self.rect.right
                self.image = self.game.flower_animation[self.current_frame]
                self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.right = right
            if self.current_frame == 0:
                self.rewind = False
        if hits and not self.wait and not self.rewind :
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(FLOWER_ANIMATION)
                bottom = self.rect.bottom
                right=self.rect.right
                self.image = self.game.flower_animation[self.current_frame]
                self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
                self.rect = self.image.get_rect()
                self.rect.bottom=bottom
                self.rect.right = right
        if  self.current_frame == 5:
                    self.wait=True
                    now2 = pg.time.get_ticks()
                    if now2-self.last_update2 >5000:
                        self.last_update2=now2
                        self.wait=False
                        self.rewind=True


class CaveGrass(Parent_Decoration):
    def __init__(self, game, pos):
        self.image = game.grass_animation[0]
        self.have_bottom=[False]
        super().__init__(pos, game, self.image, self.have_bottom,(game.others),point_of_rect="topleft")
    def update(self):

        hits= pg.sprite.spritecollide(self, self.game.moving_and_invisible, False)
        if hits:
            self.image = self.game.grass_animation[1]
        else:
            self.image = self.game.grass_animation[0]

class CaveGrassUp(Parent_Decoration):
    def __init__(self, game, pos):
        self.image = game.grass_animation[0]
        self.have_bottom = [False]
        self.not_changing_layer = True
        super().__init__(pos, game, self.image, self.have_bottom, (game.all_sprites,game.not_for_reflection), point_of_rect="topleft",set_layer=(self.not_changing_layer,DECORATION_LAYER3))
    def update(self):

        hits = pg.sprite.spritecollide(self, self.game.moving_and_invisible, False)
        if hits:
            self.image = self.game.grass_animation[1]
        else:
            self.image = self.game.grass_animation[0]



class Ordinary_Grass(pg.sprite.Sprite):
    def __init__(self, game, x,y,w,h):
        self._layer = DECORATION_LAYER1
        self.groups = (game.others)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img_w=w
        self.img_h=h
        self.image = game.ordinary_grass[0]
        self.image=pg.transform.scale(self.image,(int(self.img_w),int(self.img_h)))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pose=vec(x,y)
        self.rect.topleft= self.pose
        self.last_update = 0
        self.current_frame = 0
    def update(self):

        hits= pg.sprite.spritecollide(self, self.game.moving_and_invisible, False)
        if hits:
            self.image = self.game.ordinary_grass[1]
            self.image = pg.transform.scale(self.image, (int(self.img_w), int(self.img_h)))
        else:
            self.image = self.game.ordinary_grass[0]
            self.image = pg.transform.scale(self.image, (int(self.img_w), int(self.img_h)))
    def get_layer(self):
        return self._layer

class Wind(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self._layer = WALL_LAYER
        self.groups =  game.moving_and_invisible
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.hit_rect=self.rect
        self.rect.x = x
        self.rect.y = y
        self.x=x
    def update(self):
        self.rect.x+=WIND_SPEED*self.game.dt
        if self.rect.x>=self.game.map_rect.right:
            self.rect.x=0
# water
class Water(Parent_Decoration):
    def __init__(self, game, x, y,w,h):

        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.water_animation[0]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.pose = vec(x, y)
        self.have_bottom=[False]
        self.not_changing_layer = True
        super().__init__(self.pose, game, self.image, self.have_bottom, (game.all_sprites),
                         point_of_rect="topleft", set_layer=(self.not_changing_layer, DECORATION_LAYER2))
    def update(self):
        self.image = self.game.water_animation[0]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.game.camera.update_for_water(self)
        hits=pg.sprite.spritecollide(self,self.game.all_sprites,False)
        if hits:
            self.image.blit(self.game.water_animation[0], self.game.camera.apply_rect(self.game.map_rect))
            for sprite in self.game.all_sprites:
                if sprite not in self.game.others and sprite not in self.game.not_for_reflection or sprite  in self.game.for_reflecting  :
                    self.image.blit(pg.transform.rotate(pg.transform.flip(sprite.image, True, False), 180),
                                    self.game.camera.apply_for_water(sprite))
    def get_layer(self):
        return self._layer

class Wave(Parent_Decoration):
    def __init__(self, game, x, y, w, h):
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = pg.Surface((64,64),pg.SRCALPHA)# SRCALPHA makes objeckt transperent
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.pose = vec(x, y)
        self.have_bottom=[False]
        self.not_changing_layer=True
        super().__init__(self.pose, game, self.image, self.have_bottom, (game.all_sprites),
                         point_of_rect="topleft", set_layer=(self.not_changing_layer, DECORATION_LAYER3))
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.moving_and_invisible, False)
        if hits:
            self.image=self.game.water_animation[2]
        else:
            self.image = pg.Surface((64, 64), pg.SRCALPHA)
    def get_layer(self):
        return self._layer


class Interpolation(Parent_Decoration):
    def __init__(self, game, x, y, w, h):
        self.img_width = int(w)
        self.img_height = int(h)
        self.image=game.water_animation[4]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.pose = vec(x, y)
        self.have_bottom=[False]
        self.not_changing_layer=True
        super().__init__(self.pose, game, self.image, self.have_bottom, (game.all_sprites,game.not_for_reflection),
                         point_of_rect="topleft", set_layer=(self.not_changing_layer, DECORATION_LAYER4))
    def get_layer(self):
        return self._layer


class Tree(Parent_Decoration):
    def __init__(self, game, pos, w, h):
        self.game = game
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.tree_animation[0]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.have_bottom=[False]
        super().__init__(pos, game, self.image, self.have_bottom,(game.all_sprites,game.for_reflecting))
    def update(self):
        now=pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self, self.game.moving_and_invisible, False)
        if hits:
            if now-self.last_update>300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(TREE_ANIMATION)
                self.image=self.game.tree_animation[self.current_frame]
                self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        else:
            self.image = self.game.tree_animation[0]
            self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))

class Crystal(Parent_Decoration):
    def __init__(self, game,pos, w, h):
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.crystal_animation[0]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.have_bottom=[True,0.9]
        super().__init__(pos, game, self.image, self.have_bottom,game.all_sprites)
        self.last_update = 0
        self.current_frame = 0
        self.last_update2 = 0
        self.wait = False
        self.rewind = False
    def update(self):
        now = pg.time.get_ticks()
        hits = pg.sprite.spritecollide(self, self.game.fireflys, False)
        if not self.wait and self.rewind:
            if now - self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame - 1) % len(CRYSRAL_ANIMATION)
                self.image = self.game.crystal_animation[self.current_frame]
                self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
            if self.current_frame == 0:
                self.rewind = False
        if hits and not self.wait and not self.rewind:
            if now - self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(CRYSRAL_ANIMATION)
                self.image = self.game.crystal_animation[self.current_frame]
                self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        if self.current_frame == 5:
            self.wait = True
            now2 = pg.time.get_ticks()
            if now2 - self.last_update2 > 5000:
                self.last_update2 = now2
                self.wait = False
                self.rewind = True

class Wall_Interpolation(Parent_Decoration):
    def __init__(self, game, x, y,w,h,v):
        if v==1:
            self.image=game.wall_images[0]
        if v==2:
            self.image = game.wall_images[1]
        if v==3:
            self.image = game.wall_images[2]
        self.image=pg.transform.scale(self.image,(int(w),int(h)))
        self.pos=(x,y)
        self.have_bottom=[False]
        super().__init__(self.pos, game, self.image, self.have_bottom, (game.all_sprites, game.not_for_reflection),
                         point_of_rect="topleft")

# 3 map
class Pine(Parent_Decoration):
    def __init__(self, game, pos, w, h):
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.pine[0]
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.have_bottom=[True,0.96]
        super().__init__(pos, game, self.image, self.have_bottom,(game.all_sprites,game.decorations),)

class Toyya_Hause(Parent_Decoration):
    def __init__(self, game, pos, w, h):
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.Toyya_Hause
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.have_bottom=[False]
        super().__init__(pos, game, self.image, self.have_bottom,game.all_sprites)


class AppleTree(Parent_Decoration):
    def __init__(self, game, pos, w, h):
        self.img_width = int(w)
        self.img_height = int(h)
        self.image = game.AppleTree
        self.image = pg.transform.scale(self.image, (self.img_width, self.img_height))
        self.have_bottom = [True,0.90]
        super().__init__(pos, game, self.image, self.have_bottom,(game.all_sprites,game.matched_with_for_eating))
        self.apples=[Simp_Apple(self, self.game, (uniform(self.rect.centerx+self.rect.width/3,self.rect.centerx-self.rect.width/3), uniform(self.rect.centery-self.rect.height/2.5,self.rect.centery-self.rect.height/6)),i) for i in range(randint(5,10))]
        for sprite in self.apples:
            hits = pg.sprite.spritecollide(sprite, self.game.for_eating, False)
            if len(hits) > 2:
                self.game.all_sprites.change_layer(sprite, self._layer - 1)
            sprite.stop=True
            sprite.type_of_physics = {"on_the_ground": False,
                                    "over_the_ground": True

                                    }
        self.time=0
        self.additional_list_to_keep_track_of_which_are_down=self.apples[:]
        self.apple_choice=self.apples[0]
        # jumping managing
        self.jumped=False
        self.dict_of_bottoms={}
        self.list_of_landed=[]
        for sprite in self.apples:
                self.dict_of_bottoms[sprite]=choice([self.rect.bottom+self.rect.height/4,self.rect.bottom+self.rect.height/5,self.rect.bottom+self.rect.height/6,self.rect.bottom-self.rect.height/4,self.rect.bottom-self.rect.height/5,self.rect.bottom-self.rect.height/6])
    def update(self):
        for sprite in self.apples:
                if sprite.type_of_physics['on_the_ground']:
                    self.list_of_landed.append(sprite)
                if self.dict_of_bottoms[sprite]>self.rect.bottom and sprite not in self.list_of_landed:
                    sprite.frontal=True
                if  sprite.hit_rect.bottom>self.dict_of_bottoms[sprite] and sprite not in self.list_of_landed:
                        sprite.pos.y = self.dict_of_bottoms[sprite] - sprite.hit_rect.height / 2
                        sprite.vel.y = -sprite.vel.y/3
                        if abs(sprite.vel.y)<1:
                            sprite.type_of_physics = {"on_the_ground": True,
                                                      "over_the_ground": False
                                                      }







        # falling
        hits=pg.sprite.spritecollide(self,self.game.moving_and_invisible,False)
        for apple in self.additional_list_to_keep_track_of_which_are_down:
            if apple.rect.bottom>self.rect.centery:
                self.additional_list_to_keep_track_of_which_are_down.remove(apple)
        if not hits  and self.additional_list_to_keep_track_of_which_are_down:
            self.apple_choice = choice(self.additional_list_to_keep_track_of_which_are_down)
        else:
            if self.apple_choice.rect.bottom<self.rect.centery:
                self.apple_choice.stop=False







class Heart(pg.sprite.Sprite):
    def __init__(self,cutscene,game):
        self.frontal=True
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.cutscene = cutscene
        self.var = uniform(0.5, 1)
        self.player=cutscene.player
        self.game=game
        self.vel=vec(0,0)
        self.pos = vec(uniform(cutscene.player.rect.centerx + 15, cutscene.player.rect.centerx - 15),
                       uniform(cutscene.player.rect.centery + 15, cutscene.player.rect.centery - 15))
        self.picture=game.heart
        self.image=game.heart
        self.rect=self.image.get_rect()
        self.hit_rect=self.rect
        self.image_copy=self.image
        self.image = change_size_with_the_same_quality(self.picture,self.var)
        self.rect=self.image.get_rect()
        self.hit_rect = self.rect
    def update(self):
        self.acc = vec(0, -21*self.game.dt)
        self.acc += self.vel* (-10*self.game.dt)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        if self.pos.y<self.cutscene.player.rect.top-75:
            self.var = uniform(0.5, 1)
            self.image=change_size_with_the_same_quality(self.picture,self.var)
            self.rect=self.image.get_rect()
            self.hit_rect = self.rect
            self.pos=vec(uniform(self.cutscene.player.rect.centerx+15,self.cutscene.player.rect.centerx-15), uniform(self.cutscene.player.rect.centery+15,self.cutscene.player.rect.centery-15))
















































