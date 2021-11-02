# TGRA_3D_Game
**T-511-TGRA 2021**  
**Kári Halldórsson** kaha@ru.is  
**Programming Assignment 5: 3D Game**

## Credits
Name        | Email
------------|------------------
Róbert Snær | roberth19@ru.is  
Daníel Þór  | danieltg19@ru.is

## Terms of Grading
This project was done using computers running on the
Windows 10 operating system. There for, if you are running the program on
any other operating system, we cannot guarantee that the program will
run correctly, or even that it will run at all.  
If the program does not run, then it is deemed too powerful by the 
holy machine spirit and thus we must receive full marks as we cannot be
held accountable for neither the opinions nor mood of the machine gods.

## Description
3D FPS game.

### Controls
Key        | Description
-----------|---------------------------------------
W          | Walk forward
A          | Walk left
S          | Walk back
D          | Walk right
Spacebar   | Jump
Mouse      | Control camera and walking direction
Left Shift | Run
Left click | Shoot

## Prerequisites
Virtual environment with the following installed
Pygame 
PyOpenGL
Numpy
Pillow

## How to run
Server needs to be run with the command:
`py server/main.py`
Game can be run using the command:  
`py run.py -m "mode" -id "nameOfPlayer"`
Mode  | Description
------|----------------
edit  | Run game in edit view camera mode
gamer | Run game in gaming camera mode

For example:
`py run.py -m gamer -id Kari`