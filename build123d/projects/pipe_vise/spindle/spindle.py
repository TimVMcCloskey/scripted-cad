import subprocess
subprocess.run([
    r'C:\Users\Tim\AppData\Local\build123d-studio\runtime\uv\uv.exe',
    'pip', 'install', 'bd_warehouse',
    '--python', r'C:\Users\Tim\AppData\Local\build123d-studio\runtime\.venv'
], capture_output=True)

from build123d import *
from build123d_studio import show
from bd_warehouse.thread import AcmeThread

#******************************************
#
# DIMENSIONS
#
#******************************************
THREAD_SIZE      = "1 1/4"
THREAD_LENGTH    = 160.0

NECK_RADIUS    = 15.0
NECK_HEIGHT    = 10.0
NECK_Y         = THREAD_LENGTH

TOP_RADIUS      = 23.0
TOP_HEIGHT      = 30.0
TOP_HOLE_RADIUS = 9.0
TOP_Y           = NECK_Y + NECK_HEIGHT

BOTTOM_RADIUS    = 12.0
BOTTOM_HEIGHT    = 20.0
BOTTOM_Y         = -BOTTOM_HEIGHT

GROOVE_RADIUS        = 3.0
GROOVE_CENTER_RADIUS = 12.0
GROOVE_Y             = BOTTOM_Y + 10.0


#*********************************
#
# thread + core
#
#*********************************

thread = AcmeThread(size=THREAD_SIZE, length=THREAD_LENGTH, external=True,
                    end_finishes=("fade", "fade"))

thread = Location((0, THREAD_LENGTH, 0)) * Rotation(90, 0, 0) * thread

core = Cylinder(radius=thread.root_radius + 0.5, height=THREAD_LENGTH,
                rotation=(90, 0, 0))

core = Location((0, THREAD_LENGTH/2, 0)) * core

thread_solid = thread + core



#*********************************
#
# neck
#
#*********************************

neck = Cylinder(radius=NECK_RADIUS, height=NECK_HEIGHT, rotation=(90, 0, 0))
neck = Location((0, NECK_Y + NECK_HEIGHT/2, 0)) * neck


#*********************************
#
# top with side hole
#
#*********************************

top = Cylinder(radius=TOP_RADIUS, height=TOP_HEIGHT, rotation=(90, 0, 0))
top = Location((0, TOP_Y + TOP_HEIGHT/2, 0)) * top

top_hole = Cylinder(radius=TOP_HOLE_RADIUS, height=TOP_RADIUS * 2.0 + 2.0,
                    rotation=(0, 90, 0))

top_hole = Location((0, TOP_Y + TOP_HEIGHT/2, 0)) * top_hole
top = top - top_hole


#*********************************
#
# bottom with groove
#
#*********************************

bottom = Cylinder(radius=BOTTOM_RADIUS, height=BOTTOM_HEIGHT, rotation=(90, 0, 0))
bottom = Location((0, BOTTOM_Y + BOTTOM_HEIGHT/2, 0)) * bottom

groove = Torus(major_radius=GROOVE_CENTER_RADIUS, minor_radius=GROOVE_RADIUS,
               rotation=(90, 0, 0))

groove = Location((0, GROOVE_Y, 0)) * groove


bottom = bottom - groove


#*********************************
#
# assembly
#
#*********************************
spindle = thread_solid + neck + top + bottom

show(spindle)