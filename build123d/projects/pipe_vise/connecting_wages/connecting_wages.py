from build123d import *
from ocp_viewer import show
from bd_warehouse.thread import AcmeThread


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

MOUNT_HOLE_RADIUS = 30.0 / 2
MOUNT_HOLE_X      = 54.0

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
    left_circle = Circle(BODY_LEFT_RADIUS).locate(Location((BODY_LEFT_X, 0, 0)))
    center_circle = Circle(BODY_CENTER_RADIUS)
    
    left_sketch = make_hull(left_circle.edges() + center_circle.edges())
    left_solid = extrude(left_sketch, amount=-BODY_HEIGHT)
    left_solid = Rotation(90, 0, 0) * left_solid

    full_solid = left_solid + mirror(left_solid, about=Plane.YZ)
    return full_solid

body = make_body()


#******************************************
#
# neck
#
#******************************************

neck = Cylinder(radius=NECK_RADIUS, height=NECK_HEIGHT, rotation=(90, 0, 0))
neck = Location((0, BODY_HEIGHT+NECK_HEIGHT/2 , 0)) * neck


#******************************************
#
# fillet
#
#******************************************

body = body + neck

# Select the circular edge at the junction between neck and body
# Filter circular edges, group by Y, select the one at junction
junction_edges = ShapeList([e for e in body.edges().filter_by(GeomType.CIRCLE) 
                            if abs(e.center().Y - BODY_HEIGHT) < 0.5 
                            and abs(e.radius - NECK_RADIUS) < 0.5])
body = fillet(junction_edges, FILLET_RADIUS)


#******************************************
#
# drill mounting holes
#
#******************************************

mount_hole_left = Cylinder(radius=MOUNT_HOLE_RADIUS, height=BODY_HEIGHT + 2.0,
                            rotation=(90, 0, 0))
mount_hole_left = Location((-MOUNT_HOLE_X, BODY_HEIGHT/2, 0)) * mount_hole_left

mount_hole_right = Cylinder(radius=MOUNT_HOLE_RADIUS, height=BODY_HEIGHT + 2.0,
                             rotation=(90, 0, 0))
mount_hole_right = Location((MOUNT_HOLE_X, BODY_HEIGHT/2, 0)) * mount_hole_right


#*********************************
#
# tap spindle thread
#
#*********************************

thread = AcmeThread(size=THREAD_SIZE, length=THREAD_LENGTH,
                    end_finishes=("fade", "fade"))
                    
#thread = Rotation(90, 0, 0) * thread
thread = Location((0, THREAD_LENGTH, 0)) * Rotation(90, 0, 0) * thread

core = Cylinder(radius=thread.root_radius + 0.5, height=THREAD_LENGTH,
                rotation=(90, 0, 0))

core = Location((0, THREAD_LENGTH/2, 0)) * core

thread_solid = thread + core


#******************************************
#
# ASSEMBLY
#
#******************************************

result = body - mount_hole_left - mount_hole_right - thread_solid

export_step(result, "connecting_wages.step")

show(result)