import sys
import os
import glob

def check_or_create_folder(name):
    if os.path.isdir(name):
        return
    os.makedirs(name + "/")