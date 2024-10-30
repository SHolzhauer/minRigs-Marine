from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.garden.mapview import MapView, MarkerMap


class NauticalMap(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        map = MapView()

    def update_webview(self):
        # Continuously update the content in the WebKit widget
        Gtk.main()

