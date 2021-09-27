
import os
import numpy as np

import pygame  # GUI Framework
from PIL import Image as im  # Import library that reads image array

from cuticle_analysis import const


class ImageViewer():
    def __init__(self, surface, image_list, dataset_type, position, size):
        self.surface = surface
        self.id = 1
        self.image_list = image_list
        self.image_arr = im.fromarray(image_list.get_image(self.id, False))
        self.dataset_type = dataset_type
        self.cache_path = f'./dataset/.iv_cache.jpg'
        self.image_arr.save(self.cache_path)
        self.image = pygame.image.load(self.cache_path)
        self.img_size = None
        self.position = position
        self.bkg_color = (50, 50, 50)
        self.bkg_obj = pygame.Rect(position[0], position[1], size[0], size[1])
        self.size = size
        self.increment_flag = False
        self.decrement_flag = False
        self.__color_corrected = False

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

        if self.image_arr is not None:
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

    def __get_increment_flag__(self):
        "Returns the increment id flag for the main thread to increment image id."
        return self.increment_flag

    def __get_decrement_flag__(self):
        "Returns the increment id flag for the main thread to decrement image id."
        return self.decrement_flag

    def __increment_image__(self):
        "Sets the increment id flag for the main thread to increment image id."
        if self.id < 2876:
            self.id = self.id + 1

    def __decrement_image__(self):
        "Sets the decrement id flag for the main thread to decrement image id."
        if self.id > 1:
            self.id -= 1

    #Implement function where image gets split into eight threads to reduce
    #Recursion limit error.
    #def __correct_pixel_color(self, x, y):
     #   if y < 0:
     #       return
     #   elif x < 0 and y >= 0:
     #       self.__correct_pixel_color(len(self.image_arr[0]) - 1, y - 1)
     #   else:
     #       actl_blue = self.image_arr[y][x][0].copy()
     #       self.image_arr[y][x][0] = self.image_arr[y][x][2].copy()
     #       self.image_arr[y][x][2] = actl_blue
     #       self.__correct_pixel_color(x -1 , y)

    def __correct_color__(self):
        """Corrects the color of the image by swapping blue and red color values."""
        self.image_arr = np.array(self.image_arr)
        for y in range(len(self.image_arr)):
            for x in self.image_arr[y]:
                actl_blue = x[0].copy()
                x[0] = x[2].copy()
                x[2] = actl_blue
        self.image_arr = im.fromarray(self.image_arr)

    def __update_image__(self, id=None):
        """
            Updates the image viewer to current image, which is an image cache.
            Post-condition: Ant image is shown in image viewer. If file not found,
            The cache image is deleted and the image viewer shows error.
        """
        #IMPLEMENT FUNCTION THAT OBTAINS THE MAXIMUM IMAGE ID.
        if (id is None) or (id >= 1 and id <= 2876):
            if id is not None:
                self.id = id
            try:
                self.image_arr = im.fromarray(
                    self.image_list.get_image(self.id, False))
                self.__color_corrected = False
                self.__correct_color__()
                self.__color_corrected = True
                self.image_arr.save(self.cache_path)
                self.image = pygame.image.load(self.cache_path)
                return 1
            except ValueError as ve:
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
    
    def get_color_corrected(self):
        return self.__color_corrected