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
- this panel is useful for all three scenarios
- I recommend leaving this panel visible.
#### Prepare new scene
- removes all objects, materials, collections etc.
- prepares collection hierarchy 
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/prepare_new_scene.gif)
#### Move
- moves selected object
- snaps to surface of another object
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/move.gif)
#### Rotate
- rotates selected object based on mouse movement
- rotates in Z axis
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/rotate.gif)
#### Scale
- changes size of selected object based on mouse movement
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/scale.gif)
#### Delete
- deletes selected object
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/delete.gif)
#### Assign materials
- assigns material by color of collection
- useful when you change holds collection and want to see actual color based on collections
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/assign_materials.gif)
#### Documentation
- opens this documentation page

### Climbing wall and Rock
- in these panels the funcionality is almost similar
- they contain collections of 3D models
- you can manage these collections by Save and Remove buttons
#### Add
- adds selected model from collection
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_from_collection.gif)
#### Save
- saves selected object in collection
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_hold.gif)
#### Remove
- removes selected object from collection
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/remove_hold.gif)
#### Add collection
- at the beginning holds are inserted into collection named "route" and drawn path is inserted into "path" collection
- by this button you can add new collections and choose which you want to insert into
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_collection.gif)
#### Draw path and Done
- these two buttons serves for marking path
- you have to start drawing by Draw path button
- remember to draw only one line and press Done
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/draw_done.gif)

### Rope
#### Add carabiner
- adds carabiner 
- similar to Add button from climbing wall 
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_carabiner.gif)
#### Add point
- adds points
- similar to Add carabiner
- points are useful when you need to set the rope further from the carabiners or when the rope is going through the wall
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_point.gif)
#### Generate rope
- generates rope through carabiners and points
- order depends on table above
- generating may take a while and for longer ropes Blender can crash, saving file before generating rope is highly recommended
- if you are not happy with the result, go back by Undo (ctrl + z) before generating the rope otherwise issues can appear due to Blender Undo modification limits
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/generate_rope.gif)
#### Intersection
- highlights intersection of rope and wall
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/intersection.gif)
#### Up and Down arrow
- change order carabiners
- rope generating depends on order of carabiners and helpers
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/change_order.gif)
#### Select
- selects all needed parts of the carabiner
- carabiner consists of many parts because of physical simulation
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/select_whole_carabiner.gif)
#### Remove
- remove all parts of the carabiner
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/remove_whole_carabiner.gif)
#### Play animation
### Render
- choose collection you want to render
- press render button and waint until render is finished
- rendering may take a while and for bigger scenes Blender can crash, saving file before rendering is highly recommended
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/render.gif)
### Obtaining new 3D models
#### How model should look like
- model has to have the origin at the bottom otherwise parts would go through the wall 
- model should be located in the middle of the scene at coordinates X: 0 Y: 0 Z: 0
- model should have some reasonable size based on real holds, walls etc
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/origin_fix.gif)
#### Importing
- Blender supports importing of .obj .stl and .fbx file formats
- if you have any 3D model which is in another format, it is very likely you will find a converter of 3D model formats
- the simplest way of obtaining new 3D model is downloading it from the internet
- you can also try asking some climbing center to provide you 3D design of their wall
#### Mesh modelling
- modelling is hard and can take years to learn properly so I will demonstate only easy step by step example, you can see all shortcuts I used in bottom left corner
- press Prepare empty scene button in addon menu and add plane (shift + A -> Mesh -> Plane)
- with plane selected press Tab on keyboard to switch to edit mode
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/mesh_modelling1.gif)
- now you can edit mesh as you like by selecting some vertices, edges or faces
- common operations are rotation, moving, scaling and extruding
- keyboard shortcuts are rotation (R), moving (G), scaling (S) and extruding (E)
- when you start the operating it can be approved by left button on mouse or canceled by right button on mouse
- you can also press X, Y or Z when the operation is active to set the direction
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/mesh_modelling2.gif)
- when you are done with editing pres A to select all, then press G and Z and put your mesh all the way above its origin (orange point)
- at the end press Tab again to get to object mode also check if your model meets the requirements mentioned above
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/mesh_modelling3.gif)
#### Boolean modelling
- you have to have some object at the beggining, for example cube (shift + A -> Mesh -> Cube)
- now you can add another cubes, spheres etc, position them and subtract them from the first one
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/boolean_modelling1.gif)
- at the end you have to apply all modifiers
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/boolean_modelling2.gif)
- check if your model meets the mentioned requirements
#### Sculpting
- suitable for rocks and holds with organic look
- you have to have some object at the beggining for example cube (shift + A -> Mesh -> Cube)
- add subdivision surface modifier and apply it
- now switch to sculpt mode
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/sculpting1.gif)
- sculpt your desired shape with available brushes
- switch back to object mode
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/sculpting2.gif)
- sculpted surfaces are never perfectly flat, so it is good to subtract cube at the bottom to make it flat (see Boolean modelling)
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/sculpting3.gif)
- check if your model meets the mentioned requirements
#### Photogrammetry
- complex technique of getting real world objects into 3D scene
- this technique can be useful for creating rocks from real world
- good camera is a required and for big rocks you need drone or plane



