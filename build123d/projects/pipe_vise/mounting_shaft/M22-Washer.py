import sys
sys.path.insert(0, "/home/tim/scripted_cad/build123d/projects/pipe_vise")

from build123d import *
from ocp_viewer import show

outer = Cylinder(radius=19.5, height=3.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
bore  = Cylinder(radius=12,   height=3.6, align=(Align.CENTER, Align.CENTER, Align.MIN))

washer = (outer - bore).rotate(Axis.X, -90)

export_step(washer, "M22-Washer.step")
show(washer)
