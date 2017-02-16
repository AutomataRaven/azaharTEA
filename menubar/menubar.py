from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from menubar.menus.filemenu import FileMenu
from menubar.menus.filemenu import SeeMenu

class MenuBar(BoxLayout):


    file_menu = ObjectProperty(None)
    see_menu = ObjectProperty(None)
    
    def propagate_editor_container(self, editor_container):
        
        self.editor_container = editor_container
        self.file_menu.propagate_editor_container(editor_container)
        self.see_menu.propagate_editor_container(editor_container)
          
