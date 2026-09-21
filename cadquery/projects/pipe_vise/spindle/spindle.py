import cadquery as cq
import sys
import os
from cq_warehouse.thread import AcmeThread
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from utilities.utilities import cone, cylinder, torus, front, top, right, left, iso


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
# thread
#
#*********************************

thread = AcmeThread(
    size=THREAD_SIZE,
    length=THREAD_LENGTH,
    external=True,
    end_finishes=("fade", "fade")
)

#*********************************
#
# Core cylinder
#
#*********************************

core = cylinder(thread.root_radius, THREAD_LENGTH, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

thread_solid = cq.Workplane("XY").add(thread.cq_object)
thread_solid = thread_solid.rotate((0,0,0),(1,0,0),-90)
thread_solid = thread_solid.union(cq.Workplane().add(core))


#*********************************
#
# neck
#
#*********************************

neck = cylinder(NECK_RADIUS, NECK_HEIGHT, 0.0, NECK_Y, 0.0, 0.0, 1.0, 0.0)


#*********************************
#
# top
#
#*********************************

top = cylinder(TOP_RADIUS, TOP_HEIGHT, 0.0, TOP_Y, 0.0, 0.0, 1.0, 0.0)
top_hole = cylinder(TOP_HOLE_RADIUS, TOP_RADIUS * 2.0, -TOP_RADIUS, TOP_Y + TOP_HEIGHT / 2.0, 0.0, 1.0, 0.0, 0.0)
top = top.cut(top_hole)

#*********************************
#
# bottom
#
#*********************************

bottom_outer = cylinder(BOTTOM_RADIUS, BOTTOM_HEIGHT, 0.0, BOTTOM_Y, 0.0, 0.0, 1.0, 0.0)

groove = torus(GROOVE_CENTER_RADIUS, GROOVE_RADIUS, 0.0, GROOVE_Y, 0.0, 0.0, 1.0, 0.0)

bottom = cq.Workplane().add(bottom_outer).cut(
    cq.Workplane().add(groove)
)


#*********************************
#
# assembly
#
#*********************************

spindle = (
    thread_solid
    .union(cq.Workplane().add(neck))
    .union(top)
    .union(bottom)
)

#result.export("C:/Users/Tim/tim/cadquery_pipevise/spindle.step")

front(spindle)
