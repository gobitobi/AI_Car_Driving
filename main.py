import pygame
import sys
from PIL import Image
import numpy as np
import math

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def check_collision(car, background):
    bounding_box = car.get_bounding_box()
    
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
    car = Car()
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

class Car:
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.x = 500
        self.y = 570
        self.width = 25
        self.height = 60
        self.color = (0, 0, 255)
        self.direction = 0  # 0 = up, 1 = right, 2 = down, 3 = left
        self.speed = 5
        self.angle = 90
        self.screen = screen

        # Create a surface for the car
        self.original_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.original_surface, self.color, (0, 0, self.width, self.height))

    def draw(self, screen):
        rotated_surface = pygame.transform.rotate(self.original_surface, self.angle)
        
        # Get the rect of the rotated surface and set its center
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        
        # Draw the rotated surface on the screen
        screen.blit(rotated_surface, rotated_rect.topleft)

    def rotate(self, angle):
        # Update the angle
        self.angle += angle
        # Keep the angle between 0 and 360 degrees
        self.angle %= 360

    def move(self):
        # Convert angle to radians
        radian_angle = math.radians(self.angle)
        
        # Calculate x and y components of movement
        # Note: We use -sin and -cos here because Pygame's y-axis is inverted
        # and we want 0 degrees to point upwards
        dx = self.speed * -math.sin(radian_angle)
        dy = self.speed * -math.cos(radian_angle)
        
        # Update position
        self.x += dx
        self.y += dy

        # Keep the car within the screen bounds
        self.x = max(0, min(self.x, self.screen.get_width()))
        self.y = max(0, min(self.y, self.screen.get_height()))

    def get_bounding_box(self):
        rotated_surface = pygame.transform.rotate(self.original_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        return rotated_rect

class Background:
    def __init__(self, image_path="track.png"):
        self.image_path = image_path
        self.bg = pygame.image.load(self.image_path)
        self.bg_arr = self.convert_image_to_array()
        self.bg_arr_norm = self.bg_arr / 255

    def convert_image_to_array(self):
        im = Image.open(self.image_path, 'r')
        mode = 'RGB'
        if im.mode != mode:
            im = im.convert(mode)

        width, height = im.size
        pixel_values = list(im.getdata())
        pixel_values = np.array(pixel_values).reshape((height, width, 3))
        return pixel_values

    def is_white(self, x, y):
        color = self.get_color(x, y)
        return np.all(color > 0.9)

    def get_color(self, x, y):
        x = max(0, min(x, self.bg_arr.shape[1] - 1))
        y = max(0, min(y, self.bg_arr.shape[0] - 1))
        return self.bg_arr_norm[y, x]
    
class Game:

    def __init__(self):
        pass

if __name__ == "__main__":
    print("Running")
    main()