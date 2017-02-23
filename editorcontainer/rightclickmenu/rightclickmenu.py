"""Contains the class :py:class:`.RightClickMenu`, a menu to open in the
:py:class:`editorcontainer.editor.editor.Editor`."""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.bubble import Bubble

class RightClickMenu(Bubble):
    
    
    editor = ObjectProperty(None)
    """Used to store a reference to a :py:class:`editorcontainer.editor.editor.Editor`."""
    
    def copy(self):

        self.editor._selection_from = self.editor.text_from
        self.editor._selection_to = self.editor.text_to
        self.editor.select_text(self.editor._selection_from, self.editor._selection_to)      
        self.editor.copy()       
        self.close_menu()

        
    def paste(self):
        
        self.editor.paste()
        self.close_menu()
        
    def cut(self):
        self.editor._selection_from = self.editor.text_from
        self.editor._selection_to = self.editor.text_to
        self.editor.select_text(self.editor._selection_from, self.editor._selection_to)
        self.editor.cut()
        self.close_menu()
        
    def select_all(self):
        
        self.editor.select_all()
        self.close_menu()
        
    def close_menu(self):
        if self.parent:
            self.parent.remove_widget(self)
