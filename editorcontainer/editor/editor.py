from pygments import highlight
from pygments import lexers
from pygments import styles
from pygments.formatters import BBCodeFormatter
from kivy.uix.codeinput import CodeInput

class Editor(CodeInput):
    
    def __init__(self, **kwargs):
        super(Editor, self).__init__(**kwargs)
        #The default will be plain text
        self.change_lexer(lexers.TextLexer())
       
    def change_lexer(self, lexer = None):
        
        if lexer is not None:
            self.lexer = lexer
        else:
            self.lexer = lexers.TextLexer()         
