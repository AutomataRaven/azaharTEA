from kivy.uix.stacklayout import StackLayout
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty

from footer.menus.highlightmenu import HighlightMenu
from footer.menus.highlightmenu import HighlightStyleMenu

class Footer(StackLayout):
    
    highlight_menu = ObjectProperty(None)  
    line_col_menu = ObjectProperty(None) 
    higlight_style_menu = ObjectProperty(None)  
           
    cursor_pos = ListProperty([0,0])
    
    def __init__(self, **kwargs):
        
        super(Footer, self).__init__(**kwargs)
        self.menus_dict = {
                     
           'highlight_menu': self.change_lexer_information, 
           'line_col_menu': None,
           'highlight_style_menu': self.change_highlight_style
        }
                     
    def build_footer(self):
        pass
        
    def menu_display(self, widget):
    
        if (widget == self.highlight_menu) or (widget == self.highlight_style_menu):
            
            # See if a menu was already created to
            # speed up displaying it after the first time
            if not widget.child_menu:
                widget.editor_container = self.editor_container
                
                if widget == self.highlight_menu:
                    hl = HighlightMenu(pos=(widget.x, widget.y + widget.height))
                elif widget == self.highlight_style_menu:
                    hl = HighlightStyleMenu(pos=(widget.x, widget.y + widget.height))
                    
                hl.editor_container = self.editor_container
                hl.center_x = widget.center_x
                
                #pos = self.calculate_pos(container, hl)
                widget.bind(pos=lambda w, pos: self.change_pos(w))
                widget.child_menu = hl
                      
            widget.add_widget(widget.child_menu)
                  
   
    def menu_hide(self, widget):
        widget.remove_widget(widget.child_menu)
        pass
            
    def calculate_pos(self,window, widget):
    
        difference = 0
        if (widget.x + widget.width) > window.width:
            difference = (widget.x + widget.width) - window.width
        
        widget.x = widget.x - difference        
        
    def change_pos(self, parent):
        parent.child_menu.center_x = parent.center_x
        #self.calculate_pos(container, widget)

    def propagate_editor_container(self, editor_container):
    
        self.editor_container = editor_container
        current_tab = self.editor_container.current_tab
        self.editor_container.bind(current_tab=lambda w, v: self.change_current_tab(w, v))
        self.change_current_tab(self.editor_container, None)
    
    def change_current_tab(self, widget, value):
        editor = widget.current_tab.content.editor
        editor.unbind(cursor=lambda w, v: self.cursor_info(w,v))
        editor.bind(cursor=lambda w, v: self.cursor_info(w,v))
        self.cursor_info(None, editor.cursor)
        
    def cursor_info(self, widget, value):
        self.cursor_pos = [value[1] + 1, value[0] + 1]
        
    def change_information(self, information = dict()):
        
        try:
            for key, value in information.items():
                
                action = self.menus_dict[key]
                if action:
                   action(value)
                
        except KeyError as err:
            print(err, '{}: No such menu'.format(key), '\n') 
      
    def change_lexer_information(self, value):
       
       self.highlight_menu.text = value
       
    def change_highlight_style(self, value):
        pass   
                        
class FooterSpinner(Spinner):

    display_state = StringProperty('')
    states = ['hidden','displayed']
    state_index = NumericProperty(0)
    child_menu = ObjectProperty(None)
    editor_container = ObjectProperty(None)
    
    def on_display_state(self, instance, value):
 
        if self.display_state == 'hidden':
            self.parent.menu_display(self)
        else:
            self.parent.menu_hide(self)
            
        self.state_index = (self.state_index + 1) % len(self.states)
        
