# RouteSetter

[EN documentation](README.md)

## Instalace
### Instalace Blenderu
- Blender je možné stáhnout z https://www.blender.org/.
- Pokud je aktuální verze větší než 2.93, stáhněte 2.93 LTS verzi z https://www.blender.org/download/lts/.
- Rozšíření bylo vyvíjeno od verze 2.90.0 a bylo otestováno na aktuální verzi 2.92.0 a 2.93.0 LTS Experimental build (stabilní verze 2.93.0 LTS vyjde během Května) stáhnutelné z https://builder.blender.org/download
### Instalace rozšíření
- Stáhněte [rozšíření](RouteSetter.zip) z repozitáře (soubor RouteSetter.zip)
- Otevřete Blender
- Běžte do Edit -> Preferences -> Add-ons
- Zvolte tlačítko 'Install...'
- Vyberte stáhnutý soubor s rozšířením
- Klikněte na tlačítko 'Install Add-on'
- Nyní byste měli vidět rozšíření v seznamu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/instalation1.gif)
- Povolte rozšíření zaškrtnutím políčka
- Nyní je rozšíření nainstalované a povolené
- Rozšíření najdete v 'N panelu' v '3D viewport'
- '3D viewport' je základní obrazovka s 3D scénou a stiknutí tlačítka N na klávesnici společně s kurzorem v 3D vieportu zobrazí 'N panel'
- Ve vertikálních záložkách najděte a otevřte RouteSetter
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/instalation2.gif)

## Postup práce
### Blender

Pokud jste začátečník v Blenderu, stačí vám znát základní ovládání.
- Pohyb myši spolu se stisknutým kolečkem rotuje pohled
- Pohyb myši spolu se stisknutým kolečkem a klávesou Shift posune pohled
- Objekt vyberete levým tlačítkem myši
- Pokud držíte klávesu Ctrl můžete vybrat několik objektů
- Kliknutím do prostoru 3D scény zrušíte výběr
- Svou práci můžete uložit klávesovou zkratkou Crtl + S nebo File -> Save / Save As
- Odkaz na dokumentaci Blenderu https://www.blender.org/support/tutorials/

### Rozšíření

První věc, kterou musíte udělat je stisknout tlačítko "Prepare new scene". 
To vyčistí 3D scénu a připravý kolekce 

Když je scéna připravená nastává pět možnosti:
1) Navrhnout cesty na horolezecké stěně
2) Označit cesty na skále
3) Nastavit karabiny, zkontrolovat průnik lana se stěnou a simulovat pád
4) Vymodelovat vlastní model a umístit ho do některé z knihoven
5) Přidat a napozicovat postavu pro lepší představu rozměrů ostatních modelů

Když se rozhodnete, kterou z možností využijete, doporučuji schovat ostatní části rozšíření kliknutím na jejich jména a tím zvýšit přehlednost.
Když skončíte s prací běžte do záložky render a vyberte kolekci, kterou chcete vyrenderovat.
Render uložíte klávesovou zkratkou Crtl + S ne Image -> Save / Save As v okně renderu.

## Funkcionalita

### Edit
- tento panel je užitečný pro všechny možnosti využití, proto doporučuji nechat panel viditelný
#### Prepare new scene
- odstraní všechny obejkty, materiály, kolekce etc.
- ppřipraví hierarchii kolekcí 
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/prepare_new_scene.gif)
#### Move
- přesune vybrané objekty
- přichytává se k povrchu jiných objektů
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/move.gif)
#### Rotate
- otočí vybrané objekty na základě pohybu myši
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/rotate.gif)
#### Scale
- změní velikost vybraných objektů na základě pohybu myši
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/scale.gif)
#### Delete
- smaže vybrané objekty
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/delete.gif)
#### Assign materials
- nastaví materiály objektům, podle jejich barvy kolekce
- užitečné při přesunutí úchytu do jiné kolekce
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/assign_materials.gif)
#### Documentation
- otevře stránku s dokumentací

### Climbing wall and Rock
- funkcionalita v těchto panelech je podobná
- obsahují kolekce 3D modelů, které je možné upravovat pomocí tlačítek Save a Remove
#### Add
- přidá vybraný model z kolekce
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_from_collection.gif)
#### Save
- uloží vybraný model do kolekce
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_hold.gif)
#### Remove
- odstraní vybraný model z kolekce
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/remove_hold.gif)
#### Add collection
- na začátku se úchyty přidávají do kolekce "route" a označení cesty na skále do kolekce "path"
- tímto tlačítkem můžete přidat další kolekce nebo změnit kolekci do které chcete model přidat
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_collection.gif)
#### Add marker
- přidá označení pro počáteční a koncový úchyt
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_marker.gif)
#### Diameter, Draw path and Done
- tyto dvě tlačítka slouží pro označení cesty na skále
- kleslení zahájíte tlačítkem "Draw"
- nakleslete pouze jednu čáru a stiskněte "Done"
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/draw_done.gif)
- na posuvníku můžete nastavit průměr označení
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/draw_diameter.gif)

### Rope
#### Add carabiner
- přidá karabinu 
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_carabiner.gif)
#### Add point
- přidá pomocné body
- hodí se, když lano prochází stěnou nebo když chcete umístit konec lana dál od karabiny
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/add_point.gif)
#### Generate rope
- vygeneruje lano pospojováním bodů a karabin
- pořadí závisí na tabulce a jde měnit
- generování může chvíli trvat a Blender se může nečekaně ukončit, proto doporučuji uložit scénu před generováním
- pokud nejste spokojeni s výsledkem vraťte se pomocí klávesové zkratky Ctrl + z před generování, jinak můžou nastat problémy kvůli limitacím Blenderu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/generate_rope.gif)
#### Intersection
- znázorní průnik lana se stěnou
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/intersection.gif)
#### Up and Down arrow
- změní pořadí karabin
- generování lana závisí na pořadí
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/change_order.gif)
#### Select
- vybere všechny části karabiny
- krabina se skládá z mnoha částí kvůli fyzikální simulaci
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/select_whole_carabiner.gif)
#### Remove
- odstraní všechny části karabiny
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/remove_whole_carabiner.gif)
#### Play simulation
- spustí/zastaví fyzikální simulaci
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/simulation.gif)
#### Human reference
- posuvník nastaví výšku člověka
- napozicujte postavu v pose módu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/human1.gif)
- nastavte kosti
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/posing.gif)
- po skončení se přepněte zpět do objektového módu

### Render
- vyberte kolekci pro renderování
- stiskněte tlačítko render a počtejte než výpočet skončí
- to může trvat déle a Blender se může neočekávaně zavřít
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



