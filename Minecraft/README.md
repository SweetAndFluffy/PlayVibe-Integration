# Minecraft Mod

This is the integration into Minecraft via a forge mod. 

# Using the mod

This mod has to be run in the client if you want to play in singleplayer, or on the server if 
you want to play in multiplayer. If the mod is installed on the server, other clients don't 
need it installed on their side, because it doesn't add any new objects.

# Building

To build this, put the remoteVibratorControl folder into a forge development environent and build it using 

    gradle build

The best way to do development on this, is to make a symlink to the directory from your forge environment. 
To do this on Windows, you use the mklink command:

    mklink /d <Path to your forge development environment/src/main/java/remoteVibratorControl> <path to this repo/Minecraft/remoteVibratorControl>

For linux, you use the ln command:

    ln -s <path to this repo/Minecraft/remoteVibratorControl> <Path to your forge development environment/src/main/java/remoteVibratorControl>
