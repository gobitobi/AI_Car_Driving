import pygame
import sys
from PIL import Image
import numpy as np
import math

class Background:
    def __init__(self, image_path="./environment/assets/track.png"):
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