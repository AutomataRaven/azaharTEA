from pygments import highlight
from pygments import lexers
from pygments import styles
from pygments.formatters import BBCodeFormatter
from kivy.uix.codeinput import CodeInput

from styles.styleloader import StyleLoader

class Editor(CodeInput):
    
    def __init__(self,name, style_loader, **kwargs):
        super(Editor, self).__init__(**kwargs)
        self.editor_style_name = name
        self.style_loader = style_loader


    def _get_bbcode(self, ntext):
        # get bbcoded text for python
        try:
            ntext[0]
            
            if(self.editor_style_name != self.style_loader.DEFAULT):
                # replace brackets with special chars that aren't 
                # highlighted by pygment. can't use &bl; ... cause 
                # & is highlighted
                ntext = ntext.replace(u'[', u'\x01').replace(u']', u'\x02')
                ntext = highlight(ntext, self.lexer, self.formatter)
                ntext = ntext.replace(u'\x01', u'&bl;').replace(u'\x02',
                                                                u'&br;')
                # replace special chars with &bl; and &br;
                ntext = ntext.replace(u'\n', u'')
                # remove possible extra highlight options
                ntext = ntext.replace(u'[u]', '').replace(u'[/u]', '')
                
            ntext = ''.join((u'[color=', str(self.text_color), u']',
                            ntext, u'[/color]'))
            return ntext
            
        except IndexError:
            return ''
