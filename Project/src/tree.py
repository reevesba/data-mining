# project tree class
class Node:
    def __init__(self, attr, value):
        self.l_branch = None
        self.r_branch = None
        self.attr = attr
        self.value = value

    def insert(self, attr, value):
        if self.value:
            if value < self.value:
                if self.l_branch is None:
                    self.l_branch = Node(attr, value)
                else:
                    self.l_branch.insert(attr, value)
            elif value > self.value:
                if self.r_branch is None:
                    self.r_branch = Node(attr, value)
                else:
                    self.r_branch.insert(attr, value)
        else:
            self.value = value

    def insert_left(self, attr, value):
        pass

    def print_tree(self):
        if self.l_branch:
            self.l_branch.print_tree()

        print("{0} < {1}".format(self.attr, self.value))

        if self.r_branch:
            self.r_branch.print_tree()

    def traverse(self, root):
        res = []
        if root:
            res = self.traverse(root.l_branch)
            res.append(root.value)
            res = res + self.traverse(root.r_branch)
        return res