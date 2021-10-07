import random
import pygame as pg


PLAYER_IMG = pg.Surface((30, 50))
PLAYER_IMG.fill(pg.Color('dodgerblue1'))
TRIANGLE_IMG = pg.Surface((50, 50), pg.SRCALPHA)
pg.draw.polygon(TRIANGLE_IMG, (240, 120, 0), [(0, 50), (25, 0), (50, 50)])


class Player(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=pos)
        # The sprite will be added to this layer in the LayeredUpdates group.
        self._layer = self.rect.bottom


class Triangle(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = TRIANGLE_IMG
        self.rect = self.image.get_rect(center=pos)
        # The sprite will be added to this layer in the LayeredUpdates group.
        self._layer = self.rect.bottom

def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.LayeredUpdates()
    player = Player((50, 80))
    all_sprites.add(player)
    for _ in range(20):
        all_sprites.add(Triangle((random.randrange(600), random.randrange(440))))

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            player.rect.x += 5
        if keys[pg.K_a]:
            player.rect.x -= 5
        if keys[pg.K_w]:
            player.rect.y -= 5
        if keys[pg.K_s]:
            player.rect.y += 5
        # If any of the wasd keys are pressed, change the layer.
        if any((keys[pg.K_w], keys[pg.K_a], keys[pg.K_s], keys[pg.K_d])):
            # Set the layer of the player sprite to its rect.bottom position.
            all_sprites.change_layer(player, player.rect.bottom)

            all_sprites.update()

            screen.fill((30, 30, 30))
            all_sprites.draw(screen)

            pg.display.flip()
            clock.tick(30)

if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()