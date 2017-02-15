from kivy.uix.bubble import Bubble
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles, get_style_by_name


class HighlightMenu(Bubble):

    scroll_view = ObjectProperty(None)
    editor_container = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        
        super(HighlightMenu, self).__init__(**kwargs)
        self.lexers = {}        
        self.layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.get_available_lexers()

        
    def get_available_lexers(self):
        
        #TODO find a way to only travel the result once but keeping
        # the sorting
        sorted_lexers = [{name[0]: name[1][0]} 
                              for name in get_all_lexers()]
                              
        self.lexers = {name[0]: name[1][0] for name in get_all_lexers()}
        
        sorted_lexers = sorted(sorted_lexers, 
                                    key=lambda lexer: list(lexer.keys())[0])

        for lexer in sorted_lexers:
        
            for key, value in lexer.items():
                self.add_lexer_to_list(key)
        
        self.scroll_view.add_widget(self.layout)

    def add_lexer_to_list(self, name):
        
        button = Button(text=name, size_hint_y=None,height=40)
        button.bind(on_release=lambda w: self.change_lexer(w))
        self.layout.add_widget(button)
      
    def change_lexer(self, widget):
    
        lexer = get_lexer_by_name(self.lexers[widget.text])
        self.parent.text = widget.text
                
        self.parent.display_state = self.parent.states[self.parent.state_index]
        
        if self.editor_container:
            self.editor_container.current_tab.content.editor.lexer = lexer
 
class HighlightStyleMenu(Bubble):       
        
    scroll_view = ObjectProperty(None)
    editor_container = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        
        super(HighlightStyleMenu, self).__init__(**kwargs)
        self.styles = {}        
        self.layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.get_available_styles()

        
    def get_available_styles(self):
        
        #TODO find a way to only travel the result once but keeping
        # the sorting            
        self.styles = [name for name in get_all_styles()]
        self.styles.append('default TE')
        
        sorted_style = sorted(self.styles)

        for style in sorted_style:
            self.add_style_to_list(style)
        
        self.scroll_view.add_widget(self.layout)

    def add_style_to_list(self, name):
        
        button = Button(text=name, size_hint_y=None,height=40)
        button.bind(on_release=lambda w: self.change_style(w))
        self.layout.add_widget(button)
      
    def change_style(self, widget):
    
        #style = get_style_by_name(widget.text)
        self.parent.text = widget.text
        self.parent.display_state = self.parent.states[self.parent.state_index]
        if self.editor_container:
            self.editor_container.current_tab.content.editor.change_style(widget.text)
                 

