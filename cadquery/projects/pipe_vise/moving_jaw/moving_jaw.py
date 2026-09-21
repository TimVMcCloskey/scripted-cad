import cadquery as cq
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from utilities.utilities import cone, cylinder, front, top, right, left, iso


#******************************************
#
# DIMENSIONS
#
#******************************************

# Body profile — staircase steps (x, y) pairs
# Each step adds 5mm in both X and Y
STEP_WIDTH       = 5.0    # width of each step
STEP_HEIGHT      = 5.0    # height of each step
STEP_COUNT       = 7      # number of steps
BODY_HEIGHT      = 65.0   # total height of body
BODY_DEPTH       = 32.0   # extrusion depth (Z)
BODY_BASE_X      = 12.0   # width of base before steps begin

# Pin hole — locks spindle
PIN_HOLE_X       = 30.0   # X position
PIN_HOLE_Y       = 55.0   # Y position
PIN_HOLE_RADIUS  = 2.75   # radius (5.5mm diameter)

# Guiding groove — tracks on guide post, cut from left side
GUIDE_GROOVE_X         = -12.0  # X center of arc circle
GUIDE_GROOVE_Z         = 16.0   # Z center (mid depth)
GUIDE_GROOVE_RADIUS    = 20.0   # radius of arc circle

# Middle hole — countersunk spindle hole
MIDDLE_HOLE_X    = 42.0   # X position
MIDDLE_HOLE_Y      = 38.0   # Y position of cone bottom point
MIDDLE_HOLE_Z    = 16.0   # Z position (mid depth)
DRILL_POINT_RADIUS  = 12.0   # radius at top of bottom cone
DRILL_POINT_HEIGHT  = 7.0    # height of bottom cone
DRILL_RADIUS     = 12.0   # radius of cylindrical drill
DRILL_HEIGHT     = 20.0   # height of drill
CHAMFER_R1         = 13.2   # outer radius of top chamfer
CHAMFER_R2         = 12.0   # inner radius of top chamfer
CHAMFER_HEIGHT     = 1.2    # height of top chamfer

#******************************************
#
# GEOMETRY
#
#******************************************

points = [
    (0.0,  0.0),  (12.0,  0.0),
    (12.0, 5.0),  (17.0,  5.0),
    (17.0, 10.0), (22.0, 10.0),
    (22.0, 15.0), (27.0, 15.0),
    (27.0, 20.0), (32.0, 20.0),
    (32.0, 25.0), (37.0, 25.0),
    (37.0, 30.0), (42.0, 30.0),
    (42.0, 65.0), (0.0,  65.0)
]

#******************************************
#
# body
#
#******************************************

body = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(BODY_DEPTH)
)

#******************************************
#
# holes
#
#******************************************

pin_hole = cylinder(PIN_HOLE_RADIUS, BODY_DEPTH, PIN_HOLE_X, PIN_HOLE_Y, 0.0, 0.0, 0.0, 1.0)

guide_groove = cylinder(GUIDE_GROOVE_RADIUS, BODY_HEIGHT, GUIDE_GROOVE_X, 0.0, GUIDE_GROOVE_Z, 0.0, 1.0, 0.0)


#******************************************
#
# counter sunk hole
#
#******************************************

drill_point = cone(0.0, DRILL_POINT_RADIUS, DRILL_POINT_HEIGHT,
                   MIDDLE_HOLE_X, MIDDLE_HOLE_Y, MIDDLE_HOLE_Z,
                   0.0, 1.0, 0.0)


drill = cylinder(DRILL_RADIUS, DRILL_HEIGHT, 
                 MIDDLE_HOLE_X, MIDDLE_HOLE_Y + DRILL_POINT_HEIGHT, MIDDLE_HOLE_Z,
                 0.0, 1.0, 0.0)

chamfer = cone(CHAMFER_R1, CHAMFER_R2, CHAMFER_HEIGHT,
               MIDDLE_HOLE_X, BODY_HEIGHT, MIDDLE_HOLE_Z,
                0.0, -1.0, 0.0)

counter_sunk_drill = chamfer + drill + drill_point

#*********************************
#
# assembly
#
#*********************************

result = body.cut(pin_hole).cut(guide_groove)
result = result.mirror(result.faces(">X"), union=True)
result = result.cut(counter_sunk_drill)

#result.export("C:/Users/Tim/tim/cadquery_pipevise/moving_jaw.step")

front(result)
# top(result)
# right(result)
# left(result)
# iso(result)
