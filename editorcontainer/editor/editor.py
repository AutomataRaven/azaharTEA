import os

from pygments import highlight
from pygments import lexers
from pygments.lexers import get_lexer_for_mimetype
from pygments import styles
from pygments.util import ClassNotFound
from pygments.formatters import BBCodeFormatter
from kivy.uix.codeinput import CodeInput
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty

class Editor(CodeInput):
    
    background_color_default_te = [1,1,1,1]
    _path = StringProperty(None)
    _name = StringProperty(None)
    
    def __init__(self, **kwargs):
        
        super(Editor, self).__init__(**kwargs)
                
    def change_style(self, style = None):
        
        if style is not None:
           
            if style == 'default TE':
                self.style_name = 'default'    
                self.background_color = self.background_color_default_te
            elif style == 'default' and self.style_name == 'default':
                self.style_name = 'algol'
                self.style_name = 'default'
            else: 
                try:
                    self.style_name = style
                except ClassNotFound as err:
                    print(err, '{}: unknown style'.format(style))               
       
    def text_changed(self, *args):
        self.tab.close_button_string = '*\nx'
         
    def save_tab(self, all_tabs=False):
            
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
          
    def change_lexer(self, lexer = None):
        
        if lexer is not None:
        
            try:
                self.lexer = get_lexer_for_mimetype(lexer)
            except  ClassNotFound as err:
                print(err, 'Unsopported type {}'.format(lexer), sep='\n')
                self.lexer = lexers.TextLexer()
            finally:
                return self.lexer.name
            
                
        else:
            self.lexer = lexers.TextLexer()
            return self.lexer.name          

    def propagate_editor_container(self, editor_container):
        self.editor_container = editor_container                
