# Agenzig

This is a project to build a text-based adventure game engine in Python. By engine, I mean that without changing a line of code, a user could create their own interactive adventure which could then be played with the script. This is achieved with the ConfigObj module (an improved version of the built-in ConfigEditor module) which allows Python to read human-readable data using the standard .ini file structure.

This branch is dedicated to the fragmenting by object-orientation of the main script. It's placement in a branch is in-line with the drastic overhaul and subsequent reduced stabiltiy this entails.

In addition I intend to utilise external programs - specifically a graphics viewer and an audio player - to allow adventure writers/creators to include graphical and audio content which will be displayed/played when appropriate to complement the text

## Implemented Features

Scenes are loaded and the prompt is presented so the script is very much useable and will not crash (unless files are missing). However features are somewhat limited.
- Basic, semi-random character creation method (alpha.py)
- Printing scenes
- Printing available choices (that your character meets the requirements for)
- Making a choice (with limited effects) by typing the exact text of the choice
- Using inventory items with effects including equipping equipment and changing the scene
- Printing character inventory
- Printing character status (text descriptions of health, fatigue and attributes)
- Printing character equipmentcan be displayed. 
For a list of commands enter 'help' into the prompt.

## Roadmap

- Unequiping items
- More commenting
- Granting the ability to change scene and scene states as an item effect
- Improve equipment slot system
- Implement the ability to make choices
- Allow equipment to grant abilities, armor and attribute boosts
- Implement non-combat abilities
- Add a new character creation technique
- Implement combat

## Installation/Use

Firstly, the script was made for Python 2.7.2. Little problem should be had with other 2 versions, but it is likely the script will fail completely when put through the 3 interpreter.

Secondly, ConfigObj is required. The download comes with an installation script but it's easier to use EasyInstall which is part of the setuptools package. First download the correct setuptools installer from here: http://pypi.python.org/pypi/setuptools. Once installed, run Python.exe and type: "easy_install configobj"
This will automatically download and install the ConfigObj module

From a fresh installation, running agenzig.py will load the alpha testing adventure - Murderous Monastery. It's human-readable data files are contained within the folder Murderous Monastery in the folder Adventures.
Editing the files (e.g. Main.agez or scenes.agez) will directly alter the adventure.
If you want to try and create your own adventure, then duplicate and rename the Murderous Monastery folder. It will now appear as an option when you run agenzig.py.

## License

Copyright Thomas Sturges-Allard. 
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. http://creativecommons.org/licenses/by-nc-sa/3.0/

Makes use of the ConfigObj Python module by Michael Foord and Nicola Larosa which can be found here: http://www.voidspace.org.uk/python/configobj.html