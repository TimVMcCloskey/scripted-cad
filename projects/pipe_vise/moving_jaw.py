import cadquery as cq
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.utilities import front, top, right, left, iso

# CadQuery XZ workplane convention:
# center(world_X, world_Z)
# extrude negative to cut in -Y direction (into part from front)

# =============================================================================
# DIMENSIONS
# =============================================================================

# Body profile — staircase steps (x, y) pairs
# Each step adds 5mm in both X and Y
STEP_WIDTH       = 5.0    # width of each step
STEP_HEIGHT      = 5.0    # height of each step
STEP_COUNT       = 7      # number of steps
BODY_TOP_Y       = 65.0   # total height of body
BODY_DEPTH       = 32.0   # extrusion depth (Z)
BODY_BASE_X      = 12.0   # width of base before steps begin

# Pin hole — locks spindle
PIN_HOLE_X       = 30.0   # X position
PIN_HOLE_Y       = 55.0   # Y position
PIN_HOLE_RADIUS  = 2.75   # radius (5.5mm diameter)

# Guiding groove — tracks on guide post, cut from left side
GROOVE_CENTER_X  = -12.0  # X center of arc circle
GROOVE_CENTER_Z  = 16.0   # Z center (mid depth)
GROOVE_RADIUS    = 20.0   # radius of arc circle

# Middle hole — countersunk spindle hole
HOLE_CENTER_X    = 42.0   # X position
HOLE_BASE_Y      = 38.0   # Y position of cone bottom point
HOLE_CENTER_Z    = 16.0   # Z position (mid depth)
CONE_BOT_RADIUS  = 12.0   # radius at top of bottom cone
CONE_BOT_HEIGHT  = 7.0    # height of bottom cone
SHAFT_RADIUS     = 12.0   # radius of cylindrical shaft
SHAFT_HEIGHT     = 20.0   # height of shaft
FLARE_R1         = 13.2   # outer radius of top flare
FLARE_R2         = 12.0   # inner radius of top flare
FLARE_HEIGHT     = 1.2    # height of top flare


# =============================================================================
# GEOMETRY
# =============================================================================

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

body = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(BODY_DEPTH)
)

pin_hole = (
    cq.Workplane("XY")
    .center(PIN_HOLE_X, PIN_HOLE_Y)
    .circle(PIN_HOLE_RADIUS)
    .extrude(BODY_DEPTH)
)

groove = (
    cq.Workplane("XZ")
    .center(GROOVE_CENTER_X, GROOVE_CENTER_Z)
    .circle(GROOVE_RADIUS)
    .extrude(-BODY_TOP_Y)
)

cone_bottom = cq.Solid.makeCone(
    radius1=0.0, radius2=CONE_BOT_RADIUS, height=CONE_BOT_HEIGHT,
    pnt=cq.Vector(HOLE_CENTER_X, HOLE_BASE_Y, HOLE_CENTER_Z),
    dir=cq.Vector(0.0, 1.0, 0.0)
)

shaft = cq.Solid.makeCylinder(
    radius=SHAFT_RADIUS, height=SHAFT_HEIGHT,
    pnt=cq.Vector(HOLE_CENTER_X, HOLE_BASE_Y + CONE_BOT_HEIGHT, HOLE_CENTER_Z),
    dir=cq.Vector(0.0, 1.0, 0.0)
)

cone_top = cq.Solid.makeCone(
    radius1=FLARE_R1, radius2=FLARE_R2, height=FLARE_HEIGHT,
    pnt=cq.Vector(HOLE_CENTER_X, BODY_TOP_Y, HOLE_CENTER_Z),
    dir=cq.Vector(0.0, -1.0, 0.0)
)

# =============================================================================
# ASSEMBLY
# =============================================================================

result = body.cut(pin_hole).cut(groove)
result = result.mirror(result.faces(">X"), union=True)
result = result.cut(cone_bottom).cut(shaft).cut(cone_top)

# =============================================================================
# EXPORT
# =============================================================================

#result.export("C:/Users/Tim/tim/cadquery_pipevise/moving_jaw.step")

# =============================================================================
# SHOW — change view function as needed
# =============================================================================

front(result)
# top(result)
# right(result)
# left(result)
# iso(result)
