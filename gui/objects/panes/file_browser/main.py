###
# Creates the file browser for the ant image id.
# Sorted by taxonomy hierarchy. See dataset file system helper for info.
###

import pygame
from gui.objects.panes.pane import Pane
from gui.objects.buttons.file_browser.main import FBButton
from cuticulus.core.datasets.browser.helper import Helper as FSHelper
from gui import const


class FileBrowser(Pane):

    def get_parent_dir(self, cd=None):
        parent_dir = None
        try:
            if cd is None:
                cd = self._cur_dir
            cd_arr = cd.split('/')
            for dir in range(len(cd_arr)-1):
                if parent_dir is None:
                    parent_dir = cd_arr[dir]
                else:
                    parent_dir += cd_arr[dir]
                if dir < len(cd_arr)-2:
                    parent_dir += '/'
            return parent_dir
        except Exception:
            return None

    def append_root_btn(self, position):
        if self._cur_dir is not None:
            cd_arr = self._cur_dir.split("/")
        else:
            cd_arr = [""]
        parent_dir = None
        for dir in range(len(cd_arr)-1):
            if parent_dir is None:
                parent_dir = cd_arr[dir]
            else:
                parent_dir += cd_arr[dir]
            if dir < len(cd_arr)-2:
                parent_dir += '/'
        parent_node = self._FS_helper.get_node(
            parent_dir, self._FS_helper.root_taxon)
        root_btn = FBButton(
            self.surface,
            {
                'width': self.pane_size['width'],
                'height': 20
            },
            position,
            parent_node,
            True,
        )
        self._cd_list.append(root_btn)

    # def update_cd_ls(self, root_item=helper.get_dir(self._cur_dir), start_ind, cur_ind):

    def _update_cd_ls(self, root_item, start_ind, cur_ind=0):
        if root_item is not None:
            append_cnt = cur_ind - start_ind
            if (append_cnt >= 0) & ((20 * append_cnt) <= self.pane_size['height']):
                position = (self.position[0],
                            self.position[1] + (20 * append_cnt))
                if self.title is not None:
                    position = (position[0], position[1] +
                                const.PANE_HEADER_HEIGHT)
                if (start_ind == 0) & (cur_ind == 0) & (self._cur_dir is not None):
                    self.append_root_btn(position)
                    self._update_cd_ls(root_item, start_ind, cur_ind+1)
                else:
                    self._cd_list.append(FBButton(self.surface, {
                                         'width': self.pane_size['width'], 'height': 20}, position, root_item))
                    self._update_cd_ls(root_item.next, start_ind, cur_ind+1)
        else:
            if (self._cur_dir is not None) and (cur_ind == 0):
                self.append_root_btn(self.position)

    def update_browser(self, index, new_cd=None):
        # updates the browser
        if new_cd is not None:
            cd_ls = new_cd.split('/')
            parent_dir = self.get_parent_dir()
            parent_node = self._FS_helper.get_node(
                parent_dir, self._FS_helper.root_taxon)
            if (len(cd_ls) > 1) and (cd_ls[len(cd_ls)-1] == parent_node.name):
                self._cur_dir = parent_dir
                root_item = parent_node
                self._cd_list = []
                self._update_cd_ls(root_item, index)
                return
        self._cur_dir = new_cd
        self._cd_list = []
        root_item = self._FS_helper.get_node(
            self._cur_dir, self._FS_helper.root_taxon)
        self._update_cd_ls(root_item, index)

    def show(self):
        super().show()
        for button in self._cd_list:
            button.show()

    def on_click_recur(self, click_pos, index, ant_iv=None):
        name = self._cd_list[index].data.name
        if isinstance(name, str):
            if self._cur_dir is None:
                def func(): return self.update_browser(0, (name))
            else:
                def func(): return self.update_browser(0, (self._cur_dir + "/" + name))
        else:
            if isinstance(name, int):
                def func(): return ant_iv.set_image_id(name)
            else:
                raise TypeError("Node type \"" + str(type(name)
                                                     ) + "\" must either be int or str.")
        result = self._cd_list[index].on_click(func)
        if result == 1:
            self.index = 0
        else:
            if index > 0:
                self.on_click_recur(click_pos, index-1, ant_iv)

    def on_click(self, ant_iv=None):
        mouse_pos = pygame.mouse.get_pos()
        max_ind = self.index + 20
        if len(self._cd_list) < max_ind:
            max_ind = len(self._cd_list)-1
        self.on_click_recur(mouse_pos, max_ind, ant_iv)

    def __init__(self, surface, position, pane_size, data_helper, title=None):
        super().__init__(surface, position, title, pane_size)
        self._cur_dir = None
        self._cd_list = None
        self._FS_helper = FSHelper(data_helper)
        self.index = 0
        self.update_browser(self.index)
