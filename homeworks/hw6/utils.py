import queue


def setXcoord(node, x_coord):
    if node is None:
        return x_coord
    node.xcoord = setXcoord(node.left_child, x_coord) + 1
    #print(node.key, node.setXcoord)
    return setXcoord(node.right_child, node.xcoord)


def display(tree):
    setXcoord(tree.root, 0)
    qu = queue.Queue()
    prev_depth = -1
    prev_end_x = -1
    # in the queue store pairs(node, its depth)
    qu.put( (tree.root, 0) )
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
        print( "" + ("%2d"%node.LER), end = ''  )
        print( "_"*node_len*right_branch_size, end = ''  )

        # used in the next run of the loop:
        prev_end_x = node.xcoord + right_branch_size
        prev_depth = node_depth
    # end of queue processing
    print()
    # N = self.countNodes( self.root )
    # print("\n"+ '-'*N*node_len) # finish the last line of the tree