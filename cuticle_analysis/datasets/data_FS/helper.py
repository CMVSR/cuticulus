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
    root_taxon = None
    
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
            if node is None:
                node = Node(None, None, dict[key])
                node.data = self._add_node_rec(node.data, dict, dict_ind+1, img_id)
            else:
                if node.name == dict[key]:
                    node.data = self._add_node_rec(node.data, dict, dict_ind+1, img_id)
                else:
                    node.next = self._add_node_rec(node.next, dict, dict_ind, img_id)
        else:
            node = Node(img_id, None, img_id)
        return node

    def _add_node(self, dict, img_id):
        self.root_taxon = self._add_node_rec(self.root_taxon, dict, 0, img_id)


    def get_node(self, node_path, node):
        try:
            n_pth_arr = node_path.split("/")
            if (node.name != n_pth_arr[0]):
                if node.next is not None:
                    return self.get_node(node_path, node.next)
                else:
                    return None
            else:
                if len(n_pth_arr) == 1:
                    return node.data
                else:
                    index = 1
                    subnode_path = ""
                    for i in range(len(node_path)-1):
                        subnode_path += n_pth_arr[index] + "/"
                        index += 1
                    return self.get_node(subnode_path, node.data)
        except Exception:
            return node
                        
    
    
        


    
