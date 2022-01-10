
class Node():
    type = None

    def _set_type(self):
        if isinstance(self.data, Node):
            self.type = "directory"
        else:
            if (isinstance(self.data, int)) & (self.data == self.name):
                self.type = "image"

    def __init__(self, data, next, name):
        self.data = data
        self.next = next
        self.name = name
        self._set_type()

    def get_type(self):
        return self.type
