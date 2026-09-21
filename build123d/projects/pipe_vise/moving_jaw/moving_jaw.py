from build123d import *
from build123d_studio import show

# ******************************************
#
# DIMENSIONS
#
# ******************************************

BODY_HEIGHT = 65.0  # total height of body
BODY_WIDTH = 84.0
BODY_DEPTH = 32.0  # extrusion depth (Z)

# Pin hole locks spindle
PIN_HOLE_X = 30.0  # X position
PIN_HOLE_Y = 55.0  # Y position
PIN_HOLE_RADIUS = 2.75  # radius (5.5mm diameter)

# Guiding groove
GUIDE_GROOVE_X = -12.0  # X center of arc circle
GUIDE_GROOVE_Z = 16.0  # Z center (mid depth)
GUIDE_GROOVE_RADIUS = 20.0  # radius of arc circle

# Middle hole
MIDDLE_HOLE_X = 0.0  # X position
MIDDLE_HOLE_Y = 38.0  # Y position of cone bottom point
MIDDLE_HOLE_Z = 16.0  # Z position (mid depth)

DRILL_POINT_HEIGHT = 7.0  # height of bottom cone

DRILL_RADIUS = 12.0  #
DRILL_HEIGHT = 20.0  #

CHAMFER_R1 = 13.2  # outer radius of top chamfer
CHAMFER_R2 = 12.0  # inner radius of top chamfer
CHAMFER_HEIGHT = 1.2  # height of top chamfer

# ******************************************
#
# GEOMETRY
#
# ******************************************

points = [
    (0.0, 0.0),
    (12.0, 0.0),
    (12.0, 5.0),
    (17.0, 5.0),
    (17.0, 10.0),
    (22.0, 10.0),
    (22.0, 15.0),
    (27.0, 15.0),
    (27.0, 20.0),
    (32.0, 20.0),
    (32.0, 25.0),
    (37.0, 25.0),
    (37.0, 30.0),
    (42.0, 30.0),
    (42.0, 65.0),
    (0.0, 65.0),
]


# ******************************************
#
# body half
#
# ******************************************

outline = Polyline(*points, close=True)
profile = make_face(outline)
body = extrude(profile, amount=BODY_DEPTH)


# ******************************************
#
# pin hole
#
# ******************************************

pin_hole = Cylinder(
    radius=PIN_HOLE_RADIUS,
    height=BODY_DEPTH,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

pin_hole = pin_hole.move(Location((PIN_HOLE_X, PIN_HOLE_Y, 0)))


# ******************************************
#
# guide_groove
#
# ******************************************

guide_groove = Cylinder(
    radius=GUIDE_GROOVE_RADIUS, height=BODY_HEIGHT, rotation=(90, 0, 0)
)

guide_groove = (
    Location((GUIDE_GROOVE_X, BODY_HEIGHT / 2, GUIDE_GROOVE_Z)) * guide_groove
)


# ******************************************
#
# counter sunk hole
#
# ******************************************

# drill point cone opening upward in Y

drill_point = Cone(
    bottom_radius=0,
    top_radius=DRILL_RADIUS,
    height=DRILL_POINT_HEIGHT,
    rotation=(-90, 0, 0),
)
drill_point = drill_point.move(
    Location(
        (
            MIDDLE_HOLE_X,
            BODY_HEIGHT - DRILL_HEIGHT - DRILL_POINT_HEIGHT / 2,
            MIDDLE_HOLE_Z,
        )
    )
)


# drill

drill = Cylinder(radius=DRILL_RADIUS, height=DRILL_HEIGHT, rotation=(90, 0, 0))
drill = drill.move(
    Location((MIDDLE_HOLE_X, BODY_HEIGHT - DRILL_HEIGHT / 2, MIDDLE_HOLE_Z))
)

# chamfer

chamfer = Cone(
    bottom_radius=CHAMFER_R1,
    top_radius=CHAMFER_R2,
    height=CHAMFER_HEIGHT,
    rotation=(90, 0, 0),
)
chamfer = chamfer.move(Location((MIDDLE_HOLE_X, BODY_HEIGHT, MIDDLE_HOLE_Z)))

# counter_sunk_drill

counter_sunk_drill = drill_point + drill + chamfer

# *********************************
#
# assembly
#
# *********************************

result = body - pin_hole - guide_groove

result = Location((-BODY_WIDTH / 2, 0, 0)) * result

result = result.mirror(Plane.YZ) + result

result = result - counter_sunk_drill

show(result)
