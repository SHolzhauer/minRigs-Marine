import RPi.GPIO as GPIO
import configparser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from base import Logboek

logboek = Logboek()

# Get the power config
config = configparser.ConfigParser()
config.read('power.ini')

class PowerManagement(BoxLayout):
    def __init__(self, **kwargs):
        super(PowerManagement, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        # Create a layout for the switches
        self.switch_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.switch_layout)
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        self.pins = []
        for i in ['een','twee','drie','vier','vijf','zes','zeven','acht']:
            try:
                pin_config = {
                    'label': config[i]['label'],
                    'pin': int(config[i]['gpiopin']),
                    'enabled': False,
                }

                if 'aan' in config[i]['default']:
                    pin_config['enabled'] = True
                
                self.pins.append(pin_config)
            except KeyError:
                pass

        # Initialize the GPIO pins as outputs
        for item in self.pins:
            pin = item['pin']
            GPIO.setup(pin, GPIO.OUT)
            if item['enabled']:
                GPIO.output(pin, GPIO.HIGH)  # Set pin to be on initially
            else:
                GPIO.output(pin, GPIO.LOW)  # Set pins to be off initially

        # First column with the boat image
        boat_image = Image(source='boat.jpg')  # Add your boat image here
        self.add_widget(boat_image)

        # Add header
        l = Label(text='Stroom schakelaars', font_size='30sp')
        self.switch_layout.add_widget(l)
        # Create switches for each light
        for item in self.pins:
            label = item['label']
            pin = item['pin']
            enabled = item['enabled']
            # Create horizontal BoxLayout for each row (Label + Switch)
            row = BoxLayout(orientation='horizontal')
            switch = Switch(active=enabled)
            switch.bind(active=lambda sw, val, label=label, pin=pin: self.toggle_switch(pin, val))
            switch_label = Label(text=label)
            row.add_widget(switch_label)
            row.add_widget(switch)
            self.switch_layout.add_widget(row)
            
            #switch = Switch(active=False)
            #switch.bind(active=lambda sw, val, pin=pin: self.toggle_switch(pin, val))
            #switch_label = Label(text=label)
            #self.switch_layout.add_widget(switch_label)
            #self.switch_layout.add_widget(switch)

    def toggle_switch(self, label, pin, value):
        # Turn the GPIO pin on or off based on the switch state
        if value:
            logboek.log('status', f'schakelde {label} aan')
            GPIO.output(pin, GPIO.HIGH)  # Turn on the device
        else:
            logboek.log('status', f'schakelde {label} uit')
            GPIO.output(pin, GPIO.LOW)  # Turn off the device

    def on_stop(self):
        # Clean up GPIO on application exit
        GPIO.cleanup()
