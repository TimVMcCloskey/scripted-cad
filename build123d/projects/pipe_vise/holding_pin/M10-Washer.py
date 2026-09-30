from build123d import *
from ocp_viewer import show

# M10 Washer
outer_r = 10
inner_r = 5.25
height  = 2.2

washer = Cylinder(radius=outer_r, height=height, align=(Align.CENTER, Align.CENTER, Align.MIN))
hole   = Cylinder(radius=inner_r, height=height, align=(Align.CENTER, Align.CENTER, Align.MIN))
result = washer - hole

export_step(result, "M10-Washer.step")
show(result)

