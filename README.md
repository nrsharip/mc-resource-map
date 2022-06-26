
## Overview:
The purpose of this tool is to find and visualize the most optimal position for the maximum yield of a particular ore/resource using the [Ore Drilling Plants](https://ftb.fandom.com/wiki/Ore_Drilling_Plant).
This tool is used in conjuction with [GTVeinInfo](https://github.com/Techlone/GTVeinInfo) for the [GregTech](https://ftb.fandom.com/wiki/GregTech) modification of [Minecraft](https://www.minecraft.net/).

The following are the parameters of a specific [Ore Drilling Plant](https://ftb.fandom.com/wiki/Ore_Drilling_Plant) tiers (see [draw_map.py](draw_map.py#L70)):
- Ore Drilling Plant I   - radius is 48 blocks
- Ore Drilling Plant II  - radius is 64 blocks
- Ore Drilling Plant III - radius is 96 blocks
- Ore Drilling Plant IV  - radius is 144 blocks

## Screenshots
<!-- https://stackoverflow.com/questions/14494747/add-images-to-readme-md-on-github -->
<!-- <td><img src="https://github.com/nrsharip/iss-web/blob/master/prtsc/prtsc_0002.png?raw=true" width="25%"></td> -->

<table>
<tr>
  <td><img src="copper_tetrahedrite.png?raw=true" width="100%"></td>
  <td><img src="copper_tetrahedrite_redstone_sapphire_1.png?raw=true" width="100%"></td>
  <td><img src="copper_tetrahedrite_redstone_sapphire_2.png?raw=true" width="100%"></td>
  <td><img src="mars_tung_1.png?raw=true" width="100%"></td>
</tr>
<tr>
  <td><img src="mars_tung_2.png?raw=true" width="100%"></td>
  <td><img src="mars_tung_3.png?raw=true" width="100%"></td>
  <td><img src="mars_tung_4.png?raw=true" width="100%"></td>
  <td><img src="mars_tung_5.png?raw=true" width="100%"></td>
</tr>
</table>

## Installation:

 Make sure the following libraries are installed:
 ```
 python -m pip install matplotlib
 python -m pip install numpy
 ```

 To see the particular version installed:
 ```
 python -m matplotlib --version
 ```
 To uninstall:
 ```
 python -m pip uninstall matplotlib
 ```
## Usage:
```
USAGE:   python draw_map.py <coord_file.txt> <ore>[ <ore>...]
EXAMPLE: python draw_map.py resourses_326_516_size_30.txt copper tetrahedrite redstone
         OR
         python draw_map.py resourses_326_516_size_30.txt -circle 325 516
```

This tool gets the input ore-coordinates dictionary from [GTVeinInfo](https://github.com/Techlone/GTVeinInfo) in the following form:

```
...
-120 74 408 gold
-120 80 456 magnetite
-120 42 504 platinum
-120 23 552 nickel
-120 22 600 soapstone
-120 19 648 copper
-120 24 696 copper
-120 48 744 apatite
-120 13 792 copper
...
```

Two modes are available:
1. Find and visualize the best location(s) of a particular set of ores and show the additional side resources felt into the drilling machine circle.

   ```
   python draw_map.py resourses_328_498.txt copper gold
   ```

   <img src="ex1.png?raw=true" width="50%">

   **OUTPUT:** the set of side ores felt into the radius
   ```
   CIRCLE: -7 , 162
       DOT: -72 , 51 , 120  ( apatite )
       DOT: 24 , 54 , 168  ( lignite )
       DOT: 72 , 89 , 120  ( lignite )
       DOT: -72 , 22 , 216  ( olivine )
       DOT: 72 , 57 , 168  ( quartz )
       DOT: -24 , 5 , 72  ( diamond )
   ```

2. Visualize and print out the set of ores located in the particular coordinates:

   ```
   python draw_map.py resourses_328_498.txt -circle 325 516
   ```

   <img src="ex2.png?raw=true" width="50%">

   **OUTPUT:** the set of all ores felt into the circle with particular coordinates
   ```
   CIRCLE: 325 , 516
       DOT: 408 , 73 , 504  ( magnetite )
       DOT: 408 , 101 , 552  ( magnetite )
       DOT: 264 , 51 , 456  ( salts )
       DOT: 264 , 73 , 504  ( oilsand )
       DOT: 264 , 68 , 552  ( gold )
       DOT: 360 , 72 , 504  ( gold )
       DOT: 312 , 52 , 456  ( apatite )
       DOT: 312 , 106 , 504  ( lignite )
       DOT: 360 , 60 , 600  ( lignite )
       DOT: 360 , 61 , 456  ( coal )
       DOT: 312 , 17 , 552  ( olivine )
       DOT: 312 , 86 , 600  ( tetrahedrite )
       DOT: 360 , 23 , 552  ( iron )
   ```

## License
This project is available under the [MIT license](LICENSE) © Nail Sharipov
