import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker, MapSource


class CustomMapMarker(MapMarker):
    def __init__(self, name, bridge_info, **kwargs):
        super().__init__(**kwargs)
        self.info = info
        self.bind(on_release=self.show_details)  # Trigger on marker click

    def show_details(self, *args):
        # Create the content for the popup
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=f"Name: {self.info['Name']}"))
        try:
            content.add_widget(Label(text=f"Telefoon: {self.info['PhoneNumber']}"))
        except KeyError:
            pass

        # Create and open the popup
        popup = Popup(
            title="Marker Details", 
            content=content, 
            size_hint=(0.6, 0.4)
        )
        popup.open()

class NauticalMap(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        mapsource = MapSource(
            #min_zoom=14,
            #max_zoom=14
        )
        
        self.map = MapView(
            map_source=mapsource,
            zoom=14, 
            lat=52.51677023841208, 
            lon=4.788266954784756,
            pause_on_action=False
        )
        
        # Add the bridges
        with open("app/src/bridge.json", "r") as f:
            info = f.read()

        info = json.loads(info)
        for bridge in info["Result"]:
            br_geo = bridge["Geometry"][7:-1].split(" ")
            marker = CustomMapMarker(
                lat=br_geo[1],
                lon=br_geo[0],
                bridge_info=bridge
            )
            self.map.add_marker(marker)


        # Add map widget to layout
        self.add_widget(self.map)

