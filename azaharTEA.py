#!/usr/bin/env python3.5

"""Entry module for the application.

:py:class:`~.Container`

This class is a :py:class:`kivy.uix.boxlayout.BoxLayout` and is used
to contain the main components of the *GUI*.
"""

import sys
import mimetypes

import kivy
kivy.require('1.9.1')
from kivy.config import Config

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.core.window import Window
from pygments.lexers import get_lexer_for_mimetype

from editorcontainer.editorcontainer import EditorContainer
from menubar.menubar import MenuBar
from footer.footer import Footer
from kivyloader import load_all_kv_files


class Container(BoxLayout):
    """Contains the main *GUI* parts of the application.
    
    These parts are:
    
        * *Menu bar*
        * *Editor Container*: Contains the editor (with line numbers) and 
          a scroll.
        * *Footer*    
    """
    if Config:
        Config.set('kivy', 'desktop', 1)
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        
    menu_bar = ObjectProperty(None)
    """ A :py:class:`kivy.properties.ObjectProperty` that contains the
    menu bar, of type :py:class:`~menubar.menubar.MenuBar`
    """
    editor_container = ObjectProperty(None)
    """ A :py:class:`kivy.properties.ObjectProperty` of type 
    :py:class:`~editor.editorcontainer.EditorContainer` that contains 
    the editor and its scroll
    """
    footer = ObjectProperty(None)
    """ A :py:class:`kivy.properties.ObjectProperty` of type 
    :py:class:`~footer.fotter.Footer` that contains 
    the footer menus and information
    """
        
    def build_text_editor(self):
        """Build the text editor.
        
        Creates a default tab (if necessary) and also propagates
        the :py:attr:`.editor_container` to other parts of the application that
        need it.
        
        Doesn't return a specific value.
        """
        self.editor_container.build_default_tab() 
                   
        # Send editorcontainer to menubar and from there propapagate it
        self.menu_bar.propagate_editor_container(self.editor_container)
        # Send editorcontainer to footer and from there propapagate it
        self.footer.propagate_editor_container(self.editor_container)
        
                
class AzaharTEAApp(App):  
    """Builds the app (for kivy)"""
    
    mimetype = None
    """Used to store the mimetype of the file passed through console 
    (:py:attr:`sys.argv`), if any.
    """
    file_name = None
    """Used to store the name of the file passed through console
    (:py:attr:`sys.argv`), if any.
    """
    
    def build(self):
        """Build the main widget ( a :py:class:`.Container`)
        
        Loads all the *.kv* files and returns the main widget.
        """
        load_all_kv_files()
        
        self.container = Container()
        container = self.container
        container.editor_container.default_tab_mimetype = self.mimetype
        container.editor_container.default_tab_file_path = self.file_name
        container.build_text_editor()
        
        return container       
        
        
if __name__ == '__main__':

    app = AzaharTEAApp()
    
    # See if a file was opened directly to get the mime type and open 
    # it with the correct lexer
    if len(sys.argv) > 1:
        mime_type, encoding = mimetypes.guess_type(sys.argv[1])
        print(mime_type)
        app.mimetype = mime_type
        app.file_name = sys.argv[1]
        
    app.run()

