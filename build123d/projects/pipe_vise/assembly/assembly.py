import sys
from pathlib import Path

from build123d import *
from ocp_viewer import show

from pathlib import Path
BASE = Path.home() / "tim/scripted_cad/build123d/projects/pipe_vise"
STEP_DIR = BASE / "assembly"
sys.path.insert(0, str(BASE))

def load(filename):
    return import_step(str(STEP_DIR / filename))


def placed(part, pos_m, rotation=None):
    """Position a part using assembled_position from pipe_vise.json (metres → mm)."""
    x, y, z = [v * 1000 for v in pos_m]
    # unwrap Compound to Solid so rotate() displays correctly
    s = part.solids()[0] if rotation else part
    p = s.rotate(*rotation) if rotation else part
    return p.moved(Location((x, y, z)))

def exploded(part, pos_m, rotation=None):
    x, y, z = [v * 1000 for v in pos_m]
    # unwrap Compound to Solid so rotate() displays correctly
    s = part.solids()[0] if rotation else part
    p = s.rotate(*rotation) if rotation else part
    return p.moved(Location((x, y, z)))

# --- Load parts ---
fixed_jaw        = load("fixed_jaw.step")
connecting_wages = load("connecting_wages.step")
spindle          = load("spindle.step")
moving_jaw       = load("moving_jaw.step")
handle           = load("handle.step")
handle_cap       = load("handle_cap.step")
support_pin      = load("support_pin.step")
mounting_shaft   = load("mounting_shaft.step")
holding_pin      = load("holding_pin.step")
M10_Nut          = load("M10-Nut.step")
M10_Washer       = load("M10-Washer.step")
M22_Nut          = load("M22-Nut.step")
M22_Washer       = load("M22-Washer.step")

parts = [
    placed(fixed_jaw,        [0.0,     0.0,     0.0   ]),

    placed(mounting_shaft,   [-0.054,  0.030,   0.0   ]),
    placed(mounting_shaft,   [ 0.054,  0.030,   0.0   ]),

    placed(holding_pin,      [-0.054,  0.052,   0.055 ]),
    placed(holding_pin,      [ 0.054,  0.052,   0.055 ]),

    placed(M10_Washer,       [-0.054,  0.052,  -0.0422  ]),
    placed(M10_Washer,       [ 0.054,  0.052,  -0.0422  ]),

    placed(M10_Nut,          [-0.054,  0.052,  -0.0502], rotation=(Axis.X, 90)),
    placed(M10_Nut,          [ 0.054,  0.052,  -0.0502], rotation=(Axis.X, 90)),

    placed(connecting_wages, [ 0.0,    0.210,   0.0   ]),

    placed(M22_Washer,       [-0.054,  0.2398,   0.0   ]),
    placed(M22_Washer,       [ 0.054,  0.2398,   0.0   ]),

    placed(M22_Nut,          [-0.054,  0.2434,  0.0   ]),
    placed(M22_Nut,          [ 0.054,  0.2434,  0.0   ]),

    placed(spindle,          [ 0.0,    0.148,   0.0   ]),
    placed(moving_jaw,       [ 0.0,    0.083,  -0.016 ]),

    placed(support_pin,      [-0.012,  0.138,   0.0   ]),
    placed(support_pin,      [ 0.012,  0.138,   0.0   ]),

    placed(handle,           [ 0.0,    0.333,   0.0   ]),

    # handle_cap.step faces -X; left cap needs 180° flip around Y
    placed(handle_cap,       [ 0.09,   0.333,   0.0   ]),
    placed(handle_cap,       [-0.09,   0.333,   0.0   ], rotation=(Axis.Y, 180)),
]

exploded_parts = [
    exploded(fixed_jaw,        [0.0,     0.0,     0.0   ]),

    exploded(mounting_shaft,   [-0.200,  0.030,   0.0   ]),
    exploded(mounting_shaft,   [ 0.200,  0.030,   0.0   ]),

    exploded(holding_pin,      [-0.054,  0.052,   0.17 ]),
    exploded(holding_pin,      [ 0.054,  0.052,   0.17 ]),

    exploded(M10_Washer,       [-0.054,  0.052,  -0.06  ]),
    exploded(M10_Washer,       [ 0.054,  0.052,  -0.06  ]),

    exploded(M10_Nut,          [-0.054,  0.052,  -0.08], rotation=(Axis.X, 90)),
    exploded(M10_Nut,          [ 0.054,  0.052,  -0.08], rotation=(Axis.X, 90)),

    exploded(connecting_wages, [ 0.0,    0.210,   0.0   ]),

    exploded(M22_Washer,       [-0.200,  0.28,   0.0   ]),
    exploded(M22_Washer,       [ 0.200,  0.28,   0.0   ]),

    exploded(M22_Nut,          [-0.200,  0.300,  0.0   ]),
    exploded(M22_Nut,          [ 0.200,  0.300,  0.0   ]),

    exploded(spindle,          [ 0.0,    0.300,   0.0   ]),

    exploded(moving_jaw,       [ 0.0,    0.100,  -0.016 ]),

    exploded(support_pin,      [-0.012,  0.155,   0.06   ]),
    exploded(support_pin,      [ 0.012,  0.155,   0.06   ]),

    exploded(handle,           [ 0.20,    0.485,   0.0   ]),

    # handle_cap.step faces -X; left cap needs 180° flip around Y
    exploded(handle_cap,       [ 0.35,   0.485,   0.0   ]),
    exploded(handle_cap,       [-0.09,   0.485,   0.0   ], rotation=(Axis.Y, 180)),
]


#assembly = Compound(children=parts, label="pipe_vise")
exploded_view = Compound(children=exploded_parts, label="pipe_vise_exploded")

#export_step(assembly, "pipe_vise_assembly.step")
export_step(exploded_view, "pipe_vise_exploded.step")

#export_gltf(assembly, "pipe_vise_assembly.gltf")
export_gltf(exploded_view, "pipe_vise_exploded.gltf")

#show(assembly)
show(exploded_view)