"""
confirmationdialog
==================

**Module** : ``confirmationdialog.confirmationdialog.py``

Contains the class :py:class:`.ConfirmationDialog`, used to show
a confirmation dialog.
"""

from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty

import os

class ConfirmationDialog(Popup):
    """A popup that shows a confirmation dialog.
    
    Used to ask a question that can be answered with yes/no (True/False). 
    """
    
    yes_button = ObjectProperty(None)
    """:py:class:`kivy.uix.button.Button` used to give a positive answer (:py:attr:`.answered` =True)."""

    description_label = ObjectProperty(None)
    """:py:class:`kivy.uix.label.Label` used to write the description of the :py:class:`.ConfirmationDialog`."""
        
    question_label = ObjectProperty(None)
    """:py:class:`kivy.uix.label.Label` used to write the question of the :py:class:`.ConfirmationDialog`."""

    cancel_button = ObjectProperty(None)
    """:py:class:`kivy.uix.button.Button` to close the popup."""    
    
    answered = BooleanProperty(None)
    """Save the answer for the :py:attr:`.ConfirmationDialog`."""
    
    def __init__(self, desc, quest, **kwargs):
        super(ConfirmationDialog, self).__init__(**kwargs)
        self.description_label.text = desc
        """Description text for the :py:attr:`.description_label`."""
        
        self.question_label.text = quest
        """Question text for the :py:attr:`.question_label`."""
                           
    def cancel(self):
        """Manage the event (on_release) when :py:attr:`.cancel_button` is clicked.
        
        Closes the popup (and the widgets inside it).
        """
        
        self.dismiss()        
        
    def answer(self, widget):
        """Change the value of :py:attr:`.answered` according to the answer
        given in the confirmation dialog."""
        
        if widget == self.yes_button:
            self.cancel()
            self.answered = True
        else:
            self.cancel()
            self.answered = False
    
