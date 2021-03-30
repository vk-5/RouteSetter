# RouteSetter

## Installation
### Blender installation
- You can download and install Blender on https://www.blender.org/.
- Add-on was developed on version 2.92.0 and will be transfered to 2.93 long term support version as soon as it released.
- If actual version of blender is higher than 2.93, donwload 2.93 LTS version from here https://www.blender.org/download/lts/.
### Addon installation
- --- Cant upload so big file (rocks, holds etc..) so instead of Download 'RouteSetter.zip' from gitHub do:
- --- Download whole repo as zip, unzip the dir. Now you should have directory RouteSetter-master with addon files (.py files and more dictionaries)
- --- If you have for example RouteSetter-master/RouteSetter-master/ addon files remove one dir from the path, it is caused by unzip.
- --- Cosmetic thing rename RouteSetter-master to 
- --- Now zip the whole RouteSetter directory again and continue
- Open Blender
- Go to Edit -> Preferences -> Add-ons
- Click on 'Install...'
- Choose downloaded add-on file 
- Click on 'Install Add-on'
- Now you should see your addon in addon list
- Enable add on by check box
- Now you have installed and enabled addon
- You can find addon tab in 'N panel' of '3D viewport'
- '3D viewport' is the default viewport when you start Blender, by pressing N on you keyboard you hide/unhide 'N panel'
- Now when you are in right viewport by pressing N on you keyboard you unhide 'N panel'
- You should see some vertical tabs and one of them should be RouteSetter, probably the last one
- Click on the tab and you are ready to build
- Happy route setting!

## Workflow
### Blender

If you are absolute beginer in Blender all you need before you start are just few things about the scene.
- By holding your middle button on mouse and move your mouse your view will rotate
- By holding your middle button and shift key on keyboard your view will move
- By clicking on an object by your left mouse button, the object will become selected
- By clicking on an object by your left mouse and holding ctrl key on keyboard, you can select more objects
- By clicking somewhere else all objects will become unselected
- You can save your scene by pressing Crtl + S or go to File -> Save / Save As
- Blender has its own documentation https://www.blender.org/support/tutorials/

### Add-on

First thing you need to do every time is clicking on the first button called "Prepare new scene". 
The reason of this is that Blender opens with default cube and other mess, so we need to clean it up and prepare Collections.

Now when your screen is prepared you have three possibilites what you can do:
1) Design a climbing wall with multiple routes in Boulder panel
2) Create a path on a real rock in Rock panel
3) Set up carabiners on wall or rock and simulate a fall of a climber, then you can see if carabiners are well placed in References panel

When you decide what you want to do I recommend you to hide the other two panels by clicking on the small arrow next to the name of the panel.
All features all described in Features section below.
When you are done with whatever you have choosed and you want to see result of you work, go to Render tab, select collection which you worked with and press render. 
You can save your render by pressing Crtl + S or go to Image -> Save / Save As in render window.

## Features
### Edit
Prepare new scene
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/prepare_new_scene.gif)
### Boulder
### Rock
### References
### Render


