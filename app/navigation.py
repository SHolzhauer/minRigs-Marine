from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy_garden.mapview import MapView


class NauticalMap(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        map = MapView(zoom=13, lat=52.30, lon=4.47)

        self.add_widget(map)