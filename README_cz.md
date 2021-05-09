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
- kreslení zahájíte tlačítkem "Draw"
- nakreslete pouze jednu čáru a stiskněte "Done"
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
- renderování může chvíli trvat a Blender se může nečekaně ukončit (například z důvodu nedostatku výpočetní nebo paměťové kapacity), proto doporučuji uložit scénu před renderováním
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/render.gif)

### Získávání nových 3D modelů
#### Jak má model vypadat
- model musí mít počátek (origin) na spodu, jinak bz doch8yelo k pr;niku model;m se stěnou
- model by se měl nacházet na souřadnicích X: 0 Y: 0 Z: 0
- model by měl mít rozumnou velikost vzhledem k reálnému světu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/origin_fix.gif)
#### Importování
- Blender podporuje importování formátů .obj .stl a .fbx 
- pokud máte 3D model v jiném formátu, je velice pravděpodobné, že se vám podaří najít online převaděč do jednoho z těchto formátů
- nejjednoduší cesta jak získat nové modely je stáhnout je z internetu
- také je možnost dotázat se lezeckého centra o poskytnutí modelů
#### Mesh
- modelování je složité a učení může trvat roky, proto budu demostrovat jednoduché věci krok po kroku
- všechny klávesové zkratky, které použiji můžete vidět v leveém dolním rohu
- stiskněte tlačítko Prepare empty scene v záložce rozšíření a poté přidejte plochu (shift + A -> Mesh -> Plane)
- vyberte plochu a tabulátorem se přesuňte do editačního módu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/mesh_modelling1.gif)
- nyní můžete vybrat vrchol, hranu nebo plochu a upravit je
- běžné operace jsou rotace (R), zvětšení (S), posunutí (G) a vysunutí (E)
- operaci potvrdíte levým tlačítkem myši nebo zrušíte pravým
- stisknutí kláves X, Y, Z při aktivované operaci nastaví směr pohybu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/mesh_modelling2.gif)
- když máte model hotový stiskněte A pro vybrání všech bodů a G + Z, myší posuňte model tak aby všechny body byly nad oranžovým bodem a potvrďte
- na konec se přesuňte zpět do objektového módu tabulátorem
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/mesh_modelling3.gif)
#### Boolean
- na počátku musíte mít nějaký obejkt, například kostku (shift + A -> Mesh -> Cube)
- nyní můžete přidat další objekty a odečíst je nebo přičíst
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/boolean_modelling1.gif)
- na konci musíte potvrdit všechny modifikátory
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/boolean_modelling2.gif)
- zkontroluje jestli model upspokojuje požadavky zmíněné výše
#### Sochání
- vhodné pro skály a modely s organickým vzhledem
- na začátku musíte mít nějaký objekt, například kostku (shift + A -> Mesh -> Cube)
- přidáte modifikátor pro rozdělení povrchů a aplikujete jej
- nyní se přesuňte do sculpt módu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/sculpting1.gif)
- vysochejte tvar pomocí dostupných nástrojů
- přesuňte se zpět do objektového módu
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/sculpting2.gif)
- vysochaný povrch není nikdy perfektně rovný, proto je dobré na konec odečíst kostku a tím zarovnat povrch (více v Boolean modelování)
![](https://github.com/vk-5/RouteSetter/blob/master/gifs/sculpting3.gif)
- zkontroluje jestli model upspokojuje požadavky zmíněné výše
#### Fotogrametrie
- složitá technika, která umožňuje vytvořit modely z fotek reálného světa
- je zapotřebí mít dobrý foťák a pro velké objekty jako jsou skály také dron



