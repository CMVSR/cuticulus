from gui.const import DFLT_FNT_CLR, PANE_B_FS, PANE_BD_KEY_CLR, PANE_BKG_COLR
from gui.objects.panes.pane import Pane
import pygame
class SpeciesPane(Pane):
    _content_attrib = None
    _species_taxon = {'subgenus': None, 'genus': None, 'subfamily': None, 'species': None, 'sub-species': None}
    _p_font = None
    
    def __init__(self, surface, position, title, pane_size, taxon_dict):
        super().__init__(surface, position, title, pane_size)
        self.set_species_taxon(taxon_dict)
        self._p_font = pygame.font.SysFont('Arial', 16)
        
    def set_species_taxon(self, hierarchy, h_name):
        """Sets the value of a species taxonomy."""
        keys = self._species_taxon.keys()
        if hierarchy.lower() in keys:
            self._species_taxon[hierarchy] = h_name
        else:
            raise KeyError(hierarchy + " is not a valid taxon hierarchy.")

    def _set_species_taxon(self, taxon_dict, dict_ind):
        if dict_ind > 0:
            self._set_species_taxon(taxon_dict, dict_ind - 1)
        key_name = list(taxon_dict.keys())[dict_ind]
        self_keys = list(self._species_taxon.keys())
        if key_name in self_keys:
            self._species_taxon[key_name] = taxon_dict[key_name]
        else:
            raise KeyError(key_name + " is not a valid taxon hierarchy.")

    def set_species_taxon(self, taxon_dict):
        """Sets the value of a species taxonomy."""
        self._set_species_taxon(taxon_dict, len(taxon_dict.keys()) - 1)

    def _append_panes(self, h_key_str, h_val_str, delimiter, index, h_key_list, h_val_list):
        if index > 0:
            self._append_panes(h_key_str, h_val_str, delimiter, index-1, h_key_list, h_val_list)
        self._append_pane(h_key_str, h_val_str, delimiter, index, h_key_list, h_val_list)
        

    def _append_pane(self, h_key_str, h_val_str, delimiter, index, h_key_list = [], h_val_list = []):
        h_key_split = h_key_str.split(delimiter)
        h_val_split = h_val_str.split(delimiter)
        h_key_list.append(self._p_font.render(h_key_split[index], True, PANE_BD_KEY_CLR))
        h_val_list.append(self._p_font.render(h_val_split[index], True, DFLT_FNT_CLR))
    
    def _render_pane(self, h_key_list, h_val_list, index):
        if index > 0:
            self._render_pane(h_key_list, h_val_list, index-1)
        self.surface.blit(h_key_list[index], (self._content_attrib['position'][0], self._content_attrib['position'][1] + (index * 16)))
        self.surface.blit(h_val_list[index], ((self._content_attrib['position'][0] + 120), self._content_attrib['position'][1] + (index * 16)))

    def _render_panes(self, h_key_str, h_val_str):
        h_key_split = h_key_str.split("\n")
        h_val_split = h_val_str.split("\n")
        if len(h_key_split) != len(h_val_split):
            raise KeyError("The number of taxon keys (" + len(h_key_split) +") does not match the number of taxon values (" + len(h_val_split) + ")")
        index = len(h_key_split) - 1
        h_key_list = []
        h_val_list = []
        self._append_panes(h_key_str, h_val_str, '\n', index, h_key_list, h_val_list)
        self._render_pane(h_key_list, h_val_list, len(h_key_list)-1)

        

    def _to_string(self, return_key, index):
        """
        See to_string().
        """
        output = ""
        if index > 0:
            output += self._to_string(return_key, index - 1)
        key = list(self._species_taxon.keys())[index]
        if return_key == False:
            if self._species_taxon[key] is None:
                output += "N/A"
            else:
                output += self._species_taxon[key]
            output += "\n"
        else:
            output += key + "\n"
        return output



    def to_string(self, return_key):
        """If return_key is true, it returns string of taxonomy levels.
        Otherwise, it returns the values of the species' taxonomy."""
        return self._to_string(return_key, len(self._species_taxon.keys())-1)

    
    def show(self):
        """Renders the Species pane with information provided."""
        self._content_attrib = super().show()
        h_key_str = self.to_string(True)
        h_val_str = self.to_string(False)
        self._render_panes(h_key_str, h_val_str)
        #h_key_text = self._p_font.render(h_key_str, True, PANE_BD_KEY_CLR)
        #h_val_text = self._p_font.render(h_val_str, True, DFLT_FNT_CLR)
        #self.surface.blit(h_key_text, (self._content_attrib['position'][0], self._content_attrib['position'][1]))
        #self.surface.blit(h_val_text, ((self._content_attrib['position'][0]+ 50), self._content_attrib['position'][1]))