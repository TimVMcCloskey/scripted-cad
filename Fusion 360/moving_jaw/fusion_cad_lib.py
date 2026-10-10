import adsk.core, adsk.fusion
import math

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def cm(mm):
    """Convert mm to Fusion's internal cm unit."""
    return mm / 10.0

def _val(v):
    """Accept a param name string or a mm number, return ValueInput."""
    if isinstance(v, str):
        return adsk.core.ValueInput.createByString(v)
    return adsk.core.ValueInput.createByReal(cm(v))

def _neg_val(v):
    """Negated version of _val, for flip=True extrusions."""
    if isinstance(v, str):
        return adsk.core.ValueInput.createByString(f"-({v})")
    return adsk.core.ValueInput.createByReal(-cm(v))

def _plane(root_comp, name):
    """Return a construction plane by name string."""
    return {
        "xy": root_comp.xYConstructionPlane,
        "xz": root_comp.xZConstructionPlane,
        "yz": root_comp.yZConstructionPlane,
    }[name.lower()]

def _op(operation):
    return {
        "new":  adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
        "cut":  adsk.fusion.FeatureOperations.CutFeatureOperation,
        "join": adsk.fusion.FeatureOperations.JoinFeatureOperation,
    }[operation]

# ---------------------------------------------------------------------------
# Workspace init
# ---------------------------------------------------------------------------

def init(app, parameters=None):
    """
    Create a new parametric Fusion document.
    parameters: dict of {name: value_in_mm}
    Returns: (design, root_comp, planes_dict)
    """
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = app.activeProduct
    root_comp = design.rootComponent
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType

    if parameters:
        for name, value in parameters.items():
            init_parameter(design, name, value)

    planes = {
        "xy": root_comp.xYConstructionPlane,
        "xz": root_comp.xZConstructionPlane,
        "yz": root_comp.yZConstructionPlane,
    }
    return design, root_comp, planes

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

def init_parameter(design, name, value_mm, unit="mm"):
    """Register a user parameter. value_mm is always a plain number."""
    params = design.userParameters
    if not params.itemByName(name):
        params.add(name, adsk.core.ValueInput.createByReal(cm(value_mm)), unit, "")
    return params.itemByName(name)

def get_parameter(design, name):
    """Return parameter's current value in cm (Fusion internal unit)."""
    param = design.userParameters.itemByName(name)
    if param:
        return param.value
    raise ValueError(f"Parameter '{name}' not found")

# ---------------------------------------------------------------------------
# Construction planes
# ---------------------------------------------------------------------------

def make_plane(root_comp, base_plane_name, offset):
    """
    Offset construction plane.
    base_plane_name: "xy", "xz", "yz"
    offset: mm number or param name string
    """
    base = _plane(root_comp, base_plane_name)
    planes = root_comp.constructionPlanes
    inp = planes.createInput()
    inp.setByOffset(base, _val(offset))
    return planes.add(inp)

# ---------------------------------------------------------------------------
# Sketches
# ---------------------------------------------------------------------------

def make_custom_profile_sketch(root_comp, plane, points_list):
    """
    Closed polygon sketch from a list of (x, y) tuples in mm.
    plain numbers only — profile points are usually hardcoded geometry.
    """
    sketch = root_comp.sketches.add(plane)
    lines = sketch.sketchCurves.sketchLines
    for i in range(len(points_list) - 1):
        lines.addByTwoPoints(
            adsk.core.Point3D.create(cm(points_list[i][0]),   cm(points_list[i][1]),   0),
            adsk.core.Point3D.create(cm(points_list[i+1][0]), cm(points_list[i+1][1]), 0)
        )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(cm(points_list[-1][0]), cm(points_list[-1][1]), 0),
        adsk.core.Point3D.create(cm(points_list[0][0]),  cm(points_list[0][1]),  0)
    )
    return sketch

def make_circle_sketch(root_comp, plane, x, y, radius):
    """Single circle. x, y, radius: mm numbers or param name strings."""
    sketch = root_comp.sketches.add(plane)
    # circles use Point3D so we resolve x/y to real values for position
    x_val = cm(x) if not isinstance(x, str) else None
    y_val = cm(y) if not isinstance(y, str) else None
    if x_val is None or y_val is None:
        raise ValueError("make_circle_sketch: x and y must be numbers (use make_plane for parametric positioning)")
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(x_val, y_val, 0),
        cm(radius) if not isinstance(radius, str) else None  # radius resolved below
    )
    # If radius is a param string, use a sketch constraint instead
    # For now: plain numbers for circle geometry, params for extrusion depths
    return sketch

def make_circles_sketch(root_comp, plane, centers_and_radii):
    """
    Multiple circles on one sketch.
    centers_and_radii: list of (x, y, radius) tuples, all mm numbers.
    """
    sketch = root_comp.sketches.add(plane)
    c = sketch.sketchCurves.sketchCircles
    for x, y, r in centers_and_radii:
        c.addByCenterRadius(
            adsk.core.Point3D.create(cm(x), cm(y), 0),
            cm(r)
        )
    return sketch

# ---------------------------------------------------------------------------
# Extrusion
# ---------------------------------------------------------------------------

def extrude_sketch(root_comp, sketch, amount, symmetric=False,
                   operation="new", target_body=None,
                   profile_index=0, all_profiles=False,
                   taper_angle=0.0, flip=False):
    """
    Extrude a sketch profile.
    amount: mm number or param name string
    flip:   True reverses direction (for cuts into a face from an offset plane)
    """
    extrudes = root_comp.features.extrudeFeatures

    if all_profiles:
        profile = adsk.core.ObjectCollection.create()
        for p in sketch.profiles:
            profile.add(p)
    else:
        profile = sketch.profiles.item(profile_index)

    inp = extrudes.createInput(profile, _op(operation))

    dist = _neg_val(amount) if flip else _val(amount)
    inp.setDistanceExtent(symmetric, dist)

    if taper_angle != 0.0:
        inp.taperAngle = adsk.core.ValueInput.createByReal(
            taper_angle * (math.pi / 180.0)
        )

    if target_body and operation in ("cut", "join"):
        inp.participantBodies = [target_body]

    feat = extrudes.add(inp)
    return feat.bodies.item(0) if operation == "new" else feat

# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------

def translate(root_comp, body, x, y, z):
    """Move body by x, y, z in mm. Plain numbers only."""
    move_feats = root_comp.features.moveFeatures
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)
    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(cm(x), cm(y), cm(z))
    move_input = move_feats.createInput(bodies, transform)
    move_feats.add(move_input)

# ---------------------------------------------------------------------------
# Mirror
# ---------------------------------------------------------------------------

def mirror(root_comp, body, plane_name):
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(body)
    mirror_feats = root_comp.features.mirrorFeatures
    inp = mirror_feats.createInput(bodies, _plane(root_comp, plane_name))
    feat = mirror_feats.add(inp)
    # Return the newly created mirror body (last one added to root)
    return root_comp.bRepBodies.item(root_comp.bRepBodies.count - 1)

# ---------------------------------------------------------------------------
# Boolean
# ---------------------------------------------------------------------------

def join(root_comp, target_body, tool_body):
    """Join tool_body into target_body. tool_body is consumed."""
    tools = adsk.core.ObjectCollection.create()
    tools.add(tool_body)
    combine = root_comp.features.combineFeatures
    inp = combine.createInput(target_body, tools)
    inp.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    inp.isKeepToolBodies = False
    combine.add(inp)
    return target_body
    
def make_rectangle_sketch(root_comp, plane, x1, y1, x2, y2):
    # x1, y1: bottom-left corner; x2, y2: top-right corner — all in mm
    sketch = root_comp.sketches.add(plane)
    lines = sketch.sketchCurves.sketchLines
    lines.addTwoPointRectangle(
        adsk.core.Point3D.create(cm(x1), cm(y1), 0),
        adsk.core.Point3D.create(cm(x2), cm(y2), 0)
    )
    return sketch


def revolve_sketch(root_comp, sketch, axis, angle_deg=360.0,
                   operation="new", target_body=None,
                   profile_index=0, all_profiles=False):
    revolves = root_comp.features.revolveFeatures

    if all_profiles:
        profile = adsk.core.ObjectCollection.create()
        for p in sketch.profiles:
            profile.add(p)
    else:
        profile = sketch.profiles.item(profile_index)

    inp = revolves.createInput(profile, axis, _op(operation))
    inp.setAngleExtent(False, adsk.core.ValueInput.createByReal(
        angle_deg * (math.pi / 180.0)
    ))

    if target_body and operation in ("cut", "join"):
        inp.participantBodies = [target_body]

    feat = revolves.add(inp)
    return feat.bodies.item(0) if operation == "new" else feat


def make_thread(root_comp, body, nominal_radius_mm,
                thread_type, designation, thread_class,
                length_mm, internal=False, tapered=False, 
                right_handed=True, modeled=False):
    thread_face = None
    for face in body.faces:
        if face.geometry.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType:
            if abs(face.geometry.radius - nominal_radius_mm / 10.0) < 0.01:
                thread_face = face
                break
    if thread_face is None:
        raise ValueError(f"No cylindrical face found at radius {nominal_radius_mm}mm")

    thread_info = adsk.fusion.ThreadInfo.create(
        tapered, internal, thread_type, designation, thread_class, right_handed
    )
    threads = root_comp.features.threadFeatures
    inp = threads.createInput(thread_face, thread_info)
    inp.isFullLength = False
    inp.threadLength = adsk.core.ValueInput.createByReal(length_mm / 10.0)
    inp.isModeled = modeled
    threads.add(inp)
