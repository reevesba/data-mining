import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

''' Various methods
    pack_start(child, expand, fill, padding-bottom)

'''

class MainClass():
    def __init__(self):
        self.window = Gtk.Window(title="Decision Tree in Shifted Paired Coordinates")
        self.window.set_default_size(600, 600)

        # provides styles for application
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path('src/application.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.boxvertical = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.window.add(self.boxvertical)
        #self.grid = Gtk.Grid()
        #self.window.add(self.grid)

        self.toolbar = Gtk.Toolbar(hexpand=True)
        # ensure that the toolbar will be styled like your os
        self.context = self.toolbar.get_style_context()
        self.context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.boxvertical.pack_start(self.toolbar, False, False, 0)
        #self.grid.add(self.toolbar)

        #  create buttons
        self.addbutton = Gtk.ToolButton(Gtk.STOCK_ADD)
        self.removebutton = Gtk.ToolButton(Gtk.STOCK_REMOVE)
        self.open_btn = Gtk.ToolButton(Gtk.STOCK_OPEN)

        # add buttons to toolbar
        self.toolbar.insert(self.open_btn, 0)
        self.toolbar.insert(self.addbutton, 1)
        self.toolbar.insert(self.removebutton, 2)

        # add the toolbar to our layout
        # buttons are also connected to their respective function
        self.open_btn.connect("clicked", self.on_file)
        self.addbutton.connect("clicked", self.addrow)
        self.removebutton.connect("clicked", self.removerow)

        #self.grid.attach_next_to(self.statbar, self.toolbar, Gtk.PositionType.BOTTOM, 1, 1)

        #self.sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        #self.textt = Gtk.Label(None)
        #self.textt.set_text("hello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\nhello worldddd\n")

        #self.sw.add(self.textt)
        #self.boxvertical.pack_start(self.sw, True, True, 10)

        self.box = Gtk.Box()
        self.boxvertical.pack_start(self.box, True, True, 0)
        
        self.statbar = Gtk.Statusbar()
        self.boxvertical.pack_start(self.statbar, False, True, 0)

        # setup fig and add it to layout
        self.fig = Figure(figsize=(10,10), dpi=80)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(300, 300)
        self.canvas.connect('scroll-event', self.on_scroll)
        self.box.pack_start(self.canvas, True, True, 0)
        #self.sw.add_with_viewport(self.canvas)
        #self.grid.attach_next_to(self.sw, self.statbar, Gtk.PositionType.BOTTOM, 1, 1)

        # setup the liststore and treeview
        self.liststore = Gtk.ListStore(float, float)
        self.treeview = Gtk.TreeView(model=self.liststore)
        self.box.pack_start(self.treeview, False, True, 0)
        #self.sw.add(self.treeview)
        #self.grid.attach_next_to(self.treeview, self.sw, Gtk.PositionType.BOTTOM, 2, 2)
        #self.grid.attach_next_to(self.treeview, self.sw, Gtk.PositionType.RIGHT, 1, 1)


        # connect the columns to their respective functions
        self.xrenderer = Gtk.CellRendererText()
        self.xrenderer.set_property("editable", True)
        self.xcolumn = Gtk.TreeViewColumn("x-Value", self.xrenderer, text=0)
        self.xcolumn.set_min_width(100)
        self.xcolumn.set_alignment(0.5)
        self.treeview.append_column(self.xcolumn)

        self.yrenderer = Gtk.CellRendererText()
        self.yrenderer.set_property("editable", True)
        self.ycolumn = Gtk.TreeViewColumn("y-Value", self.yrenderer, text=1)
        self.ycolumn.set_min_width(100)
        self.ycolumn.set_alignment(0.5)
        self.treeview.append_column(self.ycolumn)

        self.xrenderer.connect("edited", self.xedited)
        self.yrenderer.connect("edited", self.yedited)

        # add two default values to each column
        self.liststore.append([2.35, 2.40])
        self.liststore.append([3.45, 4.70])

    def on_file(self):
        dlg = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response = dlg.run()
        self.text.set_text(dlg.get_filename())
        dlg.destroy()

    def on_scroll(self, widget, event):
        print(widget.get_size_request())
        if event.direction == Gdk.ScrollDirection.UP:
            widget.set_size_request(widget.get_size_request()[0]+25, widget.get_size_request()[1]+25)
        elif event.direction == Gdk.ScrollDirection.DOWN:
            widget.set_size_request(widget.get_size_request()[0]-25, widget.get_size_request()[1]-25)

    '''
    clears the axis, resets limits, recreates grid
    '''
    def resetplot(self):
        self.ax.cla()
        self.ax.set_xlim(0,10)
        self.ax.set_ylim(0,10)
        self.ax.grid(True)

    '''
    iterates over the rows of the liststore
    for each row, one point is created
    '''
    def plotpoints(self):
        self.resetplot()
        for row in self.liststore:
            self.ax.scatter(row[:1], row[1:], marker='o', s=50)
        # updates the plot
        self.fig.canvas.draw()

    '''
    converts comma to period
    value the added to liststore
    '''
    def xedited(self, widget, path, number):
        self.liststore[path][0] = float(number.replace(',', '.'))
        self.plotpoints()

    def yedited(self, widget, path, number):
        self.liststore[path][1] = float(number.replace(',', '.'))
        self.plotpoints()

    '''
    appends or removes row from liststore
    '''
    def addrow(self, widget):
        self.liststore.append()
        self.plotpoints()

    def removerow(self, widget):
        # get currently selected row
        self.select = self.treeview.get_selection()
        self.model, self.treeiter = self.select.get_selected()
        if self.treeiter is not None:
            self.liststore.remove(self.treeiter)
        self.plotpoints()

if __name__ == '__main__':
    mc = MainClass()
    # set initial plot
    mc.resetplot()
    mc.plotpoints()

    mc.window.connect("delete-event", Gtk.main_quit)
    mc.window.show_all()

    # start the main loop
    Gtk.main()