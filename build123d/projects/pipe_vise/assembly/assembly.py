import sys
sys.path.insert(0, "/home/tim/scripted_cad/build123d/projects/pipe_vise")

from build123d import *
from ocp_viewer import show

STEP_DIR = "/home/tim/scripted_cad/build123d/projects/pipe_vise/assembly/"

def load(filename):
    return import_step(STEP_DIR + filename)

def placed(part, pos_m, rotation=None):
    """Position a part using assembled_position from pipe_vise.json (metres → mm)."""
    x, y, z = [v * 1000 for v in pos_m]
    p = part.rotate(*rotation) if rotation else part
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

# --- Position parts (assembled_position from JSON, metres → mm) ---
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

assembly = Compound(children=parts, label="pipe_vise")

#export_step(assembly, "pipe_vise_assembly.step")
show(assembly)
