from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy_garden.mapview import MapView


class NauticalMap(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map = MapView(zoom=13, lat=52.51677023841208, lon=4.788266954784756)

        # Define min and max zoom limits
        self.min_zoom = 10
        self.max_zoom = 17
        
        # Add map widget to layout
        self.add_widget(self.map)
        
        # Schedule a check to enforce zoom limits on every frame
        Clock.schedule_interval(self.enforce_zoom_limits, 1 / 60)

    def enforce_zoom_limits(self, dt):
        # Adjust zoom to stay within bounds if it exceeds limits
        if self.map.zoom < self.min_zoom:
            self.map.zoom = self.min_zoom
        elif self.map.zoom > self.max_zoom:
            self.map.zoom = self.max_zoom