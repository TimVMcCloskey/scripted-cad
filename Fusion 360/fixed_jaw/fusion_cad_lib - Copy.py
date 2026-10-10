# =========================================================================
# REUSABLE LIBRARY BACKEND: fusion_cad_lib.py
# =========================================================================
import adsk.core, adsk.fusion

def init_parameter(design, name, value, unit="mm"):
    """Pushes variables to Fusion's global user parameters table (Converts mm to cm internally)."""
    params = design.userParameters
    existing = params.itemByName(name)
    if not existing:
        params.add(name, adsk.core.ValueInput.createByReal(value / 10.0), unit, "") 
    return params.itemByName(name)

def make_box(root_comp, plane, x1, y1, x2, y2, depth_formula, is_symmetric=True):
    """Draws a standard 2D rectangle and extrudes it into a clean solid body object."""
    sketches = root_comp.sketches
    extrudes = root_comp.features.extrudeFeatures
    
    sketch = sketches.add(plane)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0)
    )
    
    ext_input = extrudes.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(True, adsk.core.ValueInput.createByString(depth_formula))
    ext_input.isSymmetric = is_symmetric
    
    feat = extrudes.add(ext_input)
    return feat.bodies.item(0)

def make_custom_profile_box(root_comp, plane, points_list, depth_formula, is_symmetric=False):
    """
    UPGRADED SPECIFICALLY FOR THE MOVING JAW:
    Draws a continuous string of 2D points to map the stepped staircase profile, 
    closes the loop, and extrudes it into a solid tool body.
    """
    sketches = root_comp.sketches
    extrudes = root_comp.features.extrudeFeatures
    
    sketch = sketches.add(plane)
    lines = sketch.sketchCurves.sketchLines
    
    # Draw line segments point-to-point sequentially
    for i in range(len(points_list) - 1):
        pt1 = adsk.core.Point3D.create(points_list[i][0], points_list[i][1], 0)
        pt2 = adsk.core.Point3D.create(points_list[i+1][0], points_list[i+1][1], 0)
        lines.addByTwoPoints(pt1, pt2)
        
    # Close the boundary loop from the final index back to origin zero point
    pt_last = adsk.core.Point3D.create(points_list[-1][0], points_list[-1][1], 0)
    pt_first = adsk.core.Point3D.create(points_list[0][0], points_list[0][1], 0)
    lines.addByTwoPoints(pt_last, pt_first)
    
    ext_input = extrudes.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(True, adsk.core.ValueInput.createByString(depth_formula))
    ext_input.isSymmetric = is_symmetric
    
    feat = extrudes.add(ext_input)
    return feat.bodies.item(0)

def make_cylinder(root_comp, plane, x, y, radius, depth_formula=None, is_infinite=False, rotate_axis_deg=None):
    """Draws a circle profile and extrudes it symmetrically into a solid cutting pin."""
    sketches = root_comp.sketches
    extrudes = root_comp.features.extrudeFeatures
    
    sketch = sketches.add(plane)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x, y, 0), radius)
    
    ext_input = extrudes.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    
    if is_infinite:
        ext_input.setAllExtent(adsk.fusion.ExtentDirections.SymmetricExtentDirection)
    else:
        ext_input.setDistanceExtent(True, adsk.core.ValueInput.createByString(depth_formula))
        ext_input.isSymmetric = True
        
    feat = extrudes.add(ext_input)
    body = feat.bodies.item(0)
    
    # Custom axial shift adjustment mechanism to handle horizontal grove operations
    if rotate_axis_deg:
        moves = root_comp.features.moveFeatures
        bodies_coll = adsk.core.ObjectCollection.create()
        bodies_coll.add(body)
        
        # Rotates around local component origin X-axis
        axis = root_comp.xConstructionAxis
        angle = adsk.core.ValueInput.createByReal(rotate_axis_deg * 3.14159 / 180.0)
        
        move_input = moves.createMoveInput(bodies_coll)
        move_input.defineAsRotate(axis, angle)
        moves.add(move_input)
        
    return body

def make_cone(root_comp, plane, x, y, z, r_bottom, r_top, height, rotate_x_deg=0):
    """
    UPGRADED FOR COUNTERSINK HOLES:
    Fusion doesn't have a direct primitive 'Cone' command. We sketch two separate concentric circles 
    on offset structural planes and run a Parametric Loft Feature, matching build123d's Cone execution!
    """
    sketches = root_comp.sketches
    lofts = root_comp.features.loftFeatures
    
    # 1. Base Sketch Circle
    sketch_base = sketches.add(plane)
    # Handle zero point vertex tip limit cleanly
    r_b_val = r_bottom if r_bottom > 0 else 0.001 
    sketch_base.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x, y, z), r_b_val)
    
    # 2. Setup Offset Plane for Cone height ceiling limit
    planes = root_comp.constructionPlanes
    plane_input = planes.createInput()
    plane_input.setByOffset(plane, adsk.core.ValueInput.createByReal(height))
    offset_plane = planes.add(plane_input)
    
    # 3. Top Ceiling Sketch Circle
    sketch_top = sketches.add(offset_plane)
    sketch_top.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x, y, 0), r_top)
    
    # 4. Bind profiles into the parametric Loft blueprint configuration
    loft_input = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loft_input.loftSections.add(sketch_base.profiles.item(0))
    loft_input.loftSections.add(sketch_top.profiles.item(0))
    
    loft_feat = lofts.add(loft_input)
    body = loft_feat.bodies.item(0)
    
    # Apply rotational pitch transformation corrections if target bit is inverted
    if rotate_x_deg != 0:
        moves = root_comp.features.moveFeatures
        coll = adsk.core.ObjectCollection.create()
        coll.add(body)
        axis = root_comp.xConstructionAxis
        angle = adsk.core.ValueInput.createByReal(rotate_x_deg * 3.14159 / 180.0)
        move_input = moves.createMoveInput(coll)
        move_input.defineAsRotate(axis, angle)
        moves.add(move_input)
        
    return body

def boolean_combine(root_comp, target_body, tool_bodies_list, operation_mode="cut"):
    """Performs a solid boolean operation (Cut/Union/Intersection) using an array collection."""
    tool_collection = adsk.core.ObjectCollection.create()
    for body in tool_bodies_list:
        tool_collection.add(body)
        
    combine_feats = root_comp.features.combineFeatures
    combine_input = combine_feats.createInput(target_body, tool_collection)
    
    if operation_mode.lower() == "cut":
        combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    elif operation_mode.lower() == "union":
        combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
        
    combine_feats.add(combine_input)

def make_prism_wedge(root_comp, plane, p1_tup, p2_tup, p3_tup, depth_formula):
    """
    FIXES FIXED JAW ERROR:
    Draws a 3-point triangular loop face using coordinate tuples and 
    extrudes it symmetrically into a sharp wedge solid cutting tool body.
    """
    sketches = root_comp.sketches
    extrudes = root_comp.features.extrudeFeatures
    
    sketch = sketches.add(plane)
    p_lines = sketch.sketchCurves.sketchLines
    
    # Extract the X and Y indices from the passed point tuples
    pt1 = adsk.core.Point3D.create(p1_tup[0], p1_tup[1], 0)
    pt2 = adsk.core.Point3D.create(p2_tup[0], p2_tup[1], 0)
    pt3 = adsk.core.Point3D.create(p3_tup[0], p3_tup[1], 0)
    
    # Trace the perimeter of the cutting triangle
    p_lines.addByTwoPoints(pt1, pt2)
    p_lines.addByTwoPoints(pt2, pt3)
    p_lines.addByTwoPoints(pt3, pt1)
    
    # Extrude symmetrically as an independent solid block
    ext_input = extrudes.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(True, adsk.core.ValueInput.createByString(depth_formula))
    ext_input.isSymmetric = True
    
    feat = extrudes.add(ext_input)
    return feat.bodies.item(0)
    
def boolean_subtract(root_comp, target_body, tool_bodies_list):
    """
    UNIVERSAL LIBRARY ALIAS:
    Redirects old 'boolean_subtract' calls to the new 'boolean_combine' 
    engine configured for solid body cutting operations.
    """
    return boolean_combine(root_comp, target_body, tool_bodies_list, operation_mode="cut")


