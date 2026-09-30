from build123d import *
from ocp_viewer import show

# Dimensions
cone_h      = 20
cone_r1     = 12.5   # narrow end (bottom)
cone_r2     = 17     # wide end (top)
cone_fillet = 2

bore_r      = 8.5
bore_h      = 15
bore_fillet = 2

# Outer cone: r1 at bottom, r2 at top
cone = Cone(bottom_radius=cone_r1, top_radius=cone_r2, height=cone_h,
            align=(Align.CENTER, Align.CENTER, Align.MIN))
# Fillet top edge (large end)
cone = fillet(cone.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).last,
              radius=cone_fillet)
# Fillet bottom edge (small end)
cone = fillet(cone.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).first,
              radius=cone_fillet)

# Socket bore: open at bottom, fillet at top
bore = Cylinder(radius=bore_r, height=bore_h,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
bore = fillet(bore.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).last,
              radius=bore_fillet)

result = (cone - bore).rotate(Axis.Y, 90).moved(Location((15, 0, 0)))

export_step(result, "handle_cap.step")
show(result)