from kivy.app import App
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from base import Logboek, startup, shutdown
from power_management import PowerManagement
from logboek import LogboekDisplay
from nautical_map import NauticalMap  # Import your new NauticalMap class

logboek = Logboek()

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "barendBoot Control Panel"
        
        # Set fullscreen
        Window.fullscreen = 'auto'

    def build(self):
        # Create main layout
        main_layout = BoxLayout(orientation='vertical')

        # Create the top bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        
        # Title label
        title_label = Label(
            text="barendBoot Control Panel",
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
        
        # Add title and exit button to the top bar
        top_bar.add_widget(title_label)
        top_bar.add_widget(exit_button)

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

        return main_layout

    def exit_app(self):
        logboek.log('status', 'gaat uit')
        shutdown()
        self.stop()  # Close the app

if __name__ == '__main__':
    logboek.log('status', 'aan gezet')
    startup()
    MyApp().run()
