import pygame
import sys
from PIL import Image
import numpy as np
import math
from environment.classes.Car import Car
from environment.classes.Background import Background 

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def check_collision(car, background):
    bounding_box = car.get_bounding_box()
    # print(bounding_box)
    
    # Check corners of the bounding box
    corners = [
        bounding_box.topleft,
        bounding_box.topright,
        bounding_box.bottomleft,
        bounding_box.bottomright
    ]
    
    for corner in corners:
        x, y = int(corner[0]), int(corner[1])
        if background.is_white(x, y):
            print(f"Collision at ({x}, {y}), Color: {background.get_color(x, y)}")
            return True
    
    return False

def main():
    car = Car(screen)
    background = Background()
    background_image = pygame.image.load(background.image_path)
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            car.rotate(3)
        if keys[pygame.K_RIGHT]:
            car.rotate(-3)

        car.move()
        if check_collision(car, background):
            print("Collision detected!")
            # Handle collision (e.g., reset car position, end game, etc.)

        screen.fill((255, 0, 0))
        screen.blit(background_image, (0, 0))
        car.draw(screen)

        pygame.display.flip()




    
class Game:

    def __init__(self):
        pass

if __name__ == "__main__":
    print("Running")
    main()