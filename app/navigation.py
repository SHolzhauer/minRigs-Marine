import webview

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock

from threading import Thread


class NauticalMap(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.webview = None
        self.start_webview()

    def start_webview(self):
        # Start the webview in a separate thread
        Thread(target=self.create_webview).start()

    def create_webview(self):
        # Open Google Maps in webview
        self.webview = webview.create_window("Google Maps", "https://www.google.com/maps")
        webview.start()

