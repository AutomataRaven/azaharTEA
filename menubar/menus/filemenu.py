"""
filemenu
========

**Module** : ``menubar.menus.filemenu.py``

Contains classes for the menus that go in the menubar.
"""

from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty

from menubar.menus.filechoosers.savedialog import SaveDialog
from menubar.menus.filechoosers.opendialog import OpenDialog


class FileMenu(Spinner):
    """Menu to show options related to file manipulation.
    
    The options can increase, but the minimum options should be:
        * New File
        * Open File
        * Save
        * Save as
    """
    
    #TODO find a way to group values and FM_events in a single 
    # structure.
    values = ListProperty(['New File', 'Open File', 'Save', 'Save As'])
    """:py:class:`kivy.properties.ListProperty` used to store the different options
    of this :py:class:`.FileMenu`"""
    
    def __init__(self, **kwargs):
    
        super(FileMenu, self).__init__(**kwargs)
        self.FM_events = {
                            
            'Save As': self.save_as, 
            'New File': self.open_new_tab,
            'Open File': self.open_file_tab,
            'Save': self.save_all
        }
        """Dictionary (:py:obj:`dict`) used to store the name of the menu (the *key*)
        and the method for that option (the *value*)."""
    
    def _on_dropdown_select(self, instance, value):
        """Manage the event when an option of the dropdown for this :py:class:`.FileMenu`
        is selected.
        
        The action to take is selected using value as the *key* for :py:attr:`FM_events`, because
        the method to manage the "value" option should be the *value* of :py:attr:`FM_events`.
        
        :param instance: Instance of the widget on which the event occured.
        :param value: Text of the selected option from this :py:class:`.FileMenu` \
        (something like "New File", "Open File", etc. Some of the values inside \
        :py:attr:`.values`).
        """
        self.is_open = False
        
        try:
            self.FM_events[value]()
        except KeyError as err:
            
            print(err,'{}: no such option defined'.format(value), sep='\n')
   
    def save_as(self):
        """Manage the event when the option "Save As" of :py:attr:`.values` is selected.
        
        This method is called with :py:attr:`.FM_events` using the text selected as the
        *key*.
        
        It shows a :py:class:`menubar.menus.filechoosers.savedialog.SaveDialog` to save
        a file.
        """
        
        save_dialog = SaveDialog()
        save_dialog.to_save(self.editor_container.current_tab)
        save_dialog.open()
     
    def save_all(self):
        """Manage the event when the option "Save" of :py:attr:`.values` is selected.
        
        This method is called with :py:attr:`.FM_events` using the text selected as the
        *key*.
        
        It iterates over the open tabs and saves the changed tabs if those tabs were already
        saved (because such tabs have a path to the file set).
        """
        tabs = self.editor_container.tab_list
        
        for tab in tabs:
            tab.content.editor.save_tab(True)
          
    def open_new_tab(self):
        """Manage the event when the option "New File" of :py:attr:`.values` is selected.
        
        This method is called with :py:attr:`.FM_events` using the text selected as the
        *key*.
        
        Tells the :py:class:`editorcontainer.editorcontainer.EditorContainer` (should be a
        reference to :py:attr:`azaharTEA.Container.editor_container`) to open a new tab.
        """
        
        self.editor_container.build_tab()

    def open_file_tab(self):
        """Manage the event when the option "Open File" of :py:attr:`.values` is selected.
        
        This method is called with :py:attr:`.FM_events` using the text selected as the
        *key*.
        
        Tells the :py:class:`editorcontainer.editorcontainer.EditorContainer` (should be a
        reference to :py:attr:`azaharTEA.Container.editor_container`) to open a tab for a file
        by showing a filechooser.
        """
        open_dialog = OpenDialog()
        open_dialog.propagate_editor_container(self.editor_container)
        open_dialog.open()
             
    def propagate_editor_container(self, editor_container):
        """Propagate the :py:class:`editorcontainer.editorcontainer.EditorContainer`
        to this :py:class:`.FileMenu`.
        
        :param editor_container: :py:class:`editorcontainer.editorcontainer.EditorContainer` \
        to propagate to this :py:class:`.FileMenu`. It should be a reference to \
        :py:class:`azaharTEA.Container.editor_container`.
        """
        self.editor_container = editor_container
 
 
class SeeMenuDropDown(DropDown):
    """DropDown for the :py:class:`.SeeMenu`."""
    
    line_numbers_checkbox = ObjectProperty(None)
    """:py:class:`kivy.properties.ObjectProperty` to store the checkbox for 
    the "See Line Numbers" option of the :py:class:`.SeeMenu`."""
    
    
class SeeMenu(Spinner):
    """Menu to show options related to GUI elements that can be
    shown or hidden.
    
    The options can increase, but the minimum options should be:
        * See line numbers
    """
    
    def __init__(self, **kwargs):
        
        super(SeeMenu, self).__init__(**kwargs)   
         
        self.drop_down = SeeMenuDropDown()
        """:py:class:`.SeeMenuDropDown` to contain the options for this
        :py:class:`.SeeMenu`."""
    
    def open_menu(self, widget):
        """Display :py:attr:`.drop_down`.
        
        It binds the :py:attr:`.SeeMenuDropDown.line_numbers_checkbox` 
        of :py:attr:`.drop_down` with :py:meth:`.on_checkbox_active`.
        
        :param widget: Widget on which the event ocurred \
        (:py:attr:`.SeeMenuDropDown.line_numbers_checkbox`). Not used.
        """
        
        self.drop_down.open(self)
        self.drop_down.line_numbers_checkbox.bind(active=self.on_checkbox_active)
        
      
    def on_checkbox_active(self, widget, value):
        """Manage the event when :py:attr:`.SeeMenuDropDown.line_numbers_checkbox` 
        of :py:attr:`.drop_down` with :py:meth:`.on_checkbox_active` changes (the checkbox is
        selected or deselected).
        
        Sets the :py:attr:`editorcontainer.editorcontainer.CodeScrollView.show_line_numbers` 
        to value. If value == :py:obj:`True` the lines be display, if not, the lines should
        hide.
        
        :param widget: Widget on which the event ocurred (:py:attr:`.drop_down.line_numbers_checkbox`).
        :param value: Value of :py:attr:`.drop_down.line_numbers_checkbox.active` after the change.
        """
        tab_list = self.editor_container.tab_list
        
        for tab in tab_list:
            tab.content.show_line_numbers = value
                         
    def propagate_editor_container(self, editor_container):
        """Propagate the :py:class:`editorcontainer.editorcontainer.EditorContainer`
        to this :py:class:`.SeeMenu`.
        
        :param editor_container: :py:class:`editorcontainer.editorcontainer.EditorContainer` \
        to propagate to this :py:class:`.SeeMenu`. It should be a reference to \
        :py:class:`azaharTEA.Container.editor_container`.
        """
            
        self.editor_container = editor_container   
