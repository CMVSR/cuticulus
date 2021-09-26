
import pygame

from pygame.locals import HIDDEN, DOUBLEBUF

from cuticle_analysis.datasets import DatasetHelper
from gui.objects.image_viewer import ImageViewer
from gui.objects.buttons.buttons import Buttons
from gui.objects.textbox import Textbox
from gui import const


class Gui:
    # Object constructor
    def __init__(self, surface):
        self.surface = surface
        self.increment_id = False
        self.decrement_id = False

    # Overloaded function from the pygame library that sets caption from surface name which
    # is concatenated with PROGRAM_NAME
    def set_caption(self, surface_name) -> str:
        caption = surface_name + " - " + const.PROGAM_NAME
        pygame.display.set_caption(caption)

    # Returns the surface object.
    def get_surface(self) -> pygame.display:
        return self.surface

    # Sets the surface object.
    def set_surface(self, surface):
        self.surface = surface


def start():
    """
    This file contains the gui functions for the main window.
    The function opens the main window and adds the imageviewer navigation buttons with their corresponding
    event listeners, image id, image, ant's species classification, and the ant's texture classification.
    """
    data = DatasetHelper()
    # Initializes GUI objects and launches window.
    window = pygame.display.set_mode(
        (const.WINDOW_SIZE[0], const.WINDOW_SIZE[1]), HIDDEN)
    main = Gui(window)
    white = (255, 255, 255)
    main.get_surface().fill(white)
    pygame.mouse.set_visible(1)
    body_font = pygame.font.SysFont('Arial', const.BODY_FONT_SIZE)
    width = main.get_surface().get_width()
    height = main.get_surface().get_height()
    standby_text_pos = (width/2, height/2)
    standby_text = body_font.render("Loading program...", True, (0, 0, 0))
    main.get_surface().blit(
        standby_text, (standby_text_pos[0], standby_text_pos[1]))
    pygame.display.set_mode(
        (const.WINDOW_SIZE[0], const.WINDOW_SIZE[1]), DOUBLEBUF)
    pygame.display.update()
    prev_bttn_pos = (225, 475)
    next_bttn_pos = (525, 475)
    id_text_pos = ((width/3) + 25, 50)
    id_txtbox_pos = (300, 475)
    id_textbox = Textbox(main.get_surface(), 16, "Enter ID to view image...", None, {
                         "width": 200, "height": 50}, [id_txtbox_pos[0], id_txtbox_pos[1], 50])
    previous_button = Buttons(main.get_surface(), "rectangle", "<", const.BUTTON_COLOR, {
                              "width": 50, "height": 50}, [prev_bttn_pos[0], prev_bttn_pos[1], 50])
    next_button = Buttons(main.get_surface(), "rectangle", ">", const.BUTTON_COLOR, {
                          "width": 50, "height": 50}, [next_bttn_pos[0], next_bttn_pos[1], 50])
    ant_iv = ImageViewer(main.get_surface(), data,
                         'rough_smooth', (225, 100), (350, 350))
    id_text = body_font.render(str(ant_iv.get_image_id()), True, (0, 0, 0))
    main.set_caption(str(ant_iv.get_image_id()) + ".jpg")
    next_button.on_click(lambda: ant_iv.__increment_image__())
    previous_button.on_click(lambda: ant_iv.__decrement_image__())
    ant_iv.__show__()
    previous_button.show()
    next_button.show()
    id_textbox.__show__()
    main.get_surface().blit(id_text, [id_text_pos[0], id_text_pos[1]])
    pygame.display.update()
    # Launch event listener
    is_running = True
    while is_running == True:
        main.set_caption(str(ant_iv.get_image_id()) + ".jpg")
        main.get_surface().fill(white)
        previous_button = Buttons(main.get_surface(), "rectangle", "<", (200, 200, 200), {
                                  "width": 50, "height": 50}, [prev_bttn_pos[0], prev_bttn_pos[1], 50])
        next_button = Buttons(main.get_surface(), "rectangle", ">", (200, 200, 200), {
                              "width": 50, "height": 50}, [next_bttn_pos[0], next_bttn_pos[1], 50])
        id_text = body_font.render(
            "Image ID: " + str(ant_iv.get_image_id()), True, (0, 0, 0))
        main.get_surface().blit(id_text, [id_text_pos[0], id_text_pos[1]])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                previous_button.set_running_status(is_running)
                ant_iv.__delete_img_cache__()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print()
                else:
                    id_textbox.__update_value__(event.key)
        ant_iv.__update_image__()
        ant_iv.__show__()
        previous_button.show()
        next_button.show()
        id_textbox.__show__()
        ant_iv.__increment_image__()
        ant_iv.__decrement_image__()
        pygame.display.update()
    ant_iv.__delete_img_cache__()


# Temporary check verifying that the window staus is open until user quits.
pygame.init()
start()
