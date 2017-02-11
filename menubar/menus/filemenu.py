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
        
        try:
            self.FM_events[value]()
        except KeyError as err:
            
            print(err,'{}: no such option defined'.format(value), sep='\n')
   
    def save_as(self):
    
        save_dialog = SaveDialog()
        save_dialog.to_save(self.editor_container.current_tab)
        save_dialog.open()
        
    def propagate_editor_container(self, editor_container):
    
        self.editor_container = editor_container
    
