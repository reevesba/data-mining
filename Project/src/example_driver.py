import tana2tree as t2t

def main():
    # get the tree
    input_file = "dat/tan-output.txt"
    
    my_tree = t2t.Tanagra_Parser()
    print(my_tree.parse(input_file))

    # list all nodes in tree
    print(my_tree.traverse())

    # list specific node
    print(my_tree.get_node("wc"))

    # print tree in readable format
    my_tree.print_tree()

    # return tree as dict
    print(my_tree.make_dict())

if __name__ == '__main__':
    main()