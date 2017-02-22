"""
footer
======

**Module** : ``footer.footer.py``

Contains the :py:class:`.Footer`, the footer of the application.
Contains the :py:class:`.FooterSpinner`, for information and 
the menus in the footer.
"""

from kivy.uix.stacklayout import StackLayout
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty

from footer.menus.highlightmenu import HighlightMenu
from footer.menus.highlightmenu import HighlightStyleMenu


class Footer(StackLayout):
    """
    A footer for the application. 
    
    The application should only have one
    footer, even though more can be added. The application's footer
    is :py:attr:`azaharTEA.Container.footer`.
    """
    
    highlight_menu = ObjectProperty(None)
    """Reference to a :py:class:`footer.footer.FooterSpinner`.
    
    Menu for the highlighting options (lexers).
    """  
    
    line_col_menu = ObjectProperty(None)
    """A :py:class:`footer.footer.FooterSpinner`.
    
    Menu for lines and columns. It will display the cursor's current line
    and column (:py:attr:`.cursor_pos`).
    """  
     
    highlight_style_menu = ObjectProperty(None)  
    """A :py:class:`footer.footer.FooterSpinner`.
    
    Menu for the highlighting style options (lexers).
    """  
               
    cursor_pos = ListProperty([0,0])
    """A :py:class:`kivy.properties.ListProperty` to store
    the cursor's current position.
    """
    
    def __init__(self, **kwargs):
    
        super(Footer, self).__init__(**kwargs)
        self.menus_dict = {
                     
           'highlight_menu': self.change_lexer_information, 
           'line_col_menu': None,
           'highlight_style_menu': self.change_highlight_style
        }
        """Dictionary of the available menus. 
        
        The *key* is the name and the *value* is the method to execute for 
        that menu.
        """
                                  
    def menu_display(self, widget):
        """Manage the on_release event for the menus and display the different 
        menus in the footer.
        
        This method is called when the menu of widget (if any) is "hidden".
        
        :param widget: Widget on which the event occurred. If widget has \
        a menu, then it should be displayed.
        """
        
        if ((widget == self.highlight_menu) 
             or (widget == self.highlight_style_menu)):        
            
            # See if a menu was already created to
            # speed up displaying it after the first time
            if not widget.child_menu:
                widget.editor_container = self.editor_container
                
                if widget == self.highlight_menu:
                    pos = (widget.x, widget.y + widget.height)
                    hl = HighlightMenu(pos=pos)
                elif widget == self.highlight_style_menu:
                    pos = (widget.x, widget.y + widget.height)
                    hl = HighlightStyleMenu(pos=pos)
                    
                hl.editor_container = self.editor_container
                hl.center_x = widget.center_x
                
                widget.bind(pos=lambda w, pos: self.change_pos(w))
                widget.child_menu = hl
                      
            widget.add_widget(widget.child_menu)
                  
   
    def menu_hide(self, widget):        
        """Manage the on_release event for the menus and hide the different
        menus in the footer.
        
        This method is called when the menu of widget (if any) is "displayed".
        
        :param widget: Widget on which the event occurred. If widget has \
        a menu, then it should be hidden.        
        """
        
        widget.remove_widget(widget.child_menu)                  
        
    def change_pos(self, parent):
        """Manage event when the position of the menu changes.
        
        This method is used to reposition the content of the menu 
        contained in parent, when the content is being "displayed" 
        parent is a menu (:py:attr:`.highlight_menu`, :py:attr:`.highlight_style_menu`,
        :py:attr:`.line_col_menu`).
        
        :param parent: Menu in which the event ocurred (menu that changed position).\
        The child (content) of parent is repositioned accordingly with the new position \
        of parent.
        """
        
        parent.child_menu.center_x = parent.center_x

    def propagate_editor_container(self, editor_container):
        """Propagate the :py:class:`editorcontainer.editorcontainer.EditorContainer` to this
        :py:class:`.Footer`.
               
        Binds the "current tab" of :py:attr:`.self.editor_container` (in theory a reference to
        :py:attr:`.azaharTEA.Container.editor_container`) to :py:meth:`.change_current_tab`.
        
        :param editor_container: :py:class:`~editorcontainer.editorcontainer.EditorContainer` to \
        be propagated to this :py:class:`.Footer`. It should be \
        :py:attr:`azaharTEA.Container.editor_container`.
        """
        
        self.editor_container = editor_container
        current_tab = self.editor_container.current_tab
        change_tab_lambda = lambda w, v: self.change_current_tab(w, v)
        self.editor_container.bind(current_tab=change_tab_lambda)
        self.change_current_tab(self.editor_container, None)
    
    def change_current_tab(self, widget, value):
        """Change the footer information when the tab changes.
        
        It also unbinds and binds again the cursor information to display.
        This is, unbinds and binds :py:attr:`.cursor_pos` to :py:meth:`cursor_info`.
        
        :param widget: Widget in which the tab changes. It should be \
        :py:attr:`azaharTab.editor_container`.
        :param value: Not used yet.
        """
        
        editor = widget.current_tab.content.editor
        editor.unbind(cursor=lambda w, v: self.cursor_info(w,v))
        editor.bind(cursor=lambda w, v: self.cursor_info(w,v))
        self.cursor_info(None, editor.cursor)
        self.change_lexer_information(editor.lexer.name)
        
        # Use the not bound name to get the text that should actually
        # be displayed.
        self.change_highlight_style(editor.style_name_not_bound)
        
    def cursor_info(self, widget, value):
        """Update cursor's position information, :py:attr:`.cursor_pos`."""
        
        self.cursor_pos = [value[1] + 1, value[0] + 1]
        
    def change_information(self, information = dict()):
        """Change the information displayed in the menus (text of the 
        menu, not the content).
        
        :param information: Dictionary (:py:obj:`dict`) that contains the information \
        to change. The *key* should be the name of the menu (like "highlight_menu") and \
        the *value* the new information (text of the menu) to display.
        """
        
        try:
            for key, value in information.items():
                
                action = self.menus_dict[key]
                if action:
                   action(value)
                
        except KeyError as err:
            print(err, '{}: No such menu'.format(key), '\n') 
      
    def change_lexer_information(self, value):
       """Change the text of the :py:attr:`.highlight_menu`"""
       
       self.highlight_menu.text = value
       
    def change_highlight_style(self, value):
        """Change the text of the :py:attr:`.highlight_style_menu`"""
        
        self.highlight_style_menu.text = value  
   
                        
class FooterSpinner(Spinner):
    """Widget to open a menu in the footer.
    
    Inherits from :py:class:`kivy.uix.spinner.Spinner` just because of its 
    appearance.
    """
    
    display_state = StringProperty('')
    """Current state of the menu for this :py:class:`.FooterSpinner`.
    
    It's a value from :py:attr:`.states`.
    """
    
    states = ['hidden','displayed']
    """Possible states which the menu for this :py:class:`.FooterSpinner` can be in."""
    
    state_index = NumericProperty(0)
    """A :py:class:`kivy.properties.NumericProperty`. The current index for :py:attr:`.states`.
    
    This index rotates to change the :py:attr:`.display_state`.
    """
    
    child_menu = ObjectProperty(None)
    """:py:class:`kivy.properties.ObjectProperty`. The contents for this :py:class:`.Footer`.
    This is the actual menu (the menu options or the content of the menu).
    
    This is what should be displayed and hidden when this :py:class:`.FooterSpinner` is
    clicked.
    """
    
    editor_container = ObjectProperty(None)
    """Should be used to store a reference to :py:attr:`azaharTEA.Container.editor_container`."""
    
    def __init__(self, **kwargs):   
        
        super(FooterSpinner, self).__init__(**kwargs)
        self.bind(texture_size=self.on_texture_size)
    
    def on_display_state(self, instance, value):
        """Manage event when :py:attr:`.display_state` changes.
        
        Rotates the value in :py:attr:`display_state`, assigning it values from
        :py:attr:`states` using :py:attr:`state_index`.
        
        :param instance: Instance of the widget on which the event ocurred. Always is this :py:class:`.FooterSpinner`.
        :param value: Value of :py:attr:`display_state` after the change.
        """
        if self.display_state == 'hidden':
            self.parent.menu_display(self)
        else:
            self.parent.menu_hide(self)
            
        self.state_index = (self.state_index + 1) % len(self.states)
   
    def on_texture_size(self, widget, value):
        """"""
        
        self.width = self.texture_size[0] + 2 * self.padding_x
    
    
    
       
