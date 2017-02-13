from kivy.uix.bubble import Bubble
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from pygments.lexers import get_all_lexers, get_lexer_by_name


class HighlightMenu(Bubble):

    scroll_view = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        
        super(HighlightMenu, self).__init__(**kwargs)
        
        self.layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.get_available_lexers()

        
    def get_available_lexers(self):
        
        #TODO find a way to only travel the result once but keeping
        # the sorting
        sorted_lexers = [name[0] for name in get_all_lexers()]
        sorted_lexers.sort()
        
        for lexer in sorted_lexers:
            self.add_lexer_to_list(lexer)
        
        self.scroll_view.add_widget(self.layout)

    def add_lexer_to_list(self, name):
        
        self.layout.add_widget(Button(text=name, size_hint_y=None,height=40))
