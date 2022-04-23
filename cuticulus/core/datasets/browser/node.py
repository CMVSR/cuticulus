"""File for dataset browser tree node."""


class Node(object):

    def __init__(self, data, next, name):
        self.data = data
        self.next = next
        self.name = name
        self.set_type()

    def set_type(self):
        if (isinstance(self.data, int)) & (self.data == self.name):
            self.type = 'image'
        else:
            self.type = 'directory'

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name
