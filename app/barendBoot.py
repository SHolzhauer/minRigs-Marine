from kivy.app import App
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
import threading
from time import sleep
from base import Logboek, startup, shutdown
from power_management import PowerManagement
from logboek import LogboekDisplay
from navigation import NauticalMap  # Import your new NauticalMap class
import os

logboek = Logboek()

def shutdown_system():
    os.system("shutdown -h now")

def reboot_system():
    os.system("shutdown -r now")


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.status_label = Label(text="Starting application...", font_size=24)
        self.layout.add_widget(self.status_label)
        self.add_widget(self.layout)

    def update_status(self, status):
        """Update the status message."""
        self.status_label.text = status

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._power_management = None

    def add_content(self, content):
        """Add content dynamically to the main screen."""
        self.layout.add_widget(content)
    
    def load_power_management(self):
        self._power_management = PowerManagement()

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "minRigs - Marine"
        
        # Set fullscreen
        Window.fullscreen = 'auto'

    def load_app(self):
        """Simulate loading tasks and switch to the main UI."""
        
        steps = [
            ("Stroom schakel module aan het laden...", self.load_power_management_module),
            ("Logboek aan het laden...", self.load_logboek_module),
            ("Navigatie aan het laden...", self.load_navigation_module),
            #("applicatie klaar maken...", self.load_main_ui)

        ]

        for step, func in steps:
            # Update the status on the loading screen
            Clock.schedule_once(lambda dt, step=step: self.loading_screen.update_status(step))
            sleep(1)  # Simulate some delay
            if func:
                func()

        # Schedule the screen transition on the main thread
        Clock.schedule_once(self.switch_to_main)

    def switch_to_main(self, *args):
        """Switch to the main UI."""
        self.loading_screen.clear_widgets()  # Clear widgets from loading screen
        self.sm.current = "main"
        
    def load_main_ui(self):
        # Create main layout
        main_layout = BoxLayout(orientation='vertical')

        # Create the top bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        
        # Title label
        title_label = Label(
            text=f"{self.title}",
            font_size=20,
            halign="left",
            valign="middle",
            text_size=(Window.width * 0.8, None)  # Define text width for better alignment
        )
        
        # Exit button
        exit_button = Button(
            text="Exit",
            size_hint_x=0.15,
            on_release=lambda x: self.exit_app()  # Use lambda to bind the function call
        )

        # Reboot button
        reboot_button = Button(
            text="reboot",
            size_hint_x=0.08,
            on_release=lambda x: reboot_system()  # Use lambda to bind the function call
        )

        # Shutdown button
        shutdown_button = Button(
            text="shutdown",
            size_hint_x=0.08,
            on_release=lambda x: shutdown_system()  # Use lambda to bind the function call
        )
        
        # Add title and exit button to the top bar
        top_bar.add_widget(title_label)
        top_bar.add_widget(exit_button)
        top_bar.add_widget(reboot_button)
        top_bar.add_widget(shutdown_button)

        # Create main content layout
        content_layout = BoxLayout(orientation='horizontal')

        # Create an accordion
        accordion = Accordion(orientation='horizontal')

        # Add Nautical Map
        map_item = AccordionItem(title='Nautical Map')
        map_item.add_widget(NauticalMap())
        
        # Power Management
        power_mgmt_item = AccordionItem(title='Power Management')
        power_mgmt_item.add_widget(PowerManagement())

        # Logboek
        logboek_item = AccordionItem(title='Logboek')
        logboek_item.add_widget(LogboekDisplay())

        # Add accordion items to accordion
        accordion.add_widget(logboek_item)
        accordion.add_widget(power_mgmt_item)
        accordion.add_widget(map_item)

        # Add accordion to the content layout
        content_layout.add_widget(accordion)

        # Add the top bar and content layout to the main layout
        main_layout.add_widget(top_bar)
        main_layout.add_widget(content_layout)

        Clock.schedule_once(lambda dt: self.main_screen.add_content(main_layout))
    
    def load_power_management_module(self):
        # Create PowerManagement UI elements
        #power_mgmt_item = AccordionItem(title='Power Management')
        #power_mgmt_item.add_widget(PowerManagement())
        Clock.schedule_once(lambda dt: self.main_screen.load_power_management())

    def load_logboek_module(self):
        sleep(2)
    
    def load_navigation_module(self):
        sleep(10)

    def build(self):
        self.sm = ScreenManager()

        # Add the loading screen
        self.loading_screen = LoadingScreen(name="loading")
        self.sm.add_widget(self.loading_screen)

        # Add the main screen (will be shown later)
        self.main_screen = MainScreen(name="main")
        self.sm.add_widget(self.main_screen)

        # Start the loading process
        threading.Thread(target=self.load_app, daemon=True).start()

        return self.sm
        
    def exit_app(self):
        logboek.log('status', 'gaat uit')
        shutdown()
        self.stop()  # Close the app

if __name__ == '__main__':
    logboek.log('status', 'aan gezet')
    startup()
    MyApp().run()
