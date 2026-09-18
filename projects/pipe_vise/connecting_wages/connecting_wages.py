import cadquery as cq
import sys, os, math
from cq_warehouse.thread import AcmeThread
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from utilities.utilities import cone, cylinder, front, top, right, left, iso


#******************************************
#
# BODY DIMENSIONS
#
#******************************************

# Three circle centers and radii

# body left
BODY_LEFT_X       = -54.0
BODY_LEFT_Y       = 0.0  
BODY_LEFT_RADIUS  = 21.0   

# body center
BODY_CENTER_X      = 0.0
BODY_CENTER_Y      = 0.0;
BODY_CENTER_RADIUS = 27.5 

BODY_HEIGHT        = 30.0


#******************************************
#
# NECK DIMENSIONS
#
#******************************************

NECK_RADIUS   = 20.0
NECK_HEIGHT   = 10.0
FILLET_RADIUS = 5.0   

#******************************************
#
# MOUNT HOLES DIMENSIONS
#
#******************************************

MOUNT_HOLE_RADIUS   = 30.0 / 2
MOUNT_HOLE_X        = 54

#******************************************
#
# SPINDLE THREADED HOLE DIMENSIONS
#
#******************************************

# Internal ACME thread
THREAD_SIZE      = "1 1/4"
THREAD_LENGTH    = 40.0  


                         
#******************************************
#
# make_body
#
#******************************************

def make_body():

    # Left half — left circle and center circle
    left_half = (
        cq.Sketch()
        .push([(BODY_LEFT_X, BODY_LEFT_Y)])
        .circle(BODY_LEFT_RADIUS)
        .push([(BODY_CENTER_X, BODY_CENTER_Y)])
        .circle(BODY_CENTER_RADIUS)
        .reset()
        .hull()
    )

    # Extrude left half - extrudes in negative y
    left_solid = (
        cq.Workplane("XZ")
        .placeSketch(left_half)
        .extrude(BODY_HEIGHT)
    )
    
    
    #Mirror to get right half and union
    full_solid = left_solid.union(
        left_solid.mirror("YZ")
    )
    
    return full_solid

body = make_body()

#******************************************
#
# make neck
#
#******************************************

neck = cylinder(NECK_RADIUS, NECK_HEIGHT, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

#******************************************
#
# make fillet
#
#******************************************

fillet = (
    cq.Workplane("XY")
    .moveTo(NECK_RADIUS, 0)
    .lineTo(NECK_RADIUS + FILLET_RADIUS, 0)
    .radiusArc((NECK_RADIUS, -FILLET_RADIUS), -FILLET_RADIUS)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

fillet = fillet.rotate((0,0,0),(1,0,0),180)

body = body.union(neck).union(fillet)

#******************************************
#
# drill mounting holes
#
#******************************************

mount_hole_left = cylinder(MOUNT_HOLE_RADIUS, BODY_HEIGHT, -MOUNT_HOLE_X, 0.0, 0.0, 0.0, -1.0, 0.0)
mount_hole_right = cylinder(MOUNT_HOLE_RADIUS, BODY_HEIGHT, MOUNT_HOLE_X, 0.0, 0.0, 0.0, -1.0, 0.0)

#*********************************
#
# tap spindle thread
#
#*********************************

thread = AcmeThread(
    size=THREAD_SIZE,
    length=THREAD_LENGTH,
    external=True,
    end_finishes=("fade", "fade")
)

core = cylinder(thread.root_radius, THREAD_LENGTH, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

thread_solid = cq.Workplane("XY").add(thread.cq_object)
thread_solid = thread_solid.rotate((0,0,0),(1,0,0),-90)
thread_solid = thread_solid.union(cq.Workplane().add(core))
thread_solid = thread_solid.translate((0, -30, 0))

# Cut holes and thread
result = body.cut(mount_hole_left).cut(mount_hole_right).cut(thread_solid)

#result.export("C:/Users/Tim/tim/cadquery_pipevise/connecting_wages.step")

front(result)
