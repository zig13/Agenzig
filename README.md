# Agenzig

This is a project to build a text-based adventure game engine in Python. By engine, I mean that without changing a line of code, a user could create their own interactive adventure which could then be played with the script. This is achieved with the ConfigObj module (an improved version of the built-in ConfigEditor module) which allows Python to read human-readable data using the standard .ini file structure.

In addition I intend to utilise external programs - specifically a graphics viewer and an audio player - to allow adventure writers/creators to include graphical and audio content which will be displayed/played when appropriate to complement the text

## Progress

Scenes are loaded and the prompt is presented so the script is very much useable and will not crash (unless files are missing). However features are somewhat limited. Making choices, fighting and using inventory items are not yet implemented. However, character inventory and status (text descriptions of health, fatigue and attributes) can be displayed. For a list of commands enter 'help' into the prompt.

## Installation/Use

Firstly, the script was made for Python 2.7.2. Little problem should be had with other 2 versions, but it is likely the script will fail completely when put through the 3 interpreter.

Secondly, ConfigObj is required. The download comes with an installation script but it's easier to use EasyInstall which is part of the setuptools package. First download the correct setuptools installer from here: http://pypi.python.org/pypi/setuptools. Once installed, run Python.exe and type: "easy_install configobj"
This will automatically download and install the ConfigObj module

With ConfigObj installed, running agenzig.py with the various .agez files in the same directory will run the engine with the default included story 'Murderous Monastery'.

Straight editing the .agez files will work fine but it's safer to setup multiple adventures. To do this move the .agez files into a folder called Murderous Monastery inside a folder called 'Adventures'. Then duplicate the Murderous Monastery folder and rename it. Now when you run agenzig.py, it will ask which of the TWO adventures you wish to run.

Basically the script first checks if there is a file called 'Main.agez' in the same folder as it. If there is, it will load along with the other .agez files the script needs (which it now presumes are there also). If not, it will check to see if there are any sub-folders within the folder 'Adventures'. If there are, it will presume they contain .agez files and will list them as options.

## License

Copyright Thomas Sturges-Allard. 
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. http://creativecommons.org/licenses/by-nc-sa/3.0/

Makes use of the ConfigObj Python module by Michael Foord and Nicola Larosa which can be found here: http://www.voidspace.org.uk/python/configobj.html