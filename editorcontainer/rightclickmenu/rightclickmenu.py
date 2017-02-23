"""Contains the class :py:class:`.RightClickMenu`, a menu to open in the
:py:class:`editorcontainer.editor.editor.Editor`."""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.bubble import Bubble

class RightClickMenu(Bubble):
    """Right click menu to do actions like copy, paste, cut, select all..."""
    
    editor = ObjectProperty(None)
    """Used to store a reference to a :py:class:`editorcontainer.editor.editor.Editor`."""
    
    def copy(self):
        """Copy the selected text in :py:attr:`.editor`."""
        
        self.editor._selection_from = self.editor.text_from
        self.editor._selection_to = self.editor.text_to
        self.editor.select_text(self.editor._selection_from, self.editor._selection_to)
        self.editor.selection_text = str(self.editor.selection_text)   
        self.editor.copy()       
        self.close_menu()

        
    def paste(self):
        """Paste the copied text into :py:attr:`.editor`."""        
        self.editor.paste()
        self.close_menu()
        
    def cut(self):
        """Cut the selected text from :py:attr:`.editor`."""
        
        self.editor._selection_from = self.editor.text_from
        self.editor._selection_to = self.editor.text_to
        self.editor.select_text(self.editor._selection_from, self.editor._selection_to)
        self.editor.cut()
        self.close_menu()
        
    def select_all(self):
        """Select all the text in :py:attr:`.editor`."""
        
        self.editor.select_all()
        self.close_menu()
        
    def close_menu(self):
        """Close this :py:class:`.RightClickMenu`.
        
        Removes this :py:class:`.RightClickMenu` from the parent, if it
        has one.
        """
        
        if self.parent:
            self.parent.remove_widget(self)
