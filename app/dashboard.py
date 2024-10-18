from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from speedmeter import SpeedMeter
# For testing
from kivy.clock import Clock
import random

class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Create a GridLayout for the 3x2 boxes
        grid = GridLayout(cols=4, rows=2, padding=50, spacing=10)

        self.gauges = []

        # RPM gauge
        rpm_meter = SpeedMeter()
        rpm_meter.id = "rpm"
        rpm_meter.min = 0
        rpm_meter.max = 2000
        rpm_meter.tick = 200
        rpm_meter.start_angle = -120
        rpm_meter.end_angle = 120
        rpm_meter.subtick = 4
        rpm_meter.label = "rpm"
        rpm_meter.label_font_size = 25
        rpm_meter.sectors = [0, '#000000', 1500, '#ffff00', 1800, '#ff0000', 2000]
        rpm_meter.width = 5
        box_layout = BoxLayout(orientation='vertical', spacing=5)
        box_layout.add_widget(rpm_meter)
        grid.add_widget(box_layout)
        self.gauges.append(rpm_meter)

        # Add 6 gauges to the grid with labels
        for i in range(3):
            # Create a box layout for each gauge and label
            box_layout = BoxLayout(orientation='vertical', spacing=5)

            gauge = SpeedMeter()
            gauge.id = f"auto_{i}"
            gauge.value = 10
            box_layout.add_widget(gauge)

            # Add a label for the gauge
            gauge_label = Label(text=f'Gauge {i + 1}', size_hint=(1, 1), height=30)
            box_layout.add_widget(gauge_label)

            # Add the box layout to the grid
            grid.add_widget(box_layout)
            self.gauges.append(gauge)

        # Rudder gauge
        rudder_gauge = SpeedMeter()
        rudder_gauge.id = "rudder"
        rudder_gauge.min = -45
        rudder_gauge.max = 45
        rudder_gauge.tick = 10
        rudder_gauge.start_angle = 125
        rudder_gauge.end_angle = 235
        #rudder_gauge.subtick = 4
        #rudder_gauge.label = "rudder"
        #rudder_gauge.label_font_size = 15
        rudder_gauge.label_icon = 'speedmeter/images/rudder.png'
        rudder_gauge.label_icon_scale = 0.4
        rudder_gauge.label_radius_ratio = "0.2"
        rudder_gauge.label_angle_ratio = "-1.13"
        #rudder_gauge.sectors = [0, '#000000', 15, '#ffff00', 18, '#ff0000', 20]
        rudder_gauge.width = 5
        box_layout = BoxLayout(orientation='vertical', spacing=5)
        box_layout.add_widget(rudder_gauge)
        grid.add_widget(box_layout)
        self.gauges.append(rudder_gauge)
        
        for i in range(1):
            # Create a box layout for each gauge and label
            box_layout = BoxLayout(orientation='vertical', spacing=5)

            gauge = SpeedMeter()
            gauge.id = f"auto_{i}"
            gauge.value = 10
            box_layout.add_widget(gauge)

            # Add a label for the gauge
            gauge_label = Label(text=f'Gauge {i + 1}', size_hint=(1, 1), height=30)
            box_layout.add_widget(gauge_label)

            # Add the box layout to the grid
            grid.add_widget(box_layout)

        # temperature gauge
        temp_meter = SpeedMeter()
        temp_meter.id = "temperature"
        temp_meter.min = 35
        temp_meter.max = 110
        temp_meter.tick = 5
        temp_meter.start_angle = 90
        temp_meter.end_angle = 270
        temp_meter.label_icon = 'speedmeter/images/temp.png'
        temp_meter.label_icon_scale = 0.2
        temp_meter.label_radius_ratio = 0.35
        temp_meter.sectors = [0, '#000000', 95, '#ffff00', 100, '#ff0000', 110]
        box_layout = BoxLayout(orientation='vertical', spacing=5)
        box_layout.add_widget(temp_meter)
        grid.add_widget(box_layout)
        self.gauges.append(temp_meter)
        
        # fuel gauge
        fuel_meter = SpeedMeter()
        fuel_meter.id = "fuel"
        fuel_meter.value = 100
        fuel_meter.min = 0
        fuel_meter.max = 100
        fuel_meter.tick = 25
        fuel_meter.start_angle = 150
        fuel_meter.end_angle = 20
        #fuel_meter.label = "rpm"
        #fuel_meter.label_font_size = 25
        fuel_meter.label_icon = 'speedmeter/images/fuel.png'
        fuel_meter.label_icon_scale = 0.2
        fuel_meter.label_radius_ratio = "0.5"
        fuel_meter.sectors = (0, '#ff0000', 15)
        #fuel_meter.width = 5
        box_layout = BoxLayout(orientation='vertical', spacing=5)
        box_layout.add_widget(fuel_meter)
        grid.add_widget(box_layout)
        self.gauges.append(fuel_meter)
        
        self.add_widget(grid)

        # Schedule the gauge update function to be called every second
        Clock.schedule_interval(self.update_detailed_gauges, 1)
        Clock.schedule_interval(self.update_gauges, 8)

    def update_detailed_gauges(self, dt):
        for g in self.gauges:
            if g.id == "rpm":
                g.value = random.randint(800, 900)
    
    def update_gauges(self, dt):
        for g in self.gauges:
            if g.id == "rudder":
                g.value = random.randint(-5, 5)
            elif g.id == "temperature":
                g.value = random.randint(85, 90)
            elif g.id == "fuel":
                if 100 >= g.value > 10:
                    g.value = g.value - 1
        