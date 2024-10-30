from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker, MapSource


class NauticalMap(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        mapsource = MapSource(
            min_zoom=13,
            max_zoom=16
        )
        
        self.map = MapView(
            map_source=mapsource,
            zoom=13, 
            lat=52.51677023841208, 
            lon=4.788266954784756,
            pause_on_action=False
        )
        
        
        # Add map widget to layout
        self.add_widget(self.map)

