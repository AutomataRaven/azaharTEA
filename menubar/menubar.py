"""
menubar
=======

**Module** : ``menubar.menubar.py``

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
    """A :py:class:`kivy.properties.Property` to store a reference to
    a :py:class:`menubar.menus.filemenu.FileMenu`.
    Menu with options for file operations.
    
    This options include things like:
        * New File: To open a new tab
        * Open File
        * Save as: To save a file with an specific name.
        * Save: To save all changed files that were already saved.
    """
    
    see_menu = ObjectProperty(None)
    """A :py:class:`kivy.properties.Property to store a reference to
    a :py:class:`menubar.menus.filemenu.SeeMenu`.
    Menu with options for "see" operations.
    
    This options include things like:
        * See line number: To show or hide the editor's line numbers.
    """
        
    def propagate_editor_container(self, editor_container):
        """Propagate an :py:class:`editorcontainer.editorcontainer.EditorContainer`
        to this :py:class:`.MenuBar`. 
        
        :param editor_container: :py:class:`editorcontainer.editorcontainer.EditorContainer` \
        that should be propagated. This editor_container should be :py:attr:`azaharTEA.Container.editor_container`.
        """
        self.editor_container = editor_container
        self.file_menu.propagate_editor_container(editor_container)
        self.see_menu.propagate_editor_container(editor_container)
          
