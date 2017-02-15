from pygments import highlight
from pygments import lexers
from pygments.lexers import get_lexer_for_mimetype
from pygments import styles
from pygments.util import ClassNotFound
from pygments.formatters import BBCodeFormatter
from kivy.uix.codeinput import CodeInput
from kivy.utils import get_color_from_hex

class Editor(CodeInput):
    
    background_color_default_te = [1,1,1,1]
     
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

                    
