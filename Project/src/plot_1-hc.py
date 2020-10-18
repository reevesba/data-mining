import tana2tree as t2t

# step one: hardcoded implementation
# step two: implement based on example tree description

'''
Decision Tree w/ abbreviations
* uc < 2.5 
    * bn < 4.5 then class = benign (100.00 % of 200 examples) 
    * bn >= 4.5 then class = malignant (66.67 % of 6 examples) 
* uc >= 2.5 
    * bc < 1.5 then class = benign (87.50 % of 8 examples) 
    * bc >= 1.5 
        * cl < 4.5 
            * bn < 6.0 
                * mg < 3.5 then class = benign (100.00 % of 5 examples) 
                * mg >= 3.5 then class = malignant (66.67 % of 6 examples) 
            * bn >= 6.0 then class = malignant (100.00 % of 8 examples) 
        * cl >= 4.5 then class = malignant (93.97 % of 116 examples) 

splits: uc, bn, bc, cl, bn, mg
num_splits: 6
num_plots: 3

num_plots = ceil(num_label/2)
'''
input_file = "dat/sample_output.txt"

parser = t2t.Tanagra_Parser()
my_tree = parser.parse(input_file)

# list all nodes in tree
node_list = parser.traverse()
print(node_list)

# list specific node
#print(my_tree.get_node("wc"))

# print tree in readable format
#my_tree.print_tree()

# example tree description
tan_descr = {
    "label": "uc",
    "value": "2.5",
    "l_child": {
        "label": "bn",
        "value": "4.5",
        "l_child": {
            "target": "benign"
        },
        "r_child": {
            "target": "malignant"
        }
    },
    "r_child": {
        "label": "bc",
        "value": "1.5",
        "l_child": {
            "target": "benign"
        },
        "r_child": {
            "label": "cl",
            "value": "4.5",
            "l_child": {
                "label": "bn1",
                "value": "6.0",
                "l_child": {
                    "label": "mg",
                    "value": "3.5",
                    "l_child": {
                        "target": "benign"
                    },
                    "r_child": {
                        "target": "malignant"
                    }
                },
                "r_child": {
                    "target": "malignant"
                }
            },
            "r_child": {
                "target": "malignant"
            }
        }
    }
}

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.patches import ConnectionPatch

# my colors
RED = ["lightcoral", "red"]
BLUE = ["cornflowerblue", "blue"]
GRAY = ["lightgray", "dimgray"]

# try making a tree class to see if that helps with things
# may be easier for constructing graphs

def get_tree(d, labels, values, classes):
    for k, v in d.items():
        if isinstance(v, dict):
            get_tree(v, labels, values, classes)
        else:
            if k == "label":
                labels.append(v)
            if k == "value":
                values.append(v)
            if k == "target":
                classes.append(v)
    
    classes = list(set(classes))
    return labels, values, classes

def has_term_lchild(d, label, has_lleaf):
    for k, v in d.items():
        if isinstance(v, dict) and "label" in v:
            if v["label"] == label and "target" in v["l_child"]:
                has_lleaf.append(True)
            else:
                has_term_lchild(v, label, has_lleaf)

def has_term_rchild(d, label, has_rleaf):
    for k, v in d.items():
        if isinstance(v, dict) and "label" in v:
            if v["label"] == label and "target" in v["r_child"]:
                has_rleaf.append(True)
            else:
                has_term_rchild(v, label, has_rleaf)

def arrowed_spines(fig, ax):
    xmin, xmax = ax.get_xlim() 
    ymin, ymax = ax.get_ylim()

    # removing the default axis on all sides:
    for side in ['bottom', 'right', 'top', 'left']:
        ax.spines[side].set_visible(False)

    # arrowhead width and length
    hw = 1.0/20.0*(ymax - ymin) 
    hl = 1.0/20.0*(xmax - xmin)
    lw = 1.5     # axis line width
    ohg = 0.0    # arrow overhang

    # draw x and y axis
    ax.arrow(0.0, 0.0, xmax, 0.0, 
                facecolor='k',
                edgecolor='k', 
                linewidth = lw, 
                head_width=hw, 
                head_length=hl, 
                overhang = ohg, 
                length_includes_head= True, 
                clip_on = False) 


    ax.arrow(0.0, 0.0, 0.0, ymax, 
                facecolor='k',
                edgecolor='k', 
                linewidth = lw, 
                head_width=hw, 
                head_length=hl, 
                overhang = ohg, 
                length_includes_head= True, 
                clip_on = False)

def main():
    # get the data to plot
    labels = []
    values = []
    classes = []

    labels, values, classes = get_tree(tan_descr, labels, values, classes)

    print(labels)
    print(values)
    print(classes)

    labels2, values2, classes2 = [], [], []
    for node in node_list:
        if node.value:
            labels2.append(node.attr)
            values2.append(str(node.value))
        else:
            classes2.append(node.attr)
    print(labels2)
    print(values2)
    print(classes2)

    box_colors = {classes[0]: RED, classes[1]: BLUE}

    # used as list index
    ptr = 0

    # debugging
    #print(labels)
    #print(values)
    #print(classes)
    #print(box_colors)

    # TO DO: normalize values for generalization
    num_splots = int(np.ceil(len(labels)/2))

    # Some example data to display
    x = np.arange(1, 12, 1)
    y = x

    total_plots = num_splots
    cols = total_plots

    # Compute rows required
    rows = total_plots // cols 
    rows += total_plots % cols

    # create position index
    pos = range(1, total_plots + 1)

    # create main figure
    #fig = plt.figure(1)

    fig, axes = plt.subplots(nrows=rows, ncols=cols)    #figsize=(9, 3)
    fig.suptitle('Decision Tree in Shifted Paired Coordinates')

    # add subplots
    for ax in axes:
        ax.plot(x, y, linestyle='None') 

        # remove ticks from axis
        ax.set_xticks([])
        ax.set_yticks([])

        # make the plots square
        ax.set(adjustable='box', aspect='equal')

        # draw arrows for the axis
        arrowed_spines(fig, ax)

        # set axis labels/coords
        x_label = ax.set_xlabel(labels[ptr], fontsize=9)
        y_label = ax.set_ylabel(labels[ptr + 1], fontsize=9, rotation="horizontal")
        ax.xaxis.set_label_coords(0.9, 0.025)
        ax.yaxis.set_label_coords(0.1, 1.0)

        # draw boxes - first subplot
        # going to have to do something about coloring here
        # draw boxes
        ax_min = 0.0
        ax_max = 10.0
        lw = 1.0

        # how to decide the color?? and locations??
        # we need to determine if it's a terminal box, but how? 
        # 
        #
        #

        # first rect, intialize gray
        # second rect, if child terminal, color
            # if second child terminal color
            # else gray

        # wash, rinse, repeat

        # kind of working
        has_lleaf = []
        has_rleaf = []
        has_term_lchild(tan_descr, labels[ptr], has_lleaf)
        has_term_rchild(tan_descr, labels[ptr], has_rleaf)

        class_endpoints = 0
        if has_lleaf: class_endpoints = class_endpoints + 1
        if has_rleaf: class_endpoints = class_endpoints + 1

        #print("*** label: {0} terminal nodes: {1} ***".format(labels[ptr], class_endpoints))

        rect1 = Rectangle((ax_min, ax_min), float(values[ptr]), ax_max,
                            facecolor='lightgray',
                            linewidth=lw,
                            edgecolor='dimgray')
        ax.add_patch(rect1)

        if class_endpoints > 0:
            rect2 = Rectangle((float(values[ptr]), ax_min), ax_max - float(values[ptr]), float(values[ptr + 1]),
                                facecolor='lightcoral',
                                linewidth=lw,
                                edgecolor='red')
            ax.add_patch(rect2)

        if class_endpoints > 1:
            rect3 = Rectangle((float(values[ptr]), float(values[ptr + 1])), ax_max - float(values[ptr]), ax_max - float(values[ptr + 1]),
                                facecolor='cornflowerblue',
                                linewidth=lw,
                                edgecolor='blue')   
            ax.add_patch(rect3)

        #axes[0, i].add_patch(rect1)
        #axes[0, i].add_patch(rect2)
        #axes[0, i].add_patch(rect3)
        
        #ax1.add_patch(rect1)
        #ax1.add_patch(rect2)
        #ax1.add_patch(rect3)

        # draw boxes - second subplot
        #rect1 = Rectangle((0.0, 0.0), 1.5, 10.0,
                            #facecolor='cornflowerblue',
                            #linewidth=1.0,
                            #edgecolor='blue')

        #rect2 = Rectangle((1.5, 0.0), 8.5, 4.5,
                            #facecolor='lightgray',
                            #linewidth=1.0,
                            #edgecolor='dimgray')

        #rect3 = Rectangle((1.5, 4.5), 8.5, 5.5,
                            #facecolor='lightcoral',
                            #linewidth=1.0,
                            #edgecolor='red')

        #ax2.add_patch(rect1)
        #ax2.add_patch(rect2)
        #ax2.add_patch(rect3)

        # draw boxes - third subplot
        #rect1 = Rectangle((0.0, 0.0), 3.5, 6.0,
                            #facecolor='cornflowerblue',
                            #linewidth=1.0,
                            #edgecolor='blue')

        #rect2 = Rectangle((3.5, 0.0), 6.5, 6.0,
                            #facecolor='lightcoral',
                            #linewidth=1.0,
                            #edgecolor='red',
                            #linestyle='-')

        #rect3 = Rectangle((0.0, 6.0), 10.0, 4.0,
                            #facecolor='lightcoral',
                            #linewidth=1.0,
                            #edgecolor='red')

        #ax3.add_patch(rect1)
        #ax3.add_patch(rect2)
        #ax3.add_patch(rect3)

        # add tick labels
        ax.set_xticks([float(values[ptr])])
        ax.set_xticklabels([values[ptr]])
        ax.set_yticks([float(values[ptr + 1])])
        ax.set_yticklabels([values[ptr + 1]])

        # adjust ticks
        ax.tick_params(which='both', length=0, pad=-3)

        ptr = ptr + 2

    # draw arrows - first arrow
    xyA = (1.25, 7.25)
    xyB = (5.75, 7.25)
    con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                        axesA=fig.axes[0], axesB=fig.axes[1],
                        arrowstyle="->")

    con.set_color("red")
    con.set_linewidth(2)
    fig.axes[1].add_artist(con)

    # draw arrows - second arrow
    xyA = (1.25, 2.25)
    xyB = (5.75, 2.25)
    con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                        axesA=fig.axes[0], axesB=fig.axes[1],
                        arrowstyle="->")

    con.set_linewidth(2) 
    fig.axes[1].add_artist(con)

    # draw arrows - third arrow
    xyA = (5.75, 2.25)
    xyB = (1.75, 4.00)
    con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                        axesA=fig.axes[1], axesB=fig.axes[2],
                        arrowstyle="->")

    con.set_color("blue")
    con.set_linewidth(2) 
    fig.axes[2].add_artist(con)

    # draw arrows - fourth arrow
    xyA = (5.75, 2.25)
    xyB = (6.75, 2.25)
    con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                        axesA=fig.axes[1], axesB=fig.axes[2],
                        arrowstyle="->")

    con.set_color("red")
    con.set_linewidth(2) 
    fig.axes[2].add_artist(con)

    fig.savefig("out/decision_tree1.png")

if __name__ == '__main__':
    main()