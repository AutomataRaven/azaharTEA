"""
editor
======

Contains the :py:class:`.Editor`, that is, the graphical part
of the application to write/edit files.
"""

import os

from pygments import highlight
from pygments import lexers
from pygments.lexers import get_lexer_for_mimetype
from pygments import styles
from pygments.util import ClassNotFound
from pygments.formatters import BBCodeFormatter
from kivy.uix.codeinput import CodeInput
from kivy.extras.highlight import KivyLexer
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivy.properties import StringProperty


class Editor(CodeInput):
    """Inherits from :py:class:`kivy.uix.codeinput.CodeInput`.
    It's a :py:class:`.kivy.uix.widget.Widget` that is adapted to highlight its
    contents.
    """
        
    background_color_default_te = [1,1,1,1]
    """Default background color for the editor.
    
    It's set when the 'default TE' style is selected from the :py:class:`footer.footer.Footer`
    and when the application is opened in default.
    """
    
    _path = StringProperty(None)
    """Path to the file (without the file's name) that this :py:class:`.Editor` has open."""
    
    _name = StringProperty(None)
    """Name of the file (and tab) for this :py:class:`.Editor`"""
         
    style_name_not_bound = 'default TE'
    """Stores the style name but without being bound.
    
    Because it's not bound, it can store any name. Like 'default TE'
    """       
    
    def change_style(self, style = None):
        """Change the style of the editor.
        
        The style includes the background_color, the cursor color and the text 
        (keywords, variable names...). It means that changes the highlighting style.
        
        :param style: Name of the style to which to change.
        """
        
        if style is not None:
           
            if style == 'default TE':
                self.style_name = 'default'    
                self.style_name_not_bound = 'default TE'
                self.background_color = self.background_color_default_te
            elif style == 'default' and self.style_name == 'default':
                self.style_name = 'algol'
                self.style_name = 'default'
                self.style_name_not_bound = 'default'
            else: 
                try:
                    self.style_name = style
                    self.style_name_not_bound = style                     
                except ClassNotFound as err:
                    print(err, '{}: unknown style'.format(style))               
       
        if self.style:
            background_c = get_color_from_hex(self.style.background_color)
            color_sum = sum(background_c[0:3])
            if color_sum >= 0.5:
                self.cursor_color = [0, 0, 0, 1]
            else:
                self.cursor_color = [1, 1, 1, 1]

                
        self._trigger_refresh_text()
                   
    def text_changed(self, *args):
        """Manage event when :py:attr:`.Editor.text` changes.
        
        Changes the content of :py:attr:`editorcontainer.editorcontainer.EditorTab.close_button_string`.
        When that attribute is changed the text of :py:attr:`editorcontainer.editorcontainer.EditorTab.close_button`
        is automatically updated.
        
        This means this method is used to indicate the stated of the tab (unsaved, saved). The mark is an
        asterisk (*).
        
        :param \*args: Default arguments. Not used.
        """
        
        self.tab.close_button_string = '*\nx'
         
    def save_tab(self, all_tabs=False):
        """Save a tab.
        
        Writes the contents of this :py:class:`.Editor` to the file indicated by
        :py:attr:`._path` and :py:attr:`._name`.
        
        :param all_tabs: Boolean that indicates wheter just this :py:attr:`.Editor` 's tab \
        is being saved (:py:obj:`False`) or all the tabs open in the application are being \
        saved (:py:obj:`True`). When all_tabs is :py:obj:`False`, if the contents of this \
        :py:class:`.Editor` haven't been saved then a filechooser is shown.
        """
        
        if self._name is not None:
                    
            try:            
                    
                complete_path = os.path.join(self._path, self._name)
                with open(complete_path,'w+') as file:
                    file.write(self.text)
                        
                self.tab.close_button_string = 'x'
                    
            except PermissionError as err:
                print(err, "You don't have the required access rights"
                     " to write to: {0}".format(path), sep = '\n')
            except IsADirectoryError as err:
                print(err, "Cannot save file as directory", sep = '\n')        
                                
        elif not all_tabs:
            file_menu = self.editor_container.parent.menu_bar.file_menu
            file_menu.save_as()
          
    def change_lexer(self, mimetype = None):
        """Change the lexer of this :py:class:`.Editor`.
        
        The lexer is what takes care of recognizing the keywords, variable names, etc.
        
        :param mimetype: The mimetype for which a lexer should be found. The lexer is \
        changed to that found with this mimetype.
        """
        if mimetype is not None:
        
            try:
                # If the mimetype is 'text/plain' and the extension
                # of the file is '.kv', then a kivylexer should be used.
                if mimetype == 'text/plain' and os.path.splitext(self._name)[1] == '.kv':
                    self.lexer = KivyLexer()
                else:
                    self.lexer = get_lexer_for_mimetype(mimetype)
                
            except  ClassNotFound as err:
                print(err, 'Unsopported type {}'.format(mimetype), sep='\n')
                self.lexer = lexers.TextLexer()
            finally:
                return self.lexer.name
            
                
        elif self._name is not None:
            # If the mimetype is 'text/plain' and the extension
            # of the file is '.kv', then a kivylexer should be used.

            if os.path.splitext(self._name)[1] == '.kv':
                self.lexer = KivyLexer()
            else:
                self.lexer = lexers.TextLexer()
        else:
            
            self.lexer = lexers.TextLexer()
            
        return self.lexer.name          

    def propagate_editor_container(self, editor_container):
        """Propagate the :py:class:`~editorcontainer.editorcontainer.EditorContainer`
        to this :py:class:`.Editor`.
        
        :param editor_container: Should be a reference to :py:attr:`azaharTEA.Container.editor_container`, \
        the :py:class:`~editorcontainer.editorcontainer.EditorContainer` of the application.
        """
        
        self.editor_container = editor_container                
