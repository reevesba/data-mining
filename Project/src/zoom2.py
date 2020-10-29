import gi, math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import cairo

dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
                            Gtk.ButtonsType.OK_CANCEL, "Press OK to test rotate")
dialog.format_secondary_text(
    "Press Cancel to test zoom")
is_rotate = (dialog.run() == Gtk.ResponseType.OK)
dialog.destroy()
testing = "Testing "+("Rotation" if is_rotate else "Zoom")

win = Gtk.Window()
win.set_default_size(800, 600)

drw = Gtk.DrawingArea()
label = Gtk.Label(testing)

angle_offset = 0
angle_cur = 0

scale_offset = 0
scale = 1

if(is_rotate):
    scale = 3 # otherwise it will be unreadably small


def rotate_begin(self, widget):
    global label
    label.set_text("Rotating!")
def rotate_follow(self, widget):
    global angle_offset, angle_cur
    angle_cur = self.get_angle_delta()
    drw.queue_draw()
def rotate_end(self, widget):
    global angle_offset, angle_cur, label, testing
    angle_offset += angle_cur
    angle_cur = 0
    drw.queue_draw()
    label.set_text(testing)

def zoom_begin(self, widget):
    global label
    label.set_text("Zooming!")
def zoom_follow(self, widget):
    global scale
    scale = self.get_scale_delta()
    drw.queue_draw()
def zoom_end(self, widget):
    global scale, scale_offset, label, testing
    scale_offset += (scale - 1)
    if(scale_offset < -0.95):
        scale_offset = -0.95
    scale = 1
    drw.queue_draw()
    label.set_text(testing)

def paint(self, cr):
    scale_f = scale + scale_offset # may not be mathematically correct
    if(scale_f < 0.05):
        scale_f = 0.05
    angle_f = angle_offset + angle_cur
    fsizef = scale_f * 4

    s = "Testing Zoom"
    if(is_rotate):
        s = "Testing Rotation"

    cr.set_line_width(2 * scale_f)
    cr.set_source_rgb(0, 0, 0.0)
            
    w = self.get_allocation().width
    h = self.get_allocation().height

    cr.translate(w/2, h/2)
    cr.rotate(angle_f)
    cr.rectangle(-50 * scale_f, 
        -75 * scale_f, 
        100 * scale_f, 
        150 * scale_f)
    cr.stroke_preserve()

    cr.set_source_rgb(0.85, 0.85, 0.85)
    cr.fill()


    cr.set_source_rgb(0.1, 0.1, 0.1)

    cr.translate(-45 * scale_f, -65 * scale_f)
    cr.set_font_size(fsizef)
    cr.text_path("In a hole in the ground there lived a hobbit. Not a ")
    cr.translate(0, fsizef + (0.6 * fsizef))
    cr.fill()
    cr.text_path("nasty, dirty, wet hole, filled with the ends of worms")
    cr.translate(0, fsizef + (0.6 * fsizef))
    cr.fill()
    cr.text_path("and an oozy smell, nor yet a dry, bare, sandy hole ")
    cr.translate(0, fsizef + (0.6 * fsizef))
    cr.fill()
    cr.text_path("with nothing in it to sit down on or to eat: it was")
    cr.translate(0, fsizef + (0.6 * fsizef))
    cr.fill()
    cr.text_path("a hobbit-hole, and that means comfort. ")
    cr.fill()

    # font size is an integer, which means font zooming won't be too smooth in this demo


drw.connect("draw", paint)

box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True, valign=Gtk.Align.FILL)
box.pack_start(label, False, False, 0)
box.pack_start(drw, True, True, 0)
win.add(box)

if is_rotate:
    gesture = Gtk.GestureRotate.new(drw)
    gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
    gesture.connect("begin", rotate_begin)
    gesture.connect("update", rotate_follow)
    gesture.connect("end", rotate_end)
else:
    gesture = Gtk.GestureZoom.new(drw)
    gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
    gesture.connect("begin", zoom_begin)
    gesture.connect("update", zoom_follow)
    gesture.connect("end", zoom_end)

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()