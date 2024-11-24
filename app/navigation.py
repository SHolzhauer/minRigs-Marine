import os.path
import json
import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker, MapSource


def download_sources():
    """Download the Fairway information from Rijkswaterstaat"""
    
    # Download the item information
    infra_info = {}
    for item in ["bridge", "lock"]:
        file_name = f"app/src/{item}.json"
        item_info = []
        if not os.path.isfile(file_name):
            total_count = 9
            offset = 0
            while len(item_info) < total_count:
                resp = requests.get(
                    url=f"https://www.vaarweginformatie.nl/wfswms/queryservice/1.4/current/{item}",
                    params={
                        "offset": offset
                    }
                ).json()
                total_count = resp["TotalCount"]
                item_info += resp["Result"]
                offset += 100
            
            # Store the information in a file
            with open(file_name, "w") as f:
                f.write(json.dumps(item_info))
        else:
            with open(file_name, "r") as f:
                item_info = json.loads(f.read())

        infra_info[item] = item_info
    
    return infra_info

class CustomMapMarker(MapMarker):
    def __init__(self, infra_info, **kwargs):
        super().__init__(**kwargs)
        self.info = infra_info
        self.bind(on_release=self.show_details)  # Trigger on marker click

    def show_details(self, *args):
        # Create the content for the popup
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=f"Name: {self.info['Name']}"))
        try:
            content.add_widget(Label(text=f"Telefoon: {self.info['PhoneNumber']}"))
        except KeyError:
            pass
        try:
            if self.info['CanOpen']:
                content.add_widget(Label(text="Beweegbare Brug"))
            else:
                content.add_widget(Label(text="Vaste Brug"))
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
        self._item_info = download_sources()
        
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
        #with open("app/src/bridge.json", "r") as f:
        #    info = f.read()

        for infra_type in self._item_info:
            for infra in self._item_info:
                geo = infra["Geometry"][7:-1].split(" ")
                marker = CustomMapMarker(
                    lat=geo[1],
                    lon=geo[0],
                    infra_info=infra,
                )
                self.map.add_marker(marker)


        # Add map widget to layout
        self.add_widget(self.map)

