from build123d import *
from ocp_viewer import show
from vise_utils import make_hex_nut

result = make_hex_nut("M10-1.5", thread_pitch=1.5)
export_step(result, "M10-Nut.step")
show(result)
