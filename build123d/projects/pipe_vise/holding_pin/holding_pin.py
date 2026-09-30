from build123d import *
from ocp_viewer import show
from bd_warehouse.thread import IsoThread

# Dimensions
flange_d      = 29
flange_h      = 15
shaft_r       = 9.5
shaft_h       = 80
thread_major  = 10
thread_pitch  = 1.5
thread_length = 12
thread_minor  = thread_major - 2 * 0.6495 * thread_pitch
thread_core_d = thread_minor + 0.05
thread_z      = flange_h + shaft_h
chamfer_size  = 1

# Flange
flange = Cylinder(radius=flange_d / 2, height=flange_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
flange = chamfer(flange.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).first, length=chamfer_size)
flange = chamfer(flange.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).last,  length=chamfer_size)

# Shaft
shaft = Cylinder(radius=shaft_r, height=shaft_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
shaft = shaft.moved(Location((0, 0, flange_h)))

# Thread core + thread
core   = Cylinder(radius=thread_core_d / 2, height=thread_length, align=(Align.CENTER, Align.CENTER, Align.MIN))
core   = core.moved(Location((0, 0, thread_z)))
thread = IsoThread(major_diameter=thread_major, pitch=thread_pitch, length=thread_length,
                   external=True, end_finishes=("fade", "fade"))
thread = thread.moved(Location((0, 0, thread_z)))

result = (flange + shaft + core + thread).rotate(Axis.X, 180)

export_step(result, "holding_pin.step")
show(result)