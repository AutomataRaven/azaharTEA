"""Module that contains the function :py:func:`.load_all_kv_files`.

Used for loading *.kv* files.
"""

import os
import re

from kivy.lang import Builder

def load_all_kv_files(start="."):
    """Loads all the *.kv* files in the directories trees
    starting from *start*.
    
    It loads the files recursively in depth first order. This
    way the style can be divided in separate modules. It's in depth
    first order so the outer files don't used undefined widgets classes.
    
    This means that implemented new widgets should be in a deeper directory
    than the files that use them.
    
    :param start: Root path to start adding files (the files are not added starting from \
    here, because they are added depth first, so the root (*start*) is added last).
    """
    pattern = re.compile(r".*?\.kv")
    kv_files = []
    for root, dirs, files in os.walk(start, topdown=False):
        kv_files += [root + "/" + file_ for file_ in files if pattern.match(file_)]

    for file_ in kv_files:
        print(file_)
        Builder.load_file(file_)
