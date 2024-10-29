from kivy.app import App
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window  # Import the Window module
from base import Logboek, startup, shutdown
from power_management import PowerManagement    # Import the PowerManagement class
#from dashboard import Dashboard                 # Import the Dashboard class
from logboek import LogboekDisplay              # Import the LogboekDisplay class

logboek = Logboek()

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "barendBoot Control Panel"
        
        # Set to launch fullscreen
        Window.fullscreen = 'auto'

    def build(self):
        # Create main layout
        main_layout = BoxLayout(orientation='vertical')

        # Create the top bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        
        # Title label
        title_label = Label(text=f"{self.title}", font_size=20, halign="left", valign="middle")
        
        # Exit button
        exit_button = Button(text="Exit", size_hint_x=0.15, on_release=App.get_running_app().stop())
        
        # Add title and exit button to the top bar
        top_bar.add_widget(title_label)
        top_bar.add_widget(exit_button)

        layout = BoxLayout(orientation='horizontal')

        # Create an accordion
        accordion = Accordion(orientation='horizontal')

        # Dashboard
        #dashboard_item = AccordionItem(title='Dashboard')
        #dashboard_item.add_widget(Dashboard())
        
        # Power Management
        power_mgmt_item = AccordionItem(title='Power Management')
        power_mgmt_item.add_widget(PowerManagement())

        # Logboek
        logboek_item = AccordionItem(title='Logboek')
        logboek_item.add_widget(LogboekDisplay())

        
        # Add accordion items to accordion
        accordion.add_widget(logboek_item)
        accordion.add_widget(power_mgmt_item)
        #accordion.add_widget(dashboard_item)

        # Add accordion to the main layout
        layout.add_widget(accordion)

        # Add the top bar and content layout to the main layout
        main_layout.add_widget(top_bar)
        main_layout.add_widget(content_layout)

        return layout

if __name__ == '__main__':
    logboek.log('status', 'aan gezet')
    startup()
    MyApp().run()
    logboek.log('status', 'gaat uit')
    shutdown()
