"""
highlight
=========

**Module** : ``footer.menus.highlightmenu.py``

Contains menus related to highlighting, like menus for style and lexer.
"""
from kivy.uix.bubble import Bubble
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles, get_style_by_name


class HighlightMenu(Bubble):
    """Highlight menu used to select the lexer for highlighting."""
    
    scroll_view = ObjectProperty(None)
    """:py:class:`kivy.properties.ObjectProperty` that references the :py:class:`kivy.uix.scrollview.ScrollView`
    used to put the :py:attr:`.HighlightMenu.layout` with the options."""
    
    editor_container = ObjectProperty(None)
    """A :py:class:`kivy.properties.ObjectProperty` that should
    be used to store a reference to :py:attr:`azaharTEA.Container.editor_container`."""
    
    def __init__(self, **kwargs):
        """Initialize attributes and gets available lexers."""
        
        super(HighlightMenu, self).__init__(**kwargs)
        self.lexers = dict()
        """Dictionary :py:obj:`dict` used to store the names and 1 alias of the
        lexer."""
             
        self.layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        """Layout used to put the options. This layout is the content for
        :py:attr:`.scroll_view`."""
        
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.get_available_lexers()
      
    def get_available_lexers(self):
        """Get the available lexers provided by :py:mod:`pygments.lexers`.
        
        When the lexers are retrieved they are ordered in increasing alphabetical
        order.
        
        Then they are added to the :py:attr:`.HighlightMenu.layout` and the :py:attr:`.HighlightMenu.layout` 
        added to the :py:attr:`.scroll_view`.
        """
        
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
        """Add a button , with its text being name, to the :py:attr:`.HighlightMenu.layout`.
        
        Here the added button's on_realese event is bound to :py:meth:`.change_lexer`.
        
        :param name: Name of the lexer that will be added to the list(:py:attr:`.HighlightMenu.layout`).
        """
        
        button = Button(text=name, size_hint_y=None,height=40)
        button.bind(on_release=lambda w: self.change_lexer(w))
        self.layout.add_widget(button)
      
    def change_lexer(self, widget):
        """Manage the on_realese event of a button added to :py:attr:`.HighlightMenu.layout`.
        Change the lexer of the current_tab's editor of :py:attr:`.editor_container`.
        
        It also changes the :py:attr:`footer.footer.FooterSpinner.display_state`
        of the parent (to "hidden").
        
        :param widget: Widget is a button that was added to :py:attr:`.HighlightMenu.layout`.       
        """
        
        lexer = get_lexer_by_name(self.lexers[widget.text])
        self.parent.text = widget.text
                
        self.parent.display_state = self.parent.states[self.parent.state_index]
        
        if self.editor_container:
            self.editor_container.current_tab.content.editor.lexer = lexer
 
 
class HighlightStyleMenu(Bubble):       
    """Highlight style menu used to select the style of the text (and :py:class:`editorcontainer.editor.editor.Editor`)
    displayed in the :py:class:`editorcontainer.editor.editor.Editor`.
    """
    scroll_view = ObjectProperty(None)
    """:py:class:`kivy.properties.ObjectProperty` that references the :py:class:`kivy.uix.scrollview.ScrollView`
    used to put the :py:attr:`.HighlightStyleMenu.layout` with the options."""
    
    editor_container = ObjectProperty(None)
    """A :py:class:`kivy.properties.ObjectProperty` that should
    be used to store a reference to :py:attr:`azaharTEA.Container.editor_container`."""
       
    def __init__(self, **kwargs):
        """Initialize attributes and gets available styles."""
        
        super(HighlightStyleMenu, self).__init__(**kwargs)      
        self.layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        """Layout used to put the options. This layout is the content for
        :py:attr:`.scroll_view`."""
        
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.get_available_styles()

        
    def get_available_styles(self):
        """Get the available styles provided by :py:mod:`pygments.lexers`.
        
        When the styles are retrieved they are ordered in increasing alphabetical
        order.
        
        Then they are added to the :py:attr:`.HighlightStyleMenu.layout` and the :py:attr:`.HighlightStyleMenu.layout` 
        added to the :py:attr:`.HighlightStyleMenu.scroll_view`.
        """
                
        #TODO find a way to only travel the result once but keeping
        # the sorting            
        self.styles = [name for name in get_all_styles()]
        self.styles.append('default TE')
        
        sorted_style = sorted(self.styles)

        for style in sorted_style:
            self.add_style_to_list(style)
        
        self.scroll_view.add_widget(self.layout)

    def add_style_to_list(self, name):
        """Add a button , with its text being name, to the :py:attr:`.HighlightStyleMenu.layout`.
        
        Here the added button's on_realese event is bound to :py:meth:`.change_style`.
        
        :param name: Name of the style that will be added to the list(:py:attr:`.layout`).
        """
                
        button = Button(text=name, size_hint_y=None,height=40)
        button.bind(on_release=lambda w: self.change_style(w))
        self.layout.add_widget(button)
      
    def change_style(self, widget):
        """Manage the on_realese event of a button added to :py:attr:`.HighlightStyleMenu.layout`.
        Change the style of the current_tab's editor of :py:attr:`.editor_container`.
        
        It also changes the :py:attr:`footer.footer.FooterSpinner.display_state`
        of the parent (to "hidden").
        
        :param widget: Widget is a button that was added to :py:attr:`.layout`.       
        """
           
        self.parent.text = widget.text
        self.parent.display_state = self.parent.states[self.parent.state_index]
        if self.editor_container:
            self.editor_container.current_tab.content.editor.change_style(widget.text)
                 

