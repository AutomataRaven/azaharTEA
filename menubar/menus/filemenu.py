from kivy.uix.spinner import Spinner
from kivy.properties import ListProperty

from menubar.menus.filechoosers.savedialog import SaveDialog
from menubar.menus.filechoosers.opendialog import OpenDialog

class FileMenu(Spinner):

    #TODO find a way to group values and FM_events in a single 
    # structure.
    values = ListProperty(['New File', 'Open File', 'Save', 'Save As'])
    
    def __init__(self, **kwargs):
        
        super(FileMenu, self).__init__(**kwargs)
        self.FM_events = {
                            
            'Save As': self.save_as, 
            'New File': self.open_new_tab,
            'Open File': self.open_file_tab
        }
    
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
       
    def open_new_tab(self):
        self.editor_container.add_new_tab()

    def open_file_tab(self):
        open_dialog = OpenDialog()
        open_dialog.propagate_editor_container(self.editor_container)
        open_dialog.open()
             
    def propagate_editor_container(self, editor_container):
    
        self.editor_container = editor_container
    
