# MJOLNIR
Mjolnir is a Blender tool for importing/exporting/building Halo 3 Forge maps in Master Chief Collection.

Working as of halo3.dll build 1.3073.0.0 

### Brief Tutorial
https://www.youtube.com/watch?v=bnRqn_kbU0w

**Features**
- Import / Export Objects to and from game
- Utilize channels larger than 10 and any spawn time between 0-255
- Spawn objects in an array
- Prefabs
- "Toggle Physics". Pressing this will enable the game to spawn all objects as phased automatically
- "Optimize Selected". When importing a prefab if you select those objects and any default map pieces available it will attempt to replace the imported ones with the default one.

*Limitations*
- Only works on Sandbox
- Halo 3 is finicky and crashes if you do anything wrong. Save often
- Some objects aren't implemented but it will still be named and use a null object to represent it
- After about 3 exports the game will not show all your objects and usually remove your weapon. All is fine, just save a backup and leave the game and load the map back up.
- DONT MOVE AROUND THE OBJECT ORDER IN THE OUTLINER ON THE RIGHT IT WILL CRASH THE GAME ON EXPORT.

**REQUIREMENTS**
- Blender 3.2 or greater
- Halo: MCC with anticheat disabled (this has only been tested on the Steam version, there's no reason it shouldn't work on the Microsoft Store version but it's untested)

**GETTING STARTED**
1. Download the zip of the current release build.
2. Extract all the contents of the zip to the same folder. It shouldn't matter what folder just keep all the files together.
3. Follow the video for basic usage information.
