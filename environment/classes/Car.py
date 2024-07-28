import pygame
import sys
from PIL import Image
import numpy as np
import math

class Car:
    def __init__(self, screen, image_path=None):
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
        # rotated_surface = pygame.transform.rotate(self.original_surface, self.angle)
        rotated_surface = pygame.Surface((self.width-20, self.height-20), pygame.SRCALPHA)
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
        return rotated_rect