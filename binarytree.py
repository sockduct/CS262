# Write an "insert" procedure that takes a tree and
# an element and returns a new tree with that
# element inserted correctly
def insert(tree,element):
    if tree == None:
        return (None,element,None)
    else:
        left_child = tree[0]
        this_element = tree[1]
        right_child = tree[2]
        if element <= this_element:
            new_left_child = insert(left_child,element)
            return (new_left_child,this_element,right_child)
        else:
            # element >= this_element
            new_right_child = insert(right_child,element)
            return (left_child,this_element,new_right_child)

def print_tree(tree):
    if tree == None:
        return
    else:
        left_child = tree[0]
        this_element = tree[1]
        right_child = tree[2]
        print_tree(left_child)  # all <= this_element
        print this_element
        print_tree(right_child)  # all >= this_element

def contains(tree,element):
    if tree == None:
        return False
    else:
        left_child = tree[0]
        this_element = tree[1]
        right_child = tree[2]
        if element == this_element:
            return True
        elif element <= this_element:
            return contains(left_child,element)
        else:
            return contains(right_child,element)

