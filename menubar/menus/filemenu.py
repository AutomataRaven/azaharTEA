from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

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
            'Open File': self.open_file_tab,
            'Save': self.save_all
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
     
    def save_all(self):
    
        tabs = self.editor_container.tab_list
        
        for tab in tabs:
            tab.content.editor.save_tab(True)
          
    def open_new_tab(self):
        self.editor_container.add_new_tab()

    def open_file_tab(self):
        open_dialog = OpenDialog()
        open_dialog.propagate_editor_container(self.editor_container)
        open_dialog.open()
             
    def propagate_editor_container(self, editor_container):
    
        self.editor_container = editor_container
 
 
class SeeMenuDropDown(DropDown):

    line_numbers_checkbox = ObjectProperty(None)
    
    
class SeeMenu(Spinner):
    
    def __init__(self, **kwargs):
        
        super(SeeMenu, self).__init__(**kwargs)   
         
        self.dropdown = SeeMenuDropDown()
    
    def open_menu(self, widget):
        
        self.dropdown.open(self)
        self.dropdown.line_numbers_checkbox.bind(active=self.on_checkbox_active)
        
      
    def on_checkbox_active(self, widget, value):
       
        tab_list = self.editor_container.tab_list
        
        for tab in tab_list:
            tab.content.show_line_numbers = value

          
    def _on_dropdown_select(self, instance, value):
    
        self.is_open = False
        
        try:
            self.FM_events[value]()
        except KeyError as err:
            
            print(err,'{}: no such option defined'.format(value), sep='\n')
   
    def show_line_numbers(self):
       
        editor = self.editor_container.current_tab.content.editor
                         
    def propagate_editor_container(self, editor_container):
    
        self.editor_container = editor_container   
