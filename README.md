# PogoBlend

PogoBlend is an extension for making Pogostuck Custom Maps using Blender.

For guidance on installing and using the add-on see the [documentation](https://gubfs.github.io/pogo-blend/).

# Contributing

I don't know what needs to be said here, so if you experience difficulties feel free to contact 'thaguyfs' on Discord.

## Codebase

The add-on is written using Blenders Python API.

In Blender under ```Edit -> Preferences -> Interface -> Display``` you can enable 'Developer Extras' and 'Python Tooltips'. Navigate to the add-ons preferences, and now there should be a button to go to the install location, which will have all the Python files.
If you've cloned this repository, you might want to replace the add-on location with a symlink to the root of this project.

I use ``` just ``` for common commands. They've only been tested on linux.

To build the add-on to a ZIP file, you can use the command:\
``` just build-addon ```\
But that should only be necessary if you are releasing or sharing a final build.

### Dependencies

* **Blender 4.5 LTS**
* **xxHash**
* **PyYAML**

Wheels for xxHash and PyYAML can be downloaded with:
``` just download-wheels ```

## Documentation

The documentation is generated using Sphinx, and written with ReStructuredText.

To build the documentation to HTML, you can use, ``` just build-docs ```, and ``` just open-docs ``` to open to documentation in your default browser or ``` just run-docs ``` to both build and open the documentation.

### Dependencies

* **Sphinx**
* **sphinxcontrib.datatemplates**
* **furo (theme)**

You can install these dependencies using pip.
