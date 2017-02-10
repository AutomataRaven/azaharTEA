from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from menubar.menus.filemenu import FileMenu

class MenuBar(BoxLayout):
   
    action_view = ObjectProperty(None)    

