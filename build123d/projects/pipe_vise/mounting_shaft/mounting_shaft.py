from build123d import *
from ocp_viewer import show
from bd_warehouse.thread import IsoThread


# Dimensions
body_d        = 39
body_h        = 180
body_fillet   = 5
bore_r        = 10
bore_h        = 50
collar_r      = 15
collar_h      = 30
thread_major  = 22
thread_pitch  = 1.5
thread_h      = 25
thread_minor  = thread_major - 2 * 0.6495 * thread_pitch
thread_core_d = thread_minor + 0.05

# All cylinders built along Z then placed with explicit moves
# Body: z=0..180, then rotate 90 around X so it runs y=0..180
body = Cylinder(radius=body_d / 2, height=body_h,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
body = fillet(body.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).first,
              radius=body_fillet)
body = body.rotate(Axis.X, -90)   # now runs along +Y, base at y=0, top at y=180

# Bore along Z at y=22
bore = Cylinder(radius=bore_r, height=bore_h,
                align=(Align.CENTER, Align.CENTER, Align.CENTER))
bore = bore.moved(Location((0, 22, 0)))
body = body - bore

# Collar: build along Z, rotate to Y, place so it starts at y=180
collar = Cylinder(radius=collar_r, height=collar_h,
                  align=(Align.CENTER, Align.CENTER, Align.MIN))
collar = collar.rotate(Axis.X, -90)          # runs along +Y from y=0
collar = collar.moved(Location((0, body_h, 0)))  # shift to y=180..210

# Thread core + thread: start at y=210
thread_y = body_h + collar_h

core = Cylinder(radius=thread_core_d / 2, height=thread_h,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
core = core.rotate(Axis.X, -90)
core = core.moved(Location((0, thread_y, 0)))

thread = IsoThread(
    major_diameter=thread_major,
    pitch=thread_pitch,
    length=thread_h,
    external=True,
    end_finishes=("fade", "fade"),
)
thread = thread.rotate(Axis.X, -90).moved(Location((0, thread_y, 0)))

result = body + collar + core + thread

export_step(result, "mounting_shaft.step")
show(result)

