"""
savedialog
==========

**Module** : ``menubar.menus.filechoosers.savedialog.py``

Contains the class :py:class:`.SaveDialog`, used to show
a filechooser for saving.
"""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

import os

class SaveDialog(Popup):
    """A popup that shows a filechooser.
    
    Used to save the contents of the current_tab in the 
    :py:class:`editorcontainer.editorcontainer.EditorContainer`.
    
    The editor container should be :py:attr:`azaharTEA.Container.editor_container`.
    """
    
    save_button = ObjectProperty(None)
    """:py:class:`kivy.uix.button.Button` used to save the file (final step to save it)."""
    
    text_input = ObjectProperty(None)
    """:py:class:`kivy.uix.textinput.TextInput` used to write the name of the file."""

    cancel_button = ObjectProperty(None)
    """:py:class:`kivy.uix.button.Button` to close the popup (and the filechooser)."""    
           
    def cancel(self):
        """Manage the event (on_release) when :py:attr:`.cancel_button` is clicked.
        
        Closes the popup (and the widgets inside it, including the filechooser).
        """
        
        self.dismiss()
        
    def to_save(self, tab):
        """Set the tab whose contents will be saved.
        
        The reference to the tab is stored in :py:attr:`.self.tab_to_save`.
        
        :param tab: Tab whose contents want to be saved. In theory it should be \
        current_tab in the :py:class:`editorcontainer.editorcontainer.EditorContainer`. \
        The editor container should be :py:attr:`azaharTEA.Container.editor_container`.
        """
        
        self.tab_to_save = tab
        
    
    def save(self, path, name):
        """Manage the event (on_release) when :py:attr:`.save_button` is clicked.
        
        Saves the contents in the set tab (:py:attr:`.self.tab_to_save`, the current_tab).
        It creates a new file and saves the contents.
        The full path is *path* + *name*.
        
        :param path: Path to where the file should be saved.
        :param name: Name of the file to save.
        """   
        try:
            editor = self.tab_to_save.content.editor
            with open(os.path.join(path,name), 'w') as file:
                file.write(editor.text)
                editor._path = path
                editor._name = name
                self.tab_to_save.text = name
                self.tab_to_save.close_button_string = 'x'
                self.tab_to_save.saved = True
                
        except PermissionError as err:
            print(err, "You don't have the required access rights"
                  " to write to: {0}".format(path), sep = '\n')
        except IsADirectoryError as err:
            print(err, "Cannot save file as directory", sep = '\n')        
        finally:
            self.cancel()
