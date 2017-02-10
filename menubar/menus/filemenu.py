from kivy.uix.spinner import Spinner

from kivy.properties import ListProperty

class FileMenu(Spinner):

    values = ListProperty(['New File', 'Save', 'Save as'])
    
    def _on_dropdown_select(self, instance, value):
        self.is_open = False
   

    
