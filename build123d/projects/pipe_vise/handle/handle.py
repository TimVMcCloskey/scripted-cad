from build123d import *
from ocp_viewer import show

# Dimensions
handle_d      = 17
handle_h      = 240
rounding_r    = 1

# Build along Z, fillet both ends, then rotate to run along X
handle = Cylinder(radius=handle_d / 2, height=handle_h,
                  align=(Align.CENTER, Align.CENTER, Align.CENTER))
handle = fillet(handle.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).first,
                radius=rounding_r)
handle = fillet(handle.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).last,
                radius=rounding_r)

result = handle.rotate(Axis.Y, 90)

export_step(result, "handle.step")
show(result)
