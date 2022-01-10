###
### Creates the file browser for the ant image id.
### Sorted by taxonomy hierarchy. See dataset file system helper for info.
###

#from _typeshed import NoneType
import pygame
#from gui.__main__ import start
from gui.objects.panes.pane import Pane
from gui.objects.buttons.file_browser.main import FBButton
from cuticle_analysis.datasets.data_FS.helper import Helper as FSHelper

class FileBrowser(Pane):
    _cur_dir = None
    _cd_list = []
    _FS_helper = None

    def append_root_btn(self, position):
        cd_arr = self._cur_dir.split("/")
        parent_dir = ""
        for dir in range(len(cd_arr)-1):
            parent_dir += dir + "/"
        parent_node = self._FS_helper.get_node(parent_dir)
        root_btn = FBButton(self, self.surface, (self.pane_size[0], 20), position, parent_node, True)
        self._cd_list.append(root_btn)


    # def update_cd_ls(self, root_item=helper.get_dir(self._cur_dir), start_ind, cur_ind):
    def _update_cd_ls(self, root_item, start_ind, cur_ind = 0):
        if root_item is not None:
            append_cnt = cur_ind - start_ind
            if (append_cnt >= 0) & ((20 * append_cnt) <= self.pane_size['height']):
                position = (self.position[0], (self.position[1] + (20 * append_cnt)))
                if (start_ind == 0) & (cur_ind == 0) & (self._cur_dir is not None):
                    self.append_root_btn(position)
                else:
                    self._cd_list.append(FBButton(self.surface, (self.pane_size['width'], 20), position, root_item))
            self._update_cd_ls(root_item.next, start_ind, cur_ind+1)
        else:
            self.append_root_btn(self.position)


    def update_browser(self, index, new_cd = None):
        ### updates the browser
        #if self._cur_dir != new_cd:
        self._cur_dir = new_cd
        self._cd_list = []
        root_item = self._FS_helper.get_node(self._cur_dir, self._FS_helper.root_taxon)
        self._update_cd_ls(root_item, index)

    def show(self):
        for button in self._cd_list:
            button.show()

    def on_click_recur(self, click_pos, index):
        name = self._cd_list[index].data.name
        result = self._cd_list[index].on_click(lambda: self.update_browser(0, (self._cur_dir + "/" + name)))
        if result == 1:
            self.index = 0
        else:
            self.on_click_recur(self, click_pos, index-1)

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        max_ind = self.index + 20
        if len(self._cd_list) < max_ind:
            max_ind = len(self._cd_list)-1
        self.on_click_recur(mouse_pos, max_ind)
        

    def __init__(self, surface, position, pane_size, data_helper, title=None):
        super().__init__(surface, position, title, pane_size)
        self._cur_dir = None
        self._cd_list = None
        self._FS_helper = FSHelper(data_helper)
        self.index = 0
        self.update_browser(self.index)

