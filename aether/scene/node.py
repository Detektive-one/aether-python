class Node:
    def __init__(self, name='Node'):
        self.name = name
        self.parent = None
        self.children = []
        self.enabled = True
        self.visible = True
        self.x = 0.0
        self.y = 0.0
        self.z = 0

    def add_child(self, node: 'Node'):
        node.parent = self
        self.children.append(node)

    def remove_child(self, node: 'Node'):
        if node in self.children:
            self.children.remove(node)
            node.parent = None

    def global_position(self):
        gx, gy = self.x, self.y
        p = self.parent
        while p:
            gx += p.x
            gy += p.y
            p = p.parent
        return gx, gy


