import queue


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
        self.root = self.generate_tree()

    def generate_tree(self, sr=None, key=None, depth=0):
        if sr is None or key is None:
            sr = self.RSR
            key = self.RK
        root = PGEBinaryTree.Node(key, depth, sr)
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

    # calculates x coord = node order of in Inorder traversal
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
            #print( "." + ("%2d"%node.key) + node.tag+".", end = '' )
            #print( node.tag + ("%2d"%node.key), end = ''  )
            print( "" + ("%2d"%node.key), end = ''  )
            print( "_"*node_len*right_branch_size, end = ''  )

            # used in the next run of the loop:
            prev_end_x = node.xcoord + right_branch_size
            prev_depth = node_depth
        # end of queue processing
        print()
        # N = self.countNodes( self.root )
        # print("\n"+ '-'*N*node_len) # finish the last line of the tree

    class Node:
        def __init__(self, key, depth, sr, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left_child = left
            self.right_child = right
            self.depth = depth
            self.SR = sr
            self.disbalance = None
            self.is_balance_2 = None
            self.has_parity_children = None
            self.is_locally_minimal = None
            self.is_weekly_dominant = None
            self.is_l1_tree = None
            self.xcoord = None

        def get_cost(self):
            return self.key * (self.depth+1)

        def get_disbalance(self):
            sum_left = 0
            sum_right = 0
            if self.left_child is not None:
                sum_left = self.left_child.get_disbalance()
            if self.right_child is not None:
                sum_right = self.right_child.get_disbalance()
            self.disbalance = sum_left+sum_right
            return sum_left + sum_right

        def is_2_balance(self):
            number_of_balanced_left = 0
            number_of_balanced_right = 0
            if self.left_child is not None:
                number_of_balanced_left = self.left_child.get_2_balance()
            if self.right_child is not None:
                number_of_balanced_right = self.right_child.get_2_balance()
            # if number_of_balanced_left == number_of_balanced_right:
            #     return number_of_balanced_right + number_of_balanced_left
            # else:
            #     return False
            self.is_balance_2 = number_of_balanced_right == number_of_balanced_left
            return number_of_balanced_right == number_of_balanced_left

        def get_parity_children(self):
            if self.right_child.get_cost() % 2 == self.left_child.get_cost() % 2:
                self.has_parity_children = True
                return True

        def is_locally_minimal(self, target_key):
            if target_key > self.key:
                self.is_locally_minimal = False
                return False
            left = True
            right = True
            if self.left_child is not None:
                left = self.left_child.is_locally_minimal(target_key)
            if self.right_child is not None:
                right = self.right_child.is_locally_minimal(target_key)
            self.is_locally_minimal = left and right
            return left and right

        def is_weakly_dominant(self, dominating_key):
            if self.left_child is None and self.right_child is None:
                if dominating_key < self.key:
                    self.is_weekly_dominant = False
                    return False
                else:
                    self.is_weekly_dominant = True
                    return True
            ret = True
            if self.right_child is not None:
                ret &= self.right_child.is_weakly_dominant()
            if self.left_child is not None:
                ret &= self.left_child.is_weakly_dominant()
            self.is_weekly_dominant = ret
            return ret

        def is_l1_tree(self):
            left_child_found = [False]
            ret = self.l1_recu(left_child_found)
            self.is_l1_tree = ret & left_child_found[0]
            return ret & left_child_found[0]

        def l1_recu(self, left_child_found):
            if self.left_child is None and self.right_child is not None:
                return False
            if self.left_child is not None and self.right_child is None:
                left_child_found[0] = True
            ret = True
            if self.right_child is not None:
                ret &= self.right_child.is_L1_tree()
            if self.left_child is not None:
                ret &= self.left_child.is_weakly_dominant()
            return ret


def load_input():
    tup = input().split()
    return int(tup[0]), int(tup[1]), int(tup[2]), int(tup[3]), int(tup[4]), int(tup[5]), int(tup[6]), int(tup[7]), int(tup[8]),


if __name__ == '__main__':
    tree = PGEBinaryTree(load_input())
    tree.display()


