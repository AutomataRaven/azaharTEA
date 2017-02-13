from kivy.uix.stacklayout import StackLayout
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from footer.menus.highlightmenu import HighlightMenu

class Footer(StackLayout):
    
    highlight_menu = ObjectProperty(None)  
    line_col_menu = ObjectProperty(None)    
    
    def __init__(self, **kwargs):
        
        super(Footer, self).__init__(**kwargs)

    def build_footer(self):
        pass
        
    def menu_display(self, widget):
    
        if widget == self.highlight_menu:
        
            container = self.parent
            
            # See if a menu was already created to
            # sped up displaying it after the first time
            if not widget.child_menu:
                widget.editor_container = self.editor_container
                hl = HighlightMenu(pos=(widget.x, widget.y + widget.height))
                hl.editor_container = self.editor_container
                pos = self.calculate_pos(container, hl)
                widget.bind(pos=lambda w, pos: self.change_pos(w, hl))
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
        
    def change_pos(self, parent, widget):
        container = parent.parent.parent
        widget.pos = (parent.x, parent.y + parent.height)
        self.calculate_pos(container, widget)

    def propagate_editor_container(self, editor_container):
    
        self.editor_container = editor_container
                        
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
        
