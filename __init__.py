import importlib
import os

modules = []
for root, dirs, files in os.walk(os.path.dirname(__file__)):
    if "__pycache__" in root or ".git" in root:
        continue
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension != ".py":
            continue
        if file == "__init__.py":
            continue
        if filename in locals():
            importlib.reload(locals()[filename])
            modules.append(locals()[filename])
            # print(f"reloaded: {filename}")
        else:
            rel = root.split("/pogo_blend")[1].replace("/", ".")
            rel = f"{rel}.{filename}"
            locals()[filename] = importlib.import_module(rel, package=__name__)
            modules.append(locals()[filename])
            # print(f"loaded: {filename}")


def register():
    for module in modules:
        register = getattr(module, "register", None)
        if callable(register):
            module.register()


def unregister():
    for module in modules:
        unregister = getattr(module, "unregister", None)
        if callable(unregister):
            module.unregister()
