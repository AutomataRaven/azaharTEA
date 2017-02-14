from pygments import highlight
from pygments import lexers
from pygments.lexers import get_lexer_for_mimetype
from pygments import styles
from pygments.util import ClassNotFound
from pygments.formatters import BBCodeFormatter
from kivy.uix.codeinput import CodeInput

class Editor(CodeInput):
    
       
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
