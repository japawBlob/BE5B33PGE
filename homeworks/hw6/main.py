# from utils import display
class LERtree:
    def __init__(self, root, nodes):
        self.root = root
        self.nodes = nodes
        self.L_nodes_count = 0
        self.E_nodes_count = 0
        self.R_nodes_count = 0

    def set_LER(self):
        self.get_properties(self.root)

    def get_properties(self, node):
        if not (node.w_count is None or node.ww_count is None or node.b_count is None or node.bb_count is None):
            if node.colour == 0:
                return node.w_count + node.ww_count + 1, node.b_count + node.bb_count
            return node.w_count + node.ww_count, node.b_count + node.bb_count + 1
        if node.right_child is None:
            node.ww_count = 0
            node.bb_count = 0
        if node.left_child is None:
            node.w_count = 0
            node.b_count = 0
        if node.w_count is None or node.b_count is None:
            node.w_count, node.b_count = self.get_properties(node.left_child)
        if node.ww_count is None or node.bb_count is None:
            node.ww_count, node.bb_count = self.get_properties(node.right_child)
        node.set_LER()
        self.L_nodes_count += int(node.is_L)
        self.E_nodes_count += int(node.is_E)
        self.R_nodes_count += int(node.is_R)
        if node.colour == 0:
            return node.w_count + node.ww_count + 1, node.b_count + node.bb_count
        return node.w_count + node.ww_count, node.b_count + node.bb_count + 1

    def get_LER(self):
        return str(self.L_nodes_count) + " " + str(self.E_nodes_count) + " " + str(self.R_nodes_count) + "\n"

class Node:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.left_child = None
        self.right_child = None
        self.w_count = None
        self.ww_count = None
        self.b_count = None
        self.bb_count = None
        self.is_L = False
        self.is_E = False
        self.is_R = False
        self.LER = 0
        # self.is_principal = self.is_L or self.is_E or self.is_R
        self.xcoord = None

    def set_LER(self):
        if self.w_count is None or self.ww_count is None or self.b_count is None or self.bb_count is None:
            print("Cannot set LET with None variables")
            return
        if self.b_count == 0 or self.bb_count == 0 or self.w_count == 0 or self.ww_count == 0:
            return

        self.is_L = self.w_count/self.b_count > self.ww_count/self.bb_count
        self.is_E = self.w_count/self.b_count == self.ww_count/self.bb_count
        self.is_R = self.w_count/self.b_count < self.ww_count/self.bb_count
        self.LER = int(self.is_L)*100 + int(self.is_E)*10 + int(self.is_R)


def read_input():
    n = int(input())
    blob = Node(-1, -1)
    nodes = [blob for i in range(n)]
    colours = input().split()
    for i in range(n):
        nodes[i] = Node(i, int(colours[i]))
    for i in range(n-1):
        parent, node, position = input().split()
        if position == '0':
            nodes[int(parent)].left_child = nodes[int(node)]
        if position == '1':
            nodes[int(parent)].right_child = nodes[int(node)]
    return LERtree(nodes[0], nodes)


if __name__ == '__main__':
    tree = read_input()
    tree.set_LER()
    # display(tree)
    # print(tree.get_LER())
    print(tree.L_nodes_count, tree.E_nodes_count, tree.R_nodes_count)
