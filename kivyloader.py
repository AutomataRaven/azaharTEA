import os
import re

from kivy.lang import Builder

def load_all_kv_files(start="."):
    pattern = re.compile(r".*?\.kv")
    kv_files = []
    for root, dirs, files in os.walk(start):
        kv_files += [root + "/" + file_ for file_ in files if pattern.match(file_)]

    for file_ in kv_files:
        print(file_)
        Builder.load_file(file_)
