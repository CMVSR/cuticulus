
import pygame

from gui import const as g_const  # GUI Framework
from cuticle_analysis import const


class Pane():
    """Constructor function. 
    Any None type parameters passed will be set to default values."""
    def __init__(self, surface, position, title, pane_size):
        self.surface = surface
        self.position = position
        self.title = title
        self.pane_size = pane_size
        self.h_font = pygame.font.SysFont('Arial', g_const.PANE_H_FS)

    def show(self):
        """Makes the pane visible on GUI surface.
            If the title is not None, then the header is drawn and the pane container is drawn below.
            Once the pane header and/or background is drawn, the attributes of the pane's content is returned.
        """
        if self.title is not None:
            header_rect = pygame.Rect(self.position[0], self.position[1], int(self.pane_size.get("width")), 50) 
            pygame.draw.rect(
                self.surface, g_const.PANE_HEADER_COLR, header_rect
            )
            head_text_object = self.h_font.render(self.title, True, g_const.DFLT_FNT_CLR)
            self.surface.blit(head_text_object, (self.position[0], (self.position[1])))
            content_size = (self.pane_size.get("width"), (self.pane_size.get("height") - g_const.PANE_HEADER_HEIGHT))
            content_position = (self.position[0], (self.position[1] + g_const.PANE_HEADER_HEIGHT))
        else:
            content_size = self.pane_size
            content_position = self.position
        content_rect = pygame.Rect((content_position[0], content_position[1]), content_size)
        pygame.draw.rect(self.surface, g_const.PANE_BKG_COLR, content_rect)
        content_attrib = {'position': content_position, 'size': content_size}
        return content_attrib






