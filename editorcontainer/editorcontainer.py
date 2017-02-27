"""
editorcontainer
==================

**Module**: ``editorcontainer.editorcontainer.py``

Module that contains all that's necessary to create
the file tabs
"""

import os
import math

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.scrollview import ScrollView

from editorcontainer.editor.editor import Editor
from editorcontainer.rightclickmenu.rightclickmenu import RightClickMenu
from confirmationdialog.confirmationdialog import ConfirmationDialog

class CodeScrollView(ScrollView):
    """A :py:class:`kivy.uix.scrollview.ScrollView` that contains the
    editor and line numbers.
    
    The purpose of this class is to make the line numbers and editor
    scrollable together.
    """
    
    line_numbers_strip = ObjectProperty(None)
    """:py:class:`kivy.properties.ObjectProperty` reference to the line
    numbers widget, of type :py:class:`~editorcontainer.editor.editor.Editor`
    """
    
    editor = ObjectProperty(None)
    """:py:class:`kivy.properties.ObjectProperty` reference to the editor 
    widget, of type :py:class:`~editorcontainer.editor.editor.Editor`
    """
        
    layout = ObjectProperty(None)
    """Reference to the layout that is the content of this :py:class:`.CodeScrollView`.
    
    It contains the :py:attr:`.editor` and :py:attr:`.line_numbers_strip`
    """
    
    show_line_numbers = BooleanProperty(True)   
    """:py:class:`kivy.properties.BooleanProperty` that indicates wether this
    :py:class:`.CodeScrollView` should display the line numbers (:py:obj:`True`)
    or not (:py:obj:`False`). Defaults to :py:obj:`True`.
    """    
    
    def __init__(self, **kwargs):
        """Call __init__ from super and decide wether to show the line numbers"""
        
        super(CodeScrollView, self).__init__(**kwargs)
        
        self.max_num_of_lines = 0
        """Maximum number of lines actually.
        
        It will increase depending on the quantity of lines in the editor.
        Generally, it increases when 'enter' is pressed (a new line is added).
        Defaults to 0.
        """
        
        self.scroll_distance = self.editor.line_height
        
        self.editor.bind(focus=self.on_editor_focus)
        
        parent = self.line_numbers_strip.parent
        
        if not self.show_line_numbers:
            parent.remove_widget(self.line_numbers_strip)
        else:
            self.editor.bind(_lines=self.on_lines_change)

    def on_editor_focus(self, widget, value):
        """Bind or unbind :py:meth:`.on_keyboard` depending on the focus of the editor
        
        It binds an event (with the method :py:meth:`.on_keyboard`) to the
        :py:attr:`kivy.core.window.Window.on_keyboard` attribute.
        
        :param widget: Instance of the :py:attr:`kivy.uix.widget` on which the event ocurred (:py:attr:`.editor`). 
        :param value: Value of the property of the event (:py:attr:`.editor.focus` in this case).        
        """
        
        if value:
            Window.bind(on_keyboard=self.on_keyboard)
            Window.bind(on_mouse_down=self.on_mouse_down)
        else:
            Window.unbind(on_keyboard=self.on_keyboard)
            Window.unbind(on_keyboard=self.on_mouse_down)

    def on_mouse_down(self, mouse, x, y, button, modifiers):
        """Manage event when some mouse button is utliized.
        
        For example, when the middle mouse button is used to scroll,
        the cursor is repositioned here.
        
        :param mouse: Instance of the mouse listener.
        :param x: x position of the mouse.
        :param y: y position of the mouse.
        :param button: Mouse button pressed ('left', 'right', 'scrollup', ...)
        :param modifiers: Modifiers used for the mouse press ('ctrl', 'alt', ...)
        """
        self.editor.last_click = button
        
        # In any case, remove a right click menu if there is one
        rc_menu = self.editor_container.right_click_menu
        if rc_menu is not None and rc_menu in Window.children:
        
            top = Window.size[1] - (rc_menu.y + rc_menu.height)
            bottom = (top + rc_menu.height - 10) #TODO find a way to remove this 10
            # It's in the widget and I don't know why (in the widget in rightclickmenu.kv)
            
            if ((x < rc_menu.x or x > rc_menu.width + rc_menu.x)
                or (y < top or y > bottom) or button == 'right'):
                
                Window.remove_widget(rc_menu)        
        
        # To show right click menu, let's brute force this.
        # It calculates if the click is inside the visible area 
        # of the editor.
        if button == 'right':
                      
            self.editor.text_from = self.editor._selection_from
            self.editor.text_to = self.editor._selection_to   
            c_y = self.editor_container.y
            c_h = self.editor_container.height
            m_c_x = self.editor_container.to_widget(x, y, relative=True)
            
            top = (Window.size[1] - c_y 
                   - c_h + self.editor_container._tab_layout.height)
                   
            bottom = c_h + self.editor_container.parent.menu_bar.height
            
            editor = self.editor_container.current_tab.content.editor
            
            e_x = editor.x
            e_w = editor.x + editor.width
            if (len(self.editor_container.tab_list) > 0 
                and (x >= e_x  and x < e_w) 
                and (y >= top and y <= bottom) ):
                
                self.editor_container.open_right_click_menu(x+15, y)                    
            
        if button == 'scrollup':
        
            editor = self.editor
            y_pos = math.floor(self.scroll_y 
                              * float(self.viewport_size[1] - self.height))  
            
            new_col, new_row = editor.get_cursor_from_xy(self.scroll_x,
                                                         y_pos)            

            editor.cursor = (editor.cursor_col, new_row)
            
        if button == 'scrolldown':
        
            editor = self.editor
            
            y_pos = math.floor(self.scroll_y 
                              * float(self.viewport_size[1] 
                                      - self.height))  
            
            new_col, new_row = editor.get_cursor_from_xy(self.scroll_x,
                                                         y_pos + self.height)           

            editor.cursor = (editor.cursor_col, new_row)        
                    
    def on_keyboard(self, keyboard, keycode, scancode, value, modifiers):
        """Manage keyboard events (on :py:attr:`.editor`).
        
        It controls wether it should save the file (ctrl-s), etc.
        
        :param keyboard: Instance of the keyboard manager.
        :param keycode: Int that represents the pressed key.
        :param scancode: Extra code (not used).
        :param value: Value of the pressed key, as a :py:obj:`str`.
        :param modifiers: List of pressed modifiers (such as 'ctrl', 'alt'...)
        """
                
        # ctrl-s to save
        if keycode == 115 and value == 's':
            if 'ctrl' in modifiers and len(modifiers) == 1:
                self.editor.save_tab()
        
        # To fix the up and down keys navigation, keycode for up key
        # is 273 and for down key is 274
        if keycode == 274:
            self.key_down()
        if keycode == 273:
            self.key_up()
    
    def key_down(self):
        """Change the scroll position if the cursor postion after
        pressing the 'down' if needed."""
        
        y_pos = self.editor.cursor_pos[1]
        line_height = self.editor.line_height
            
        traveled = math.floor(self.scroll_y * float(self.viewport_size[1] - self.height))
                                                                             
        if ( self.viewport_size[1] > traveled):
            inverse_traveled = self.viewport_size[1] - traveled
        else:
            inverse_traveled = 0
                
        inverse_y_pos =  self.viewport_size[1] - y_pos

        if (inverse_y_pos + line_height) > inverse_traveled:
            # Normalize the quantity to be between 0 and 1
            normalized = self.convert_distance_to_scroll(0, line_height)
            # Reposition the scroll
            new_scroll_y = self.scroll_y - normalized[1] 
                
            if new_scroll_y >= 0:
                self.scroll_y = new_scroll_y             
            else:
                self.scroll_y = 0       

    def key_up(self):
        """Change the scroll position if the cursor postion after
        pressing the 'up' if needed."""
        
        y_pos = self.editor.cursor_pos[1]
        line_height = self.editor.line_height
            
        traveled = math.floor(self.scroll_y 
                              * float(self.viewport_size[1] - self.height))          

        if y_pos > (traveled + self.height):
            # Normalize the quantity to be between 0 and 1
            normalized = self.convert_distance_to_scroll(0, line_height)
            # Reposition the scroll
            new_scroll_y = self.scroll_y + normalized[1] 
                
            if new_scroll_y <= 1:
                self.scroll_y = new_scroll_y             
            else:
                self.scroll_y = 1   
                
                                    
    def on_lines_change(self, widget, value):
        """Manage event when :py:attr:`editor._lines` changes
        
        Requests an update on the line numbers depending on the situation.
        
        :param widget: Instance of the :py:attr:`kivy.uix.widget` on which the event ocurred (:py:attr:`.editor`).
        :param value: Value of :py:attr:`.editor._lines` after it changed.      
        """
        
        n = len(value)
        if n > self.max_num_of_lines:
            self.update_lines_number(self.max_num_of_lines, n)

    def on_show_line_numbers(self, widget, value):
        """Manage event when :py:attr:`.show_line_numbers` changes.
        
        :param widget: :py:attr:`kivy.uix.widget` on which the event ocurred (this :py:class:`.CodeScrollView`).
        :param value: Value of :py:attr:`.show_line_numbers` after the change.
        """
        
        if value:
            max_num_l = str(self.max_num_of_lines)
            _get_extents = self.line_numbers_strip._label_cached.get_extents
            padding = self.line_numbers_strip.padding[0] * 2
            
            self.line_numbers_strip.width = (_get_extents(str(max_num_l))[0] 
                                             + padding)
        else:
            self.line_numbers_strip.width = 0

    def update_lines_number(self, old, new):
        """Update the lines number.
        
        When the number of lines increases, the line numbers should be updated
        using this method (thid method is called by :py:meth:`.on_lines_change`).
        
        :param old: Old number of lines
        :param new: New number of lines
        """
        
        self.max_num_of_lines = new
        lines = [str(i) for i in range(old + 1, new + 1)]
        self.line_numbers_strip.text += '\n'.join(lines) + '\n'
           
        max_num_l = str(self.max_num_of_lines)
        _get_extents = self.line_numbers_strip._label_cached.get_extents
        padding = self.line_numbers_strip.padding[0] * 2
        
        self.line_numbers_strip.width = (_get_extents(str(max_num_l))[0] 
                                         + padding)
        
        
class EditorContainer(TabbedPanel):   
    """Used to create a tab for a new file or load a file.
    
    This :py:class:`.EditorContainer` has tabs. Each tab 
    consists of an :py:class:`.EditorTab` and a content.
    
    The content will be a :py:class:`.CodeScrollView`.
    """

    right_click_menu = None
    """Stores the :py:class:`editorcontainer.rightclickmenu.rightclickmenu.RightClickMenu`
    to use in the application."""
          
    def __init__(self, **kwargs):
       
        super(EditorContainer, self).__init__()
       
        self.default_tab_mimetype = None
        """Stores the mimetype (of a file) of a default tab. 
        
        Used to store the mimetype of a file that is opened directly with the 
        application (from 'console'). Defaults to :py:obj:`None`.
        """
        
        self.default_tab_file_path = None
        """Stores the path (to a file) of a default tab.
        
        Used to store the path of a file that is opened directly with the application 
        (from 'console'). Defaults to :py:obj:`None`.
        """                     
       
        # Bind current_tab to disable the unused editors
        # and enable the current one.
        self.bind(current_tab=self.disable_tabs)
       
    def add_new_tab(self, mime_type=None, tab_name=None):
        """Add a new tab.
        
        The contents of the added tab depend on the mime_type and 
        tab_name. The tab is added to this :py:class:`.EditorContainer`.

        The 'text' attribute of The :py:class:`editorcontainer.editor.editor.Editor` is binded to 
        its method :py:meth:`editorcontainer.editor.editor.Editor.text_changed` if a blank new tab
        is created.
                
        :param mime_type: Mimetype of the file to open (contents of the new tab). Defaults to :py:obj:`None` if no file will be opened.
        :param tab_name: Name to put in the tab header. It's the name of the file. Defaults to :py:obj:`None`.
        :return: The created tab, an :py:class:`.EditorTab`.
        """
        
        editor_tab = EditorTab()       
        
        editor_content = CodeScrollView()
        
        editor_content.editor_container = self

        editor_tab.content = editor_content
        
        editor_tab.change_tab_name(tab_name)               
              
        #editor_tab.width = 200
         
        self.add_widget(editor_tab)
        
        editor_content.editor.tab = editor_tab
       
        #TODO Change this to 'self.switch_to(editor, do_scroll=True) 
        # when kivy 1.9.2 releases
        self.switch_to(editor_tab)

        editor = editor_tab.content.editor
            
        editor.propagate_editor_container(self)
            
        if tab_name is None:
            editor.text=' '
            editor.text=''
            editor.bind(text=editor.text_changed)
            
        self.footer_visibility()
        
        return editor_tab
   
    def disable_tabs(self, widget, value):
        """Manage the event when the current_tab changes.
        
        It enables the tab's editor to which the user changed and
        disables all others.
        """        
        
        for tab in self.tab_list:
            tab.content.editor.disabled = True
            
        widget.current_tab.content.editor.disabled = False
       
    def build_default_tab(self):
        """Build a default tab. It's a tab created when the application is opened.
        
        The default type depends on :py:attr:`.default_tab_file_path` and 
        :py:attr:`.default_tab_mimetype`. If those attributes are :py:obj:`None`
        a blank new tab will be created, otherwise a tab with the contents of
        :py:attr:`.default_tab_file_path` and highlighted for :py:attr:`.default_tab_mimetype`
        will be created.
        """
        
        self.build_tab(self.default_tab_file_path, self.default_tab_mimetype)

    def build_tab(self, file_path = None, mime_type = None):
        """Build a tab.
        
        The tab will have a path file_path and a mimetype mimetype.
        The tab name is extracted from file_path, unless it's :py:obj:`None`.This
        name is the file name, including the file extension.
        If the parameters are :py:obj:`None`, a blank new tab is created.
        
        The 'text' attribute of The :py:class:`editorcontainer.editor.editor.Editor` is binded to 
        its method :py:meth:`editorcontainer.editor.editor.Editor.text_changed` if a not blank tab
        is created.
        
        :param file_path: Path of the file to open. Defaults to :py:obj:`None`.
        :param mimetype: Mimetype of the file to open. Defaults to :py:obj:`None`.
        """
        
        text = ''
        dir_path = None
        file_name = None
        
        if file_path is not None:

            try:
                   
                with open(file_path) as file:
                    text = file.read()                            
                        
            except PermissionError as err:
                print(err, "You don't have the required access rights"
                      " to read: {0}".format(path), sep = '\n')
                
                dir_path = mime_type = file_name = file_path = None
                
            except FileNotFoundError as err:
                print(err, "{}: not found".format(file_path), sep='\n')
                
                dir_path = mime_type = file_name = file_path = None

            except IsADirectoryError as err:
                print(err, "Cannot open a directory", sep = '\n')  
                
                dir_path = mime_type = file_name = file_path = None
                                
            else:
                dir_path, file_name = os.path.split(file_path)
          
        editor_tab = self.add_new_tab(mime_type,
                         file_name)
          
        editor =  editor_tab.content.editor
            
        editor._name = file_name
        editor._path = dir_path          
        editor.text = text
 
        name = editor.change_lexer(mime_type)

        self.parent.footer.change_information({'highlight_menu': name})
                       
        editor.bind(text=editor.text_changed)
    
    def footer_visibility(self):
        """It there are no open tabs then remove the
        footer from the GUI. If not then add it"""
        
        container = self.parent
        if len(self.tab_list) == 0:
            container.remove_widget(container.footer)
        elif len(self.tab_list) == 1:
            
            if not (container.footer in container.children):      
                container.add_widget(container.footer)

    def open_right_click_menu(self, x, y):
        """Open the right click menu.
        
        The menu is added to :py:class:`kivy.core.window.Window`.
       
        :param x: x position to place the menu.
        :param y: y position to place the menu.
        """
        
        inv_y = Window.height - y
        rc_menu = self.right_click_menu
        
        if rc_menu is not None:
            rc_menu.pos = (x, inv_y - rc_menu.height)        
        else:
            rc_menu = RightClickMenu()
            rc_menu.pos = (x, inv_y - rc_menu.height)
            self.right_click_menu = rc_menu
                                
        rc_menu.editor = self.current_tab.content.editor
        
        Window.add_widget(rc_menu)
                                                                  
class EditorTab(TabbedPanelHeader):
    """Tab header of a tab to add to the :py:class:`.EditorContainer`.
    
    It will display the name of the tab (which can be the name of the file
    opened by that tab or the default, established in the related *.kv* file).
    """
    
    close_button = ObjectProperty(None)
    """An :py:class:`kivy.properties.ObjectProperty` that's a reference
    to the button to close the tab (the button is in the :py:class:`.EditorTab`).
    """
    
    close_button_string = StringProperty('x')
    """Text to display in the :py:attr:`.close_button`. 
    
    It's a :py:class:`kivy.properties.StringProperty` and defaults to 'x'.
    This attribute's value will change when a change to the text of the 
    :py:class:`editorcontainer.editor.editor.Editor` occurs and display an
    asterisk (*) on top of it.
    """
    
    label = ObjectProperty(None)
    """Label to place the name of the tab"""
    
    def __init__(self, **kwargs):
        """Calls super's __init__ and binds texture_size of
        :py:attr:`.label` to :py:meth:`.on_label_textture_size`."""
        
        super(EditorTab, self).__init__(**kwargs)
        
        self.label.bind(texture_size=self.on_label_texture_size)
        
        self.saved = True
        """Indicates if the contents of the tab were already saved (after a change).
        
        True = saved
        False = unsaved
        """
        
    def close_tab_question(self, widget, value):
        """Close the tab after using a confirmation dialog, if the answer was 'yes'.
        
        :param widget: Widget on which the event ocurred \
        (a :py:class:`confirmationdialog.confirmationdialog.ConfirmationDialog`).
        :param value: Value after the change (the value of widget.answered).
        """
        
        if value:
            self.close_editor_tab(saved=True) 
       
    def close_editor_tab(self, saved=False):
        """Close this :py:class:`.EditorTab`.

        Determines to which tab to move (if some tab is open) when this one is
        closed.
        """
        
        if self.saved == False and saved == False:
            description = 'This tab has unsaved changes'
            question = 'Do you want to close it without saving?'
            confirmation_dialog = ConfirmationDialog(description, 
                                                         question)
            confirmation_dialog.open()
            confirmation_dialog.bind(answered=self.close_tab_question)     
               
        else:
            
            parent_panel = self.parent.tabbed_panel
            
            # Save the position to change tabs
            # in theory to the one on the left
            switch_index = parent_panel.tab_list.index(self)
            
            # See if the tab was the current one
            was_current = False or (self is parent_panel.current_tab)
            
            parent_panel.remove_widget(self)
            self.content.opacity = 0
            
            tab_list = parent_panel.tab_list
            
            # Find out if it's possible to change to other tab,
            # then change to it
            tab_list_len = len(parent_panel.tab_list) 
            if(tab_list_len > 0):
            
                # It's not necessary if the tab wasn't the 'current_tab'            
                
                if was_current:
                
                    #Calculate position to switch to
                    if not switch_index == tab_list_len:
                        switch_index = switch_index % tab_list_len
                    else:
                        switch_index = tab_list_len - 1
                         
                    parent_panel.switch_to(parent_panel.tab_list[switch_index])

            # Tell the EditorContainer to remove the footer if there are no more
            # open tabs
            parent_panel.footer_visibility()
        
    def change_tab_name(self, name=None):
        """Change the name of this :py:class:`.EditorTab`. The name is what's
        displayed in the tab header (that is, this :py:class:`.EditorTab`)."""
        
        if name is not None:
            self.label.text = name
   
    def on_label_texture_size(self, widget, value):
        """Manage event when texture_size changes in :py:attr:`.label`.
        
        The width of the tab is changed accordingly to fit the tab name.
        
        :param widget: Widget on which the event ocurred (:py:attr:`.label`).
        :param value: Value of texture_size after it changed.
        """

        double_padding = 2 * self.label.padding_x
        self.label.width = self.label.texture_size[0] + double_padding
        self.width = self.close_button.width + self.label.width
   
   
   
                            
