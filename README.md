# PogoBlend

PogoBlend is an extension for making Pogostuck Custom Maps using Blender.

For guidance on installing and using the add-on see the [documentation](www.example.org).

# Contributing

I don't know what needs to be said here, so if you experience difficulties feel free to contact 'thaguyfs' on Discord.

## Codebase

The add-on is written using Blenders Python API.

In Blender under ```Edit -> Preferences -> Interface -> Display``` you can enable 'Developer Extras' and 'Python Tooltips'. Navigate to the add-on preferences, and now there should be a button to go to the install location, which will have all the Python files.
If you've cloned this repository, you might want to replace the add-on location with a symlink to the 'addon' directory in this project.

To build the add-on to a ZIP file, you can use the command:\
``` blender --command extension build --source-dir addon --output-dir build --split-platforms ```\
But that should only be necessary if you are releasing or sharing a final build.

In the ```addon/__init__.py``` file, there is some commented out text, that when uncommented will reload all modules in the add-on, when reloading scripts from Blender, so you don't have to restart Blender on every change. Blender will normally only reload the ```__init__.py``` file otherwise.

### Dependencies

* **Blender 4.5 LTS**
* **xxHash**
* **PyYAML**

Python Wheels for xxHash and PyYAML is distributed along with the addon, so all you should need to start changing/adding to the codebase is Blender (and a text editor/IDE I suppose).

## Documentation

The documentation is generated using Sphinx, and written with ReStructuredText.

To build the documentation to HTML, use the provided make file, or make.bat on Windows. I find it easiest to include ``` SPHINXOPTS="-E" ``` to remake all files, because otherwise the datatemplates or content tree might become unsynced:\
``` make html SPHINXOPTS="-E" ```

### Dependencies

* **Sphinx**
* **sphinxcontrib.datatemplates**
* **furo (theme)**

You can install these dependencies using pip.