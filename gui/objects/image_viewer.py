
import os
import numpy as np
import cv2

import pygame  # GUI Framework
from PIL import Image as im  # Import library that reads image array

import const


class ImageViewer():
    def __init__(self, surface, image_list, position, size):
        self.surface = surface
        self.id = 1
        self.image_list = image_list
        self.image_arr = self.image_list.get_image(self.id, False)
        self.cache_path = f'./dataset/.iv_cache.jpg'
        cv2.imwrite(self.cache_path, self.image_arr)
        self.image = pygame.image.load(self.cache_path)
        self.img_size = None
        self.position = position
        self.bkg_color = (50, 50, 50)
        self.bkg_obj = pygame.Rect(position[0], position[1], size[0], size[1])
        self.size = size

    def __scale_image__(self):
        """
            Scales the ant image within the image viewer canvas.
            Pre-condition: The class' image variable must be defined.
            Post-condition: An img-ratio is defined and the image is scaled
            adhering to that ratio.
        """
        img_ratio = None

        if self.image.get_width() > self.image.get_height():
            img_ratio = int(self.image.get_width()/self.image.get_height())
            img_height = self.size[0] * img_ratio
            self.image = pygame.transform.scale(
                self.image, (self.size[0], img_height))
        else:
            img_ratio = int(self.image.get_height()/self.image.get_width())
            img_width = self.size[1] * img_ratio
            self.image = pygame.transform.scale(
                self.image, (img_width, self.size[1]))

    def __show__(self):
        "Sets the image to visible"
        pygame.draw.rect(self.surface, self.bkg_color, self.bkg_obj)

        if self.image is not None:
            self.image = pygame.image.load(self.cache_path)
            self.__scale_image__()
            self.surface.blit(self.image, self.position)
        else:
            body_font = pygame.font.SysFont('Arial', 12)
            cwd = os.getcwd()
            if len(cwd) > 50:
                cwd_folders = cwd.split('/')
                if len(cwd_folders) > 1:
                    cwd = "/" + cwd_folders[1] + "/..."
                else:
                    cwd = cwd[0:10:1] + "..."
            error_text = body_font.render(
                "Could not locate image '" + f'{cwd}/dataset/{self.id}.jpg' + "'.", True, (255, 255, 255))
            self.surface.blit(
                error_text, (self.position[0], self.size[1]/3))

    def __increment_image__(self):
        "Sets the increment id flag for the main thread to increment image id."
        if self.id < 2876:
            self.id = self.id + 1

    def __decrement_image__(self):
        "Sets the decrement id flag for the main thread to decrement image id."
        if self.id > 1:
            self.id -= 1

    def __correct_color__(self):
        """Corrects the color of the image by swapping blue and red color values."""
        #self.image_arr = cv2.imwrite()

    def __update_image__(self, id=None):
        """
            Updates the image viewer to current image, which is an image cache.
            Post-condition: Ant image is shown in image viewer. If file not found,
            The cache image is deleted and the image viewer shows error.
        """
        #IMPLEMENT FUNCTION THAT OBTAINS THE MAXIMUM IMAGE ID.
        if id is None or id >= 1:
            if id is not None:
                self.id = id
            try:
                self.image_arr = self.image_list.get_image(self.id, False)
                #self.__correct_color__()
                #self.image_im.save(self.cache_path)
                cv2.imwrite(self.cache_path, self.image_arr)
                self.image = pygame.image.load(self.cache_path)
                return 0
            except Exception as e:
                self.image_arr = None
                self.__delete_img_cache__()
                return -1
        return 0

    def __delete_img_cache__(self):
        "Deletes the image cache file upon program exit."
        try:
            if os.path.exists(self.cache_path) is True:
                os.remove(self.cache_path)
        except Exception as e:
            print("Cache deleted.")
        self.image = None

    
    def get_image_id(self):
        """Returns the image id."""
        return self.id

    def set_image_id(self, id):
        self.id = id
