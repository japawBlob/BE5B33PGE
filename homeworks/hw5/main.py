import math
import queue
import time


class PGEBinaryTree:
    def __init__(self, input_tuple=None):
        if input_tuple is not None:
            self.AL = input_tuple[0]
            self.AR = input_tuple[1]
            self.C0 = input_tuple[2]
            self.CL = input_tuple[3]
            self.CR = input_tuple[4]
            self.D = input_tuple[5]
            self.M = input_tuple[6]
            self.RK = input_tuple[7]
            self.RSR = input_tuple[8]
        self.number_of_nodes = 0
        self.root = self.generate_tree()
        self.ret = [0, 0, 0, 0, 0, 0, 0, 0]


    def generate_tree(self, sr=None, key=None, depth=0):
        if sr is None or key is None:
            sr = self.RSR
            key = self.RK
        self.number_of_nodes += 1
        root = PGEBinaryTree.Node(self.number_of_nodes, key, depth, sr)
        if root.SR < self.C0 or root.depth == self.D:
            return root
        if self.C0 <= root.SR < self.CL:
            root.left_child = self.generate_tree((root.SR * self.AL) % self.M, (self.AL * (root.key+1)) % self.M, depth+1)
        if self.CL <= root.SR < self.CR:
            root.right_child = self.generate_tree((root.SR * self.AR) % self.M, (self.AR * (root.key + 2)) % self.M, depth+1)
        if self.CR <= root.SR < self.M:
            root.left_child = self.generate_tree((root.SR * self.AL) % self.M, (self.AL * (root.key+1)) % self.M, depth+1)
            root.right_child = self.generate_tree((root.SR * self.AR) % self.M, (self.AR * (root.key + 2)) % self.M, depth+1)
        return root

    def init_tree(self):
        self.init_sub_tree(self.root)

    def init_sub_tree(self, root):
        if root is None:
            return
        if root.left_child is not None:
            self.init_sub_tree(root.left_child)
        if root.right_child is not None:
            self.init_sub_tree(root.right_child)
        root.set_disbalance()
        root.set_2_balance()
        root.set_parity_children()
        root.set_locally_minimal()
        root.set_weakly_dominant()
        root.set_l1()
        root.set_increasing_paths()

    def go_trough_tree(self, root=None):
        if root is None:
            root = self.root
        self.ret[0] += root.get_cost()
        self.ret[1] += root.disbalance
        if root.is_2_balance:
            self.ret[2] += root.key
        if root.has_parity_children:
            self.ret[3] += 1
        if root.is_locally_minimal:
            self.ret[4] += root.key
        if root.is_weakly_dominant:
            self.ret[5] += 1
        if root.is_l1_tree:
            self.ret[6] += 1
        self.ret[7] = max(self.ret[7], root.value_of_increasing_path)
        if root.left_child is not None:
            self.go_trough_tree(root.left_child)
        if root.right_child is not None:
            self.go_trough_tree(root.right_child)

    def print_solution(self):
        for i in range(len(self.ret)):
            print(self.ret[i])

    def get_solution(self):
        ret = ""
        for i in range(len(self.ret)):
            ret += str(self.ret[i]) + "\n"
        return ret

    def setXcoord(self, node, x_coord):
        if node is None:
            return x_coord
        node.xcoord = self.setXcoord(node.left_child, x_coord) + 1
        #print(node.key, node.setXcoord)
        return self.setXcoord(node.right_child, node.xcoord)

    def display(self):
        self.setXcoord(self.root, 0)
        qu = queue.Queue()
        prev_depth = -1
        prev_end_x = -1
        # in the queue store pairs(node, its depth)
        qu.put( (self. root, 0) )
        while not qu.empty():
            node, node_depth = qu.get()

            left_branch_size = right_branch_size = 0
            if node.left_child is not None:
                left_branch_size = (node.xcoord - node.left_child.xcoord)
                qu.put( (node.left_child, node_depth+1) )
            if node.right_child is not None:
                right_branch_size = (node.right_child.xcoord - node.xcoord)
                qu.put( (node.right_child, node_depth+1) )

            left_spaces_size = (node.xcoord - left_branch_size) - 1  # if first on a line
            if prev_depth == node_depth:                  # not first on line
                left_spaces_size -= prev_end_x

            # print the node, branches, leading spaces
            if prev_depth < node_depth and prev_depth > -1 :
                print() # next depth occupies new line
            node_len = 2
            print( " "*node_len*left_spaces_size, end = '' )
            print( "_"*node_len*left_branch_size, end = ''  )
            # print( "." + ("%2d"%node.key) + node.tag+".", end = '' )
            # print( node.tag + ("%2d"%node.key), end = ''  )
            print( "" + ("%2d"%node.is_weakly_dominant), end = ''  )
            print( "_"*node_len*right_branch_size, end = ''  )

            # used in the next run of the loop:
            prev_end_x = node.xcoord + right_branch_size
            prev_depth = node_depth
        # end of queue processing
        print()
        # N = self.countNodes( self.root )
        # print("\n"+ '-'*N*node_len) # finish the last line of the tree

    class Node:
        def __init__(self, name, key, depth, sr, parent=None, left=None, right=None):
            self.name = name
            self.key = key
            self.parent = parent
            self.left_child = left
            self.right_child = right
            self.depth = depth
            self.SR = sr
            self.subtree_key_sum = None
            self.subtree_keys_of_2_balanced_nodes = None
            self.subtree_number_of_2_balanced_nodes = None
            self.disbalance = None
            self.is_2_balance = None
            self.is_2_node = None
            self.has_parity_children = None
            self.is_locally_minimal = None
            self.subtree_local_minimum = None
            self.subtree_dominating_number = None
            self.is_weakly_dominant = None
            self.subtree_contains_solo_left = None
            self.subtree_contains_solo_right = None
            self.is_l1_tree = None
            self.value_of_increasing_path = None
            self.xcoord = None

        def get_cost(self):
            return self.key * (self.depth+1)

        def set_disbalance(self):
            sum_left = 0
            sum_right = 0
            if self.left_child is not None:
                if self.left_child.disbalance is not None:
                    sum_left = self.left_child.subtree_key_sum+self.left_child.key
                else:
                    sum_left = self.left_child.set_disbalance()+self.left_child.key
            if self.right_child is not None:
                if self.right_child.disbalance is not None:
                    sum_right = self.right_child.subtree_key_sum+self.right_child.key
                else:
                    sum_right = self.right_child.set_disbalance()+self.right_child.key
            self.disbalance = abs(sum_left-sum_right)
            self.subtree_key_sum = sum_left+sum_right
            return self.subtree_key_sum

        def set_2_balance(self):
            number_of_2_nodes_left = 0
            number_of_2_nodes_right = 0
            if self.left_child is not None:
                if self.left_child.subtree_number_of_2_balanced_nodes is None:
                    number_of_2_nodes_left = self.left_child.set_2_balance() + self.left_child.is_2_node
                else:
                    number_of_2_nodes_left = self.left_child.subtree_number_of_2_balanced_nodes + self.left_child.is_2_node
            if self.right_child is not None:
                if self.right_child.subtree_number_of_2_balanced_nodes is None:
                    number_of_2_nodes_right = self.right_child.set_2_balance() + self.right_child.is_2_node
                else:
                    number_of_2_nodes_right = self.right_child.subtree_number_of_2_balanced_nodes + self.right_child.is_2_node
            self.is_2_node = self.left_child is not None and self.right_child is not None
            self.is_2_balance = number_of_2_nodes_right == number_of_2_nodes_left
            self.subtree_number_of_2_balanced_nodes = number_of_2_nodes_left + number_of_2_nodes_right
            return self.subtree_number_of_2_balanced_nodes

        def set_parity_children(self):
            if self.right_child is not None and self.left_child is not None and self.right_child.key % 2 == self.left_child.key % 2:
                self.has_parity_children = True
            return False

        def set_locally_minimal(self):
            left = math.inf
            right = math.inf
            if self.left_child is not None:
                if self.left_child.subtree_local_minimum is None:
                    left = self.left_child.set_locally_minimal()
                else:
                    left = self.left_child.subtree_local_minimum
            if self.right_child is not None:
                if self.right_child.subtree_local_minimum is None:
                    right = self.right_child.set_locally_minimal()
                else:
                    right = self.right_child.subtree_local_minimum
            if self.key <= min(left, right):
                self.is_locally_minimal = True
            else:
                self.is_locally_minimal = False
            self.subtree_local_minimum = min(self.key, left, right)
            return self.subtree_local_minimum

        def set_weakly_dominant(self):
            left = 0
            right = 0
            if self.left_child is not None:
                if self.left_child.subtree_dominating_number is None:
                    left = self.left_child.set_weakly_dominant()
                else:
                    left = self.left_child.subtree_dominating_number
            if self.right_child is not None:
                if self.right_child.subtree_dominating_number is None:
                    right = self.right_child.set_weakly_dominant()
                else:
                    right = self.right_child.subtree_dominating_number

            if self.right_child is None and self.left_child is None:
                self.is_weakly_dominant = False
                self.subtree_dominating_number = self.key
            else:
                self.subtree_dominating_number = max(left, right)
                if self.key >= max(left, right):
                    self.is_weakly_dominant = True
                else:
                    self.is_weakly_dominant = False
            return self.subtree_dominating_number

        def set_l1(self):
            left_solo_left = False
            left_solo_right = False
            right_solo_left = False
            right_solo_right = False
            if self.left_child is not None:
                if self.left_child.subtree_contains_solo_right is None or self.left_child.subtree_contains_solo_left is None:
                    self.left_child.set_l1()
                left_solo_left = self.left_child.subtree_contains_solo_left or self.right_child is None
                left_solo_right = self.left_child.subtree_contains_solo_right
            if self.right_child is not None:
                if self.right_child.subtree_contains_solo_right is None or self.right_child.subtree_contains_solo_left is None:
                    self.right_child.set_l1()
                right_solo_left = self.right_child.subtree_contains_solo_left
                right_solo_right = self.right_child.subtree_contains_solo_right or self.left_child is None
            if (not right_solo_right and not left_solo_right) and (left_solo_left or right_solo_left):
                self.is_l1_tree = True
            else:
                self.is_l1_tree = False
            self.subtree_contains_solo_left = left_solo_left or right_solo_left
            self.subtree_contains_solo_right = left_solo_right or right_solo_right

        def set_increasing_paths(self):
            left_value_of_increasing_path = self.key
            right_value_of_increasing_path = self.key
            if self.left_child is not None and self.key <= self.left_child.key:
                if self.left_child.value_of_increasing_path is None:
                    self.left_child.set_increasing_paths()
                left_value_of_increasing_path += self.left_child.value_of_increasing_path
            if self.right_child is not None and self.key <= self.right_child.key:
                if self.right_child.value_of_increasing_path is None:
                    self.right_child.set_increasing_paths()
                right_value_of_increasing_path += self.right_child.value_of_increasing_path
            self.value_of_increasing_path = max(left_value_of_increasing_path, right_value_of_increasing_path)


def load_input():
    tup = input().split()
    return int(tup[0]), int(tup[1]), int(tup[2]), int(tup[3]), int(tup[4]), int(tup[5]), int(tup[6]), int(tup[7]), int(tup[8]),


if __name__ == '__main__':
    # start_time = time.time()
    tree = PGEBinaryTree(load_input())
    tree.init_tree()
    tree.go_trough_tree()
    # tree.display()
    tree.print_solution()
    # print("Execution time", time.time() - start_time)


