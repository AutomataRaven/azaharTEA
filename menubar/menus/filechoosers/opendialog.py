"""
opendialog
==========

**Module** : ``menubar.menus.filechoosers.opendialog.py``

Contains the class :py:class:`.OpenDialog`, used to show
a filechooser for opening files.
"""

import os
import mimetypes

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class OpenDialog(Popup):
    """A popup that shows a filechooser.
    
    Used to open the contents of a file in a new tab.
    """
    
    open_button = ObjectProperty(None)
    """:py:class:`kivy.uix.button.Button` used to open the file (final step to open it)."""
    
    text_input = ObjectProperty(None)
    """:py:class:`kivy.uix.textinput.TextInput` the path is shown here when a file
    is selected. 
    
    The contents of this textinput are used to open the file.
    """
    
    cancel_button = ObjectProperty(None)
    """:py:class:`kivy.uix.button.Button` to close the popup (and the filechooser)."""    
          
    def cancel(self):
        """Manage the event (on_release) when :py:attr:`.cancel_button` is clicked.
        
        Closes the popup (and the widgets inside it, including the filechooser).
        """
        
        self.dismiss()
        
    def propagate_editor_container(self, editor_container):
        """Propagate the :py:class:`editorcontainer.editorcontainer.EditorContainer`
        to this :py:class:`.OpenDialog`.
        
        :param editor_container: :py:class:`editorcontainer.editorcontainer.EditorContainer` \
        to propagate to this :py:class:`.OpenDialog`. It should be a reference to \
        :py:class:`azaharTEA.Container.editor_container`.
        """
        
        self.editor_container = editor_container
        
    
    def open_file(self, path):
        """Manage the event (on_release) when :py:attr:`.open_button` is clicked.
        
        Opens the file in a new tab. The tab is built accordingly.
        
        :param path: Path of the file to open.
        """  
                   
        mimetype, encoding = mimetypes.guess_type(path)
                
        self.editor_container.build_tab(path, mimetype)
                                 
        self.cancel()
