import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Renderer(Gtk.CellRenderer):
    def __init__(self):
        super().__init__()


class MainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="grocy Pantry-Scanner")
        self.set_border_width(10)
        self.set_default_size(700, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self._stack.set_transition_duration(500)



        self.liststore = Gtk.ListStore(str, bool, bool)
        self.liststore.append(["Debian", False, True])
        self.liststore.append(["OpenSuse", True, False])
        self.liststore.append(["Fedora", False, False])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        #renderer_toggle.connect("toggled", self.on_cell_toggled)

        column_toggle = Gtk.TreeViewColumn("Toggle", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        renderer_radio = Gtk.CellRendererToggle()
        renderer_radio.set_radio(True)
        #renderer_radio.connect("toggled", self.on_cell_radio_toggled)

        column_radio = Gtk.TreeViewColumn("Radio", renderer_radio, active=2)
        treeview.append_column(column_radio)







        self._stack.add_titled(treeview, "consume", "Verbrauchen")

        button = Gtk.Button()
        button.set_label("<big>A fancy label</big>")
        self._stack.add_titled(button, "purchase", "Einkaufen")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self._stack)
        stack_switcher.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(self._stack, True, True, 0)

    def is_purchase_page(self):
        return self._stack.get_visible_child_name() == "purchase"

    def is_consume_page(self):
        return self._stack.get_visible_child_name() == "consume"


if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.maximize()
    win.set_icon_from_file("../resources/grocy.png")
    win.show_all()
    Gtk.main()
