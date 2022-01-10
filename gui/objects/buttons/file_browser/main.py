# Appends buttons to file browser pane.
# See FileBrowser class from module
# gui.objects.panes.file_browser for more info.

#from _typeshed import NoneType
from typing import Type

import pygame
from gui.objects.buttons import buttons
from gui import const

class FBButton(buttons.Buttons):
    data = None
    type_icon_dir = None
    
    def _set_icon_dir(self):
        type = self.data.get_type()
        if type == "directory":
            print()
            # self.type_icon_dir = dir icon
        else:
            if type == "image":
                print()
                # self.type_icon_dir = img icon
            else:
                raise TypeError("Node " + self.data.name + " is an invalid type " + str(type(self.data.data)) + """.
                 The node must either be an image link or a directory.""")

    def show(self):
        width = list(self.size.values())[list(self.size.keys()).index("width")]
        height = list(self.size.values())[list(self.size.keys()).index("height")]
        rect_obj = pygame.Rect(self.position[0], self.position[1], width, height)
        pygame.draw.rect(self.surface, const.TAXON_BTTN_CLR, rect_obj)
        self.surface.blit(self.text_object, self.position)

    def on_click(self, func):
        super().on_click(func)
    
    def __init__(self, surface, size, position, data, is_parent=False):
        self.data = data
        self.surface = surface
        self.size = size
        self.position = position
        self.font = pygame.font.SysFont('Arial', 12)
        if is_parent:
            text_string = ".."
        else:
            text_string = data.name
        text_string = data.name
        self.text_object = self.font.render(text_string, True, (0, 0, 0))
        super().__init__(surface, "rectangle", text_string, const.TAXON_BTTN_CLR, size, position)
        self._set_icon_dir()

