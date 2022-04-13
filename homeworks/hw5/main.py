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
        self.root = None

    class Node:
        def __init__(self, key, depth, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left_child = left
            self.right_child = right
            self.depth = depth
            self.disbalance = 0
            self.balance_2 = False
            self.hasParityChildren = False

        def get_cost(self):
            return self.key * (self.depth+1)

        def get_disbalance(self):
            SL = 0
            SR = 0
            if self.left_child is not None:
                SL = self.left_child.get_disbalance()
            if self.right_child is not None:
                SR = self.right_child.get_disbalance()
            self.disbalance = SL+SR
            return SL + SR

        def get_2_balance(self):
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
            return number_of_balanced_right == number_of_balanced_left

        def get_parity_children(self):
            if self.right_child.get_cost() % 2 == self.left_child.get_cost() % 2:
                self.hasParityChildren = True
                return True

        def is_locally_minimal(self, target_key):
            if target_key > self.key:
                return False
            left = True
            right = True
            if self.left_child is not None:
                left = self.left_child.is_locally_minimal(target_key)
            if self.right_child is not None:
                right = self.right_child.is_locally_minimal(target_key)
            return left and right

        def is_weakly_dominant(self, dominating_key):
            if self.left_child is None and self.right_child is None:
                if dominating_key < self.key:
                    return False
                else:
                    return True
            ret = True
            if self.right_child is not None:
                ret &= self.right_child.is_weakly_dominant()
            if self.left_child is not None:
                ret &= self.left_child.is_weakly_dominant()
            return ret

        def is_L1_tree(self, left_child_found=False):
            if self.left_child is None and self.right_child is not None:
                return False
            ret = left_child_found



if __name__ == '__main__':
    pass