
import pygame

from gui import const


class Textbox():
    """
    This class handles textbox objects using the Pygame library.
    label is the default text shwon when value is empty.
    value is the value that user enters into the textbox.
    """

    def __init__(self, surface, font_size, default_label, default_value, size, position):
        self.surface = surface
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.label = default_label
        self.__k_input__ = None
        self.value = default_value
        self.text_object = None
        self.size = size
        self.position = position
        self.function = None
        self.func_param = None
        self.text_color = const.TEXTBOX_LABEL_COLOR
        self.is_running = True
        self.shape_object = pygame.Rect(self.position[0], self.position[1], int(list(size.values())[list(
            size.keys()).index("width")]), int(list(size.values())[list(size.keys()).index("height")]))
        self.keyboard_events = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
                                pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    def __show__(self):
        """Sets textbox visible"""
        pygame.draw.rect(
            self.surface, const.TEXTBOX_BKG_COLOR, self.shape_object)
        if self.value is None:
            self.text_color = const.TEXTBOX_LABEL_COLOR
            self.text_object = self.font.render(
                self.label, True, self.text_color)
        else:
            self.text_color = (0, 0, 0)
            self.text_object = self.font.render(
                str(self.value), True, self.text_color)
        self.surface.blit(self.text_object, (self.position[0], (self.position[1] + int(
            list(self.size.values())[list(self.size.keys()).index("height")]/3))))

    def __to_int__(self, KEY_EVENT, max_events):
        """Converts keyboard input into integers.
        Pre-condition: The input must be a number.
        Post-condition: The integer represenation of input is returned."""
        if max_events > -1:
            if KEY_EVENT == self.keyboard_events[max_events]:
                self.__k_input__ = max_events
                return
            else:
                self.__to_int__(KEY_EVENT, (max_events - 1))

    def __update_value__(self, KEY_EVENT):
        """Updates the textbox on keyboard press.
        Pre-condition: The button must be a number, return key, or backspace key.
        Post-condition: The textbox is updated."""
        try:
            if KEY_EVENT == pygame.K_BACKSPACE:
                self.value = int(self.value / 10)
                if self.value == 0:
                    self.value = None
            else:
                ASCII_0 = 48
                ASCII_9 = 57
                if (KEY_EVENT >= 48) and (KEY_EVENT <= 57):
                    self.__to_int__(KEY_EVENT, 9)
                    if self.value is None:
                        self.value = 0
                    self.value = self.value * 10 + self.__k_input__
        except Exception as e:
            self.value = None

    def __clear_value__(self):
        self.value = None

    def __get_value__(self):
        if self.value is not None:
            return self.value
