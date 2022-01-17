
class Node():


    def __init__(self, data, next, name):
        self.data = data
        self.next = next
        self.name = name

    def set_type(self):
        if isinstance(self.data, Node):
            self.type = "directory"
        else:
            if (isinstance(self.data, int)) & (self.data == self.name):
                self.type = "image"

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name
