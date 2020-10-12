import pydot

'''
tanagra_tree = {
    "uc": {
            "bn": {
                "benign1": "",
                "malignant1": ""
            },
            "bc":  {
                "benign2": "",
                "cl": {
                    "bn1": {
                        "mg": {
                            "benign4": "",
                            "malignant4": ""
                        },
                        "malignant3": ""
                    },
                    "malignant2": ""
                }
            }
        }
}


def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)

def visit(node, parent=None):
    for k,v in node.items():
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(parent, k)
            visit(v, k)
        else:
            draw(parent, k)

graph = pydot.Dot(graph_type='graph')
visit(tanagra_tree)
graph.write_png('example1_graph.png')
'''

tan_descr = {
    "label": "uc",
    "value": "2.5",
    "l_child": {
        "label": "bn",
        "value": "4.5",
        "l_child": {
            "label": "benign",
            "value": "0"
        },
        "r_child": {
            "label": "malignant",
            "value": "0"
        }
    },
    "r_child": {
        "label": "bc",
        "value": "1.5",
        "l_child": {
            "label": "benign",
            "value": "0"
        },
        "r_child": {
            "label": "cl",
            "value": "4.5",
            "l_child": {
                "label": "bn",
                "value": "6.0",
                "l_child": {
                    "label": "mg",
                    "value": "3.5",
                    "l_child": {
                        "label": "benign",
                        "value": "0"
                    },
                    "r_child": {
                        "label": "malignant",
                        "value": "0"
                    }
                },
                "r_child": {
                    "label": "malignant",
                    "value": "0"
                }
            },
            "r_child": {
                "label": "malignant",
                "value": "0"
            }
        }
    }
}


# print the entire dict
def print_dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            print("{0}: ".format(k))
            print_dict(v)
        else:
            print("{0}: {1}".format(k, v))

def print_labels(d):
    for k, v in d.items():
        if isinstance(v, dict) and v["value"] != "0":
            print_labels(v)
        else:
            if k == "label":
                print("{0}".format(v))

print_labels(tan_descr)