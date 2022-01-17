"""
    Helper class responsible for creating & accessing
    Taxon data file system
"""

#NOTE: root_taxon represents the highest
#level of taxonomy where images are classified.
#Determine which taxonomy level should be root.


#from _typeshed import NoneType
from logging import exception, root
from cv2 import NORMCONV_FILTER
from cuticle_analysis.datasets.data_FS.node import Node

class Helper():
    def sort_dict(self, original_dict):
        sorted_dict = {'subfamily': None, 'genus': None, 'subgenus': None, 'species': None, 'subspecies': None}
        dict_list = list(sorted_dict.keys())
        for taxon in dict_list:
            if taxon in original_dict:
                sorted_dict[taxon] = original_dict[taxon]
        return sorted_dict

    def update_data(self, data_helper):
        index = 1
        for i in range(3000):
            print("Updating data... (" + str(index) + "/" + str(3000) + ")", end='\r')
            dict = data_helper.get_ant_info(index)
            if dict == {}:
                consc_nulls += 1
            else:
                consc_nulls = 0
                dict = self.sort_dict(dict)
                self._add_node(dict, index)
            index += 1
            if consc_nulls > 5:
                break

    def __init__(self, data_helper, root_taxon = None):
        self.root_taxon = root_taxon
        self.update_data(data_helper)

    def _add_node_rec(self, node, dict, dict_ind, img_id):
        if dict_ind < len(list(dict.keys())):
            key = list(dict.keys())[dict_ind]
            while key is None:
                dict_ind += 1
                key = list(dict.keys())[dict_ind]
            if dict[key] is None:
                taxon_name = "[unclassified " + key + "]"
            else:
                taxon_name = dict[key]
            if node is None:
                node = Node(None, None, taxon_name)
                node.data = self._add_node_rec(node.data, dict, dict_ind+1, img_id)
                node.data.set_type()
            else:
                prev_node = None
                root_node = node
                while (node is not None) and (node.name <= taxon_name):
                    if node.name == taxon_name:
                        node.data = self._add_node_rec(node.data, dict, dict_ind+1, img_id)
                        node.data.set_type()
                        break
                    else:
                        prev_node = node
                        node = node.next
                if (node is None) or (node.name > taxon_name):
                    node = Node(None, None, taxon_name)
                    node.data = self._add_node_rec(node.data, dict, dict_ind+1, img_id)
                    node.data.set_type()
                    if prev_node is not None:
                        node.next = prev_node.next
                        prev_node.next = node
                    else:
                        node.next = root_node
                    node.set_type()
                    if prev_node is not None:
                        node = prev_node
                
        else:
            node = Node(img_id, None, img_id)
            node.set_type()
        return node

    def _add_node(self, dict, img_id):
        self.root_taxon = self._add_node_rec(self.root_taxon, dict, 0, img_id)


    def get_node(self, node_path, node):
        if node is None:
            node = self.root_taxon
        try:
            n_pth_arr = node_path.split("/")
            while (node.name != n_pth_arr[0]) and (node is not None):
                node = node.next
            if node is not None:
                if len(n_pth_arr) <= 1:
                    return node.data
                else:
                    subnode_path = ""
                    index = 1
                    for i in range(len(n_pth_arr)-1):
                        subnode_path += n_pth_arr[index]
                        if i < (len(n_pth_arr)-2):
                            subnode_path+= '/'
                        index += 1
                    return self.get_node(subnode_path, node.data)
            else:
                return None
        except Exception:
            return node
                        
    
    
        


    
