import pygame

import lib.util as util
import lib.spotify as spotify
import lib.auth as auth


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

# place images in img/ directory
img = []
for i in util.fetch_images():
    img.append(pygame.image.load(f"img/{i}"))

image_amt = len(img)
image_idx = 0


while auth.request_spotify_access_token() != True:
    pass

print("Client authentication successful!")


while auth.request_user_authorization() != True:
    pass

print("User credentials fetched!")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if flicker:
        screen.blit(img[image_idx], (CENTER[0] - (img[image_idx].get_width() / 2), 
                                     CENTER[1] - (img[image_idx].get_height() / 2)))
        
        image_idx = (image_idx + 1) % image_amt
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
