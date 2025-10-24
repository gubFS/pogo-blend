import os
import importlib

if "bpy" in locals():
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        if "__pycache__" in root or ".git" in root: continue
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension != ".py": continue
            if file == "__init__.py": continue
            if filename in locals():
                importlib.reload(locals()[filename])
                print(f"reloaded: {filename}")
            else:
                rel = root.split("/pogo_blend")[1].replace("/", ".")
                rel = f"{rel}.{filename}"
                locals()[filename] = importlib.import_module(rel, package=__name__)
                print(f"loaded: {filename}")

import bpy
from . import pogo_blend

def register():
    pogo_blend.register()

def unregister():
    pogo_blend.unregister()

