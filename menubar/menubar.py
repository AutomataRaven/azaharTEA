"""
menubar.py
==========

Contains the MenuBar class.

The MenuBar class is used to place the main menus for
the application.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from menubar.menus.filemenu import FileMenu
from menubar.menus.filemenu import SeeMenu

class MenuBar(BoxLayout):

    """Contains the main menus for the application.
    
    These menus include (more can be added or some can be removed):
        * File Menu: To create a new file, save a file...
        * See Menu: To select what to see (line numbers, for example)
    """

    file_menu = ObjectProperty(None)
    see_menu = ObjectProperty(None)
    
    def propagate_editor_container(self, editor_container):
        
        self.editor_container = editor_container
        self.file_menu.propagate_editor_container(editor_container)
        self.see_menu.propagate_editor_container(editor_container)
          
