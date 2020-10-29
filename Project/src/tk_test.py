import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.patches import ConnectionPatch
import tana2tree as t2t
import re

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import numpy as np

# color constants
COLORS = [["lightcoral", "red"],
          ["cornflowerblue", "blue"],
          ["lightseagreen", "seagreen"],
          ["lightgray", "dimgray"]]

LARGE_FONT= ("Verdana", 12)

# list specific node
#print(my_tree.get_node("wc"))

# print tree in readable format
#my_tree.print_tree()

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
    # initializing gtk
    win = Gtk.Window()
    win.set_default_size(800, 500)
    boxvertical = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    win.add(boxvertical)

    toolbar = Gtk.Toolbar()
    context = toolbar.get_style_context()
    context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
    boxvertical.pack_start(toolbar, True, True, 0)
    addbutton = Gtk.ToolButton(Gtk.STOCK_ADD)
    removebutton = Gtk.ToolButton(Gtk.STOCK_REMOVE)

    toolbar.insert(addbutton, 0)
    toolbar.insert(removebutton, 1)

    #addbutton.connect("clicked", addrow)
    #removebutton.connect("clicked", removerow)

    # adding button
    addbutton = Gtk.ToolButton(Gtk.STOCK_ADD)

    # parse tanagra description
    input_file = "dat/sample_output.txt"
    #input_file = "dat/tan-output.txt"
    parser = t2t.Tanagra_Parser()
    my_tree = parser.parse(input_file)

    # all nodes in tree
    node_list = parser.traverse()

    # will probably not need these
    # eventually want to read from node directly
    labels, values, classes = [], [], []

    for node in node_list:
        if node.value:
            labels.append(node.attr)
            values.append(str(node.value))
        else:
            find_index = node.attr.find("_")
            if find_index != -1:
                classes.append(node.attr[:node.attr.find("_")])
            else:
                classes.append(node.attr)

    classes = list(set(classes))
    classes.sort()
    num_classes = len(classes)

    box_colors = {}
    for i in range(num_classes):
        box_colors[classes[i]] = COLORS[i]

    #print(box_colors)

    parent_nodes = []
    target_nodes = []

    # make a list of the parent nodes
    for node in node_list:
        if node.value:
            parent_nodes.append(node)

    for node in parent_nodes:
        if node.l_branch.value is None:
            i = node.l_branch.attr.find("_")
            if i != -1: 
                node.l_branch.attr = node.l_branch.attr[:i]

        if node.r_branch.value is None:
            i = node.r_branch.attr.find("_")
            if i != -1: 
                node.r_branch.attr = node.r_branch.attr[:i]

    num_pnodes = len(parent_nodes)

    # used as list index
    ptr = 0

    # TO DO: normalize values for generalization

    num_splots = int(np.ceil(len(labels)/2))


    # controls the size of the plot
    # this means values should be in range 1-10
    # this is coded to 12 to make the axis labels longer
    x = np.arange(1, 12, 1)
    y = x

    total_plots = num_splots
    cols = total_plots

    # Compute rows required
    rows = total_plots // cols 
    rows += total_plots % cols

    # create position index
    pos = range(1, total_plots + 1)

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
        x_label = ax.set_xlabel(parent_nodes[ptr].attr, fontsize=9)
        y_label = ax.set_ylabel(parent_nodes[ptr + 1].attr, fontsize=9, rotation="horizontal")
        ax.xaxis.set_label_coords(0.9, 0.025)
        ax.yaxis.set_label_coords(0.1, 1.0)

        # setup the subplot rectangles
        ax_min = 0.0
        ax_max = 10.0
        lw = 1.0

        attr1_has_lleaf = False
        attr1_has_rleaf = False

        attr2_has_lleaf = False
        attr2_has_rleaf = False

        # find out if any of the parent nodes have a terminal node as child
        if parent_nodes[ptr].l_branch.value is None:
            print("{} left terminal is {}".format(parent_nodes[ptr].attr, parent_nodes[ptr].l_branch.attr))
            attr1_has_lleaf = True
        else: print("{} no left terminal".format(parent_nodes[ptr].attr))

        if parent_nodes[ptr].r_branch.value is None:
            print("{} right terminal is {}".format(parent_nodes[ptr].attr, parent_nodes[ptr].r_branch.attr))
            attr1_has_rleaf = True
        else: print("{} no right terminal".format(parent_nodes[ptr].attr))

        if parent_nodes[ptr + 1].l_branch.value is None:
            print("{} left terminal is {}".format(parent_nodes[ptr + 1].attr, parent_nodes[ptr + 1].l_branch.attr))
            attr2_has_lleaf = True
        else: print("{} no left terminal".format(parent_nodes[ptr + 1].attr))

        if parent_nodes[ptr + 1].r_branch.value is None:
            print("{} right terminal is {}".format(parent_nodes[ptr + 1].attr, parent_nodes[ptr + 1].r_branch.attr))
            attr2_has_rleaf = True
        else: print("{} no right terminal".format(parent_nodes[ptr + 1].attr))

        # building out first rectangle
        has_gray = True
        if attr1_has_rleaf is True and\
            attr2_has_lleaf is True and\
            attr2_has_rleaf is True: 
            has_gray = False

        if has_gray is True:
            if attr1_has_lleaf is False and attr1_has_rleaf is False:
                x_coord = ax_min
                y_coord = ax_min
                width = float(parent_nodes[ptr].value)
                height = ax_max
            elif attr1_has_lleaf is False:
                x_coord = float(parent_nodes[ptr].value)
                y_coord = float(parent_nodes[ptr + 1].value)
                width = ax_max - float(parent_nodes[ptr].value)
                height = ax_max
            elif attr1_has_rleaf is False:
                x_coord = float(parent_nodes[ptr].value)
                y_coord = ax_min
                width = ax_max - float(parent_nodes[ptr].value)
                height = float(parent_nodes[ptr + 1].value)
            else:
                x_coord = ax_min
                y_coord = ax_min
                width = ax_max
                height = ax_max

            fc = COLORS[3][0]
            ec = COLORS[3][1]
        else: 
            # no gray rectangle
            x_coord = 0
            y_coord = 0
            width = 0
            height = 0

        # add gray rectangle
        rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
        ax.add_patch(rect)
        
        if attr1_has_lleaf is True and attr1_has_rleaf is True:
            x_coord = parent_nodes[ptr].value
            y_coord = ax_min
            width = ax_max - parent_nodes[ptr].value
            height = parent_nodes[ptr + 1].value
            fc = box_colors[parent_nodes[ptr].l_branch.attr][0]
            ec = box_colors[parent_nodes[ptr].l_branch.attr][1]

            rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
            #ax.add_patch(rect)

            x_coord = parent_nodes[ptr].value
            y_coord = parent_nodes[ptr + 1].value
            width = ax_max - parent_nodes[ptr].value
            height = ax_max
            fc = box_colors[parent_nodes[ptr].r_branch.attr][0]
            ec = box_colors[parent_nodes[ptr].r_branch.attr][1]

            rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
            #ax.add_patch(rect)

        elif attr1_has_lleaf is True:
            x_coord = ax_min
            y_coord = ax_min
            width = parent_nodes[ptr].value
            height = ax_max
            fc = box_colors[parent_nodes[ptr].l_branch.attr][0]
            ec = box_colors[parent_nodes[ptr].l_branch.attr][1]

            rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
            ax.add_patch(rect)

        elif attr1_has_rleaf is True:
            x_coord = ax_min
            y_coord = parent_nodes[ptr + 1].value
            width = ax_max
            height = ax_max - parent_nodes[ptr + 1].value
            fc = box_colors[parent_nodes[ptr].r_branch.attr][0]
            ec = box_colors[parent_nodes[ptr].r_branch.attr][1]

            rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
            ax.add_patch(rect)
        else:
            pass

        if attr2_has_lleaf is True and attr2_has_rleaf is True:
            x_coord = parent_nodes[ptr].value
            y_coord = ax_min
            width = ax_max - parent_nodes[ptr].value
            height = parent_nodes[ptr + 1].value
            fc = box_colors[parent_nodes[ptr + 1].r_branch.attr][0]
            ec = box_colors[parent_nodes[ptr + 1].r_branch.attr][1]
    
            rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
            ax.add_patch(rect)
            
            if attr1_has_rleaf is True or attr1_has_lleaf is True:
                x_coord = ax_min
                y_coord = ax_min
                width = parent_nodes[ptr].value
                height = parent_nodes[ptr + 1].value
                fc = box_colors[parent_nodes[ptr + 1].l_branch.attr][0]
                ec = box_colors[parent_nodes[ptr + 1].l_branch.attr][1]

                rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
                ax.add_patch(rect)
            else:
                x_coord = parent_nodes[ptr].value
                y_coord = parent_nodes[ptr + 1].value
                width = ax_max - parent_nodes[ptr].value
                height = ax_max - parent_nodes[ptr + 1].value
                fc = box_colors[parent_nodes[ptr + 1].l_branch.attr][0]
                ec = box_colors[parent_nodes[ptr + 1].l_branch.attr][1]

                rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
                ax.add_patch(rect)
        elif attr2_has_lleaf is True:
            x_coord = parent_nodes[ptr].value
            y_coord = ax_min
            width = ax_max - parent_nodes[ptr].value
            height = parent_nodes[ptr + 1].value
            fc = box_colors[parent_nodes[ptr + 1].l_branch.attr][0]
            ec = box_colors[parent_nodes[ptr + 1].l_branch.attr][1]

            rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
            ax.add_patch(rect)

        elif attr2_has_rleaf is True:
            x_coord = parent_nodes[ptr].value
            y_coord = parent_nodes[ptr + 1].value
            width = ax_max - parent_nodes[ptr].value
            height = ax_max - parent_nodes[ptr + 1].value
            fc = box_colors[parent_nodes[ptr + 1].r_branch.attr][0]
            ec = box_colors[parent_nodes[ptr + 1].r_branch.attr][1]

            rect = Rectangle((x_coord, y_coord), width, height, fc=fc, lw=lw, ec=ec)
            ax.add_patch(rect)

        else:
            pass

        # add tick labels
        ax.set_xticks([float(parent_nodes[ptr].value)])
        ax.set_xticklabels([parent_nodes[ptr].value])
        ax.set_yticks([float(parent_nodes[ptr + 1].value)])
        ax.set_yticklabels([parent_nodes[ptr + 1].value])

        # adjust ticks
        ax.tick_params(which='both', length=0, pad=-3)

        ptr = ptr + 2

    # drawing arrows
    '''
    for i in range(num_splots - 1):
        # draw arrows - first arrow
        xyA = (1.25, 7.25)
        xyB = (5.75, 7.25)
        con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                            axesA=fig.axes[i], axesB=fig.axes[i + 1],
                            arrowstyle="->")

        con.set_color("blue")
        con.set_linewidth(2)
        fig.axes[i + 1].add_artist(con)

        # draw arrows - second arrow
        xyA = (1.25, 2.25)
        xyB = (5.75, 2.25)
        con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                            axesA=fig.axes[i], axesB=fig.axes[i + 1],
                            arrowstyle="->")

        con.set_linewidth(2) 
        fig.axes[i + 1].add_artist(con)

        # draw arrows - third arrow
        xyA = (5.75, 2.25)
        xyB = (5.00, 6.75)
        con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                            axesA=fig.axes[1], axesB=fig.axes[2],
                            arrowstyle="->")

        con.set_color("blue")
        con.set_linewidth(2) 
        fig.axes[2].add_artist(con)

        # draw arrows - fourth arrow
        xyA = (5.75, 2.25)
        xyB = (3.00, 2.25)
        con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                            axesA=fig.axes[1], axesB=fig.axes[2],
                            arrowstyle="->")

        con.set_color("red")
        con.set_linewidth(2) 
        fig.axes[2].add_artist(con)
    '''

    fig.savefig("out/decision_tree1.png")

    sw = Gtk.ScrolledWindow()
    win.add(sw)
    # A scrolled window border goes outside the scrollbars and viewport
    sw.set_border_width(10)

    canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
    canvas.set_size_request(800, 600)
    sw.add(canvas)

    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()