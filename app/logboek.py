import csv
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

class LogboekDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super(LogboekDisplay, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Create a header layout
        header = BoxLayout(size_hint_y=None, height=30)  # Fixed height for header
        header.add_widget(Label(text='Tijd', size_hint_x=0.33))
        header.add_widget(Label(text='Unit', size_hint_x=0.33))
        header.add_widget(Label(text='Meet waarde', size_hint_x=0.33))
        self.add_widget(header)

        # Create a scrollable area for the rows
        self.scroll_view = ScrollView()
        self.grid_layout = GridLayout(cols=3, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)

        self.add_widget(self.scroll_view)

        self.csv_file_path = 'logboek.csv'  # Update with your CSV file path
        
        # Initial display of CSV content
        self.update_logboek()
        
        # Schedule the update every 15 seconds
        Clock.schedule_interval(self.update_logboek, 15)

    def update_logboek(self, *args):
        """Update the displayed logboek with new rows from the CSV file."""
        # Clear existing rows in the grid layout
        self.grid_layout.clear_widgets()
        
        # Read the CSV file
        if os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) == 3:  # Ensure there are three columns
                        time, unit, measurement = row
                        self.grid_layout.add_widget(Label(text=time, size_hint_y=None, height=30))
                        self.grid_layout.add_widget(Label(text=unit, size_hint_y=None, height=30))
                        self.grid_layout.add_widget(Label(text=measurement, size_hint_y=None, height=30))

