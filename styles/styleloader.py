import json
import os

from kivy.utils import get_hex_from_color, get_color_from_hex

class StyleLoader:

    DEFAULT = 'default'
    
    def __init__(self, name = DEFAULT):
    
        self.style = None
        self.style_name = name
        self.set_style(name)
            
    def set_style(self, name = DEFAULT):
    
        try:
            with open(os.path.join('styles', name + '.json'), 'r') as file:
                self.style = json.load(file)
                # Assuming for the time being that all data are
                # colors.
                for key, value in self.style.items():
                    self.style[key] = get_color_from_hex(value)
                    
        except FileNotFoundError as err:
            print(err, 'Loading default style', sep = '\n')
            self.set_style(self.DEFAULT)       
         
