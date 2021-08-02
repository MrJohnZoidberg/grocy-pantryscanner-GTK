import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):

    def __init__(self, pantryscanner):
        super().__init__(title="grocy Pantry-Scanner")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self._stack.set_transition_duration(500)

        label = Gtk.Label()
        label.set_markup("<big>A fancy label</big>")
        self._stack.add_titled(label, "consume", "Verbrauchen")

        button = Gtk.Button()
        button.set_label("<big>A fancy label</big>")
        self._stack.add_titled(button, "purchase", "Einkaufen")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self._stack)
        stack_switcher.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(stack_switcher, False, False, 0)
        vbox.pack_start(self._stack, True, True, 0)

        self.connect("destroy", pantryscanner.stop)
        self.maximize()
        self.show_all()

    def is_purchase_page(self):
        return self._stack.get_visible_child_name() == "purchase"
