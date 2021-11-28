from gui.const import DFLT_FNT_CLR, PANE_B_FS, PANE_BD_KEY_CLR, PANE_BKG_COLR
from gui.objects.panes import Pane
class SpeciesPane(Pane):
    _content_attrib = None
    _species_taxon = {'subgenus': None, 'genus': None, 'sub-family': None, 'species': None, 'sub-species': None}
    _p_font = super().pygame.font.render('Arial', PANE_B_FS)
    
    def __init__(self, surface, position, title, pane_size, taxon_dict):
        super().__init__(surface, position, title, pane_size)
        self.set_species_taxon(taxon_dict)
        
        
    def set_species_taxon(self, hierarchy, h_name):
        """Sets the value of a species taxonomy."""
        keys = self._species_taxon.keys()
        if hierarchy.lower() in keys:
            self._species_taxon[hierarchy] = h_name
        else:
            raise KeyError(hierarchy + " is not a valid taxon hierarchy.")

    def _set_species_taxon(self, taxon_dict, dict_ind):
        if dict_ind > 0:
            self._set_species_taxon(self, taxon_dict, dict_ind - 1)
        key_name = taxon_dict.keys()[dict_ind].lower()
        self_keys = self._species_taxon.keys()
        if key_name in self_keys:
            self._species_taxon[key_name] = taxon_dict[key_name]
        else:
            raise KeyError(key_name + " is not a valid taxon hierarchy.")

    def set_species_taxon(self, taxon_dict):
        """Sets the value of a species taxonomy."""
        self._set_species_taxon(self, taxon_dict, len(taxon_dict.keys()) - 1)

    def _to_string(self, return_key, index):
        """
        See to_string().
        """
        output = ""
        if index > 0:
            output += self._to_string(return_key, index - 1)
        key = self._species_taxon.keys()[index]
        if return_key == False:
            output += self._species_taxon[key] + "\n"
        else:
            output += key + "\n"
        return output



    def to_string(self, return_key):
        """If return_key is true, it returns string of taxonomy levels.
        Otherwise, it returns the values of the species' taxonomy."""
        return self._to_string(self, return_key, len(self._species_taxon.keys()))

    
    def show(self):
        """Renders the Species pane with information provided."""
        self._content_attrib = super().show()
        h_key_str = self.to_string(True)
        h_val_str = self.to_string(False)
        h_key_text = self._p_font.render(h_key_str, True, PANE_BD_KEY_CLR)
        h_val_text = self._p_font.render(h_val_str, True, DFLT_FNT_CLR)
        super().surface.bilt(h_key_text, (self._content_attrib['position'](0), self._content_attrib['position'](1)))
        super().surface.bilt(h_val_text, ((self._content_attrib['position'](0)+ 50), self._content_attrib['position'](1)))