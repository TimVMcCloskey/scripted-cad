from bd_warehouse.fastener import HexNut
from bd_warehouse.thread import IsoThread
from build123d import *

def make_hex_nut(size, thread_pitch, fastener_type="iso4032"):
    """
    size         - bd_warehouse size string e.g. "M22-2.5"
    thread_pitch - actual thread pitch to cut (may differ from body_pitch)
    """
    nut = HexNut(size=size, fastener_type=fastener_type)
    h = nut.nut_thickness
    major = float(size.split("-")[0][1:])  # extract 22 from "M22-2.5"
    
    minor = major - 2 * 0.6495 * thread_pitch
    core_r = (minor + 0.05) / 2

    fill_rod = Cylinder(radius=major / 2 + 0.1, height=h,
                        align=(Align.CENTER, Align.CENTER, Align.MIN))
    nut_filled = nut + fill_rod

    thread = IsoThread(major_diameter=major, pitch=thread_pitch,
                       length=h + 4 * thread_pitch, external=True,
                       end_finishes=("fade", "fade"))
    thread = thread.moved(Location((0, 0, -2 * thread_pitch)))

    core = Cylinder(radius=core_r, height=h + 4 * thread_pitch,
                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    core = core.moved(Location((0, 0, -2 * thread_pitch)))

    return (nut_filled - (core + thread)).rotate(Axis.X, -90)

