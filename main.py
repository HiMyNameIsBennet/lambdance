import pygame

import lib.util as util


# pygame setup
pygame.init()

WIDTH = 800
HEIGHT = 800
CENTER = (WIDTH / 2, HEIGHT / 2)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("λnce")
clock = pygame.time.Clock()
running = True

flicker = True

# place image in img/ directory
img = pygame.image.load("img/image.png")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if flicker:
        screen.blit(img, (CENTER[0] - (img.get_width() / 2), CENTER[1] - (img.get_height() / 2)))
    else:
        screen.fill("black")

    flicker = not flicker


    # RENDER YOUR GAME HERE


    pygame.display.flip()


    # this can be optimized
    bpm = util.fetch_bpm()
    fps = util.bpm_to_fps(bpm)
    #

    clock.tick(fps)


pygame.quit()
