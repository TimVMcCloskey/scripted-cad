# Scripted CAD — Parametric Pipe Vise

Parametric 3D modeling of a mechanical pipe vise assembly in Python, implemented in both **CadQuery** and **build123d** frameworks. The three most geometrically complex parts are modeled with full parametric dimensions, boolean operations, and export to STEP.

## Parts

### Moving Jaw
The sliding jaw assembly with staircase profile, guide groove arc, pin hole, and countersunk spindle hole with chamfer.

### Spindle
ACME threaded rod with collar, flange with side handle hole, and bottom socket with toroidal retaining groove.

### Connecting Wages
Three-circle hull body with neck, concave fillet, mount holes, and internal ACME thread tap.

## Structure

```
scripted_cad/
  cadquery/
    projects/pipe_vise/
      moving_jaw/moving_jaw.py
      spindle/spindle.py
      connecting_wages/connecting_wages.py
    utilities/utilities.py
  build123d/
    projects/pipe_vise/
      moving_jaw/moving_jaw.py
      spindle/spindle.py
      connecting_wages/connecting_wages.py
```

## Frameworks

**CadQuery** — fluent API, method chaining, VTK viewer  
**build123d** — algebraic mode, `+`/`-` operators, build123d Studio viewer

Both frameworks are built on the Open CASCADE geometry kernel and export to STEP, STL and other CAD formats.

## Dependencies

**CadQuery:**
```bash
pip install cadquery cq-warehouse
```

**build123d:**
```bash
pip install build123d bd-warehouse
```

## Running

Activate the appropriate venv and run any script directly:

```bash
# CadQuery
source cquery/Scripts/activate
python cadquery/projects/pipe_vise/moving_jaw/moving_jaw.py

# build123d
# Open in build123d Studio and run with Shift+Enter
```

Each script exports a STEP file alongside the script and displays the model in the viewer.

## Author

**Tim McCloskey** — CAD scripting, VR/graphics engineering, Denver CO  
Portfolio: timvmccloskey.github.io · GitHub: github.com/TimVMcCloskey
