import sys
sys.path.insert(0, "/home/tim/scripted_cad/build123d/projects/pipe_vise")

from build123d import *
from ocp_viewer import show

pin = Cylinder(radius=2.5, height=32, align=(Align.CENTER, Align.CENTER, Align.CENTER))
pin = fillet(pin.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).last, radius=1)
pin = fillet(pin.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z).first, radius=1)

export_step(pin, "support_pin.step")
show(pin)
