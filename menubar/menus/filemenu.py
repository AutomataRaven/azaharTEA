from kivy.uix.spinner import Spinner
from kivy.properties import ListProperty

from menubar.menus.filechoosers.savedialog import SaveDialog

class FileMenu(Spinner):

    values = ListProperty(['New File', 'Save', 'Save as'])
    
    def __init__(self, **kwargs):
        
        super(FileMenu, self).__init__(**kwargs)
        self.FM_events = {'Save as': self.save_as}
    
    def _on_dropdown_select(self, instance, value):
        self.is_open = False
        self.FM_events[value]()
   
    def save_as(self):
        SaveDialog().open()
    
