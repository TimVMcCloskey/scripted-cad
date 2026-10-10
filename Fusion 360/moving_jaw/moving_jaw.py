import adsk.core, adsk.fusion, traceback
import sys
import importlib
from . import fusion_cad_lib as cad

if "fusion_cad_lib" in sys.modules or f"{__name__}.fusion_cad_lib" in sys.modules:
    importlib.reload(cad)
    
BODY_WIDTH  = 84.0
BODY_HEIGHT = 65.0
BODY_DEPTH  = 32.0

# Pin hole locks spindle
PIN_HOLE_X = BODY_WIDTH / 2 - 30.0  # X position
PIN_HOLE_Y = 55.0  # Y position
PIN_HOLE_RADIUS = 2.75  # radius (5.5mm diameter)

# Guiding groove
GUIDE_GROOVE_X = 54  # X center of arc circle
GUIDE_GROOVE_Y = BODY_HEIGHT
GUIDE_GROOVE_Z = 0.0  
GUIDE_GROOVE_RADIUS = 20.0  # radius of arc circle

# Middle hole
MIDDLE_HOLE_X = 0.0  
MIDDLE_HOLE_Y = BODY_HEIGHT 
MIDDLE_HOLE_Z = 0.0
MIDDLE_HOLE_DEPTH = 20.0 
 
MIDDLE_HOLE_RADIUS = 12.0 
MIDDLE_HOLE_CONE_Y = MIDDLE_HOLE_DEPTH

CHAMFER_R1 = 13.2  # outer radius of top chamfer
CHAMFER_R2 = 12.0  # inner radius of top chamfer
CHAMFER_HEIGHT = 1.2  # height of top chamfer

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design, root_comp, planes = cad.init(app, { "BODY_WIDTH":           BODY_WIDTH,
                                                    "BODY_HEIGHT":          BODY_HEIGHT,
                                                    "BODY_DEPTH":           BODY_DEPTH,
                                                    "PIN_HOLE_X":           PIN_HOLE_X,
                                                    "PIN_HOLE_Y":           PIN_HOLE_Y,
                                                    "PIN_HOLE_RADIUS":      PIN_HOLE_RADIUS,
                                                    "GUIDE_GROOVE_X":       GUIDE_GROOVE_X,
                                                    "GUIDE_GROOVE_Y":       GUIDE_GROOVE_Y,
                                                    "GUIDE_GROOVE_Z":       GUIDE_GROOVE_Z,
                                                    "GUIDE_GROOVE_RADIUS":  GUIDE_GROOVE_RADIUS,
                                                    "MIDDLE_HOLE_X":        MIDDLE_HOLE_X,
                                                    "MIDDLE_HOLE_Y":        MIDDLE_HOLE_Y,
                                                    "MIDDLE_HOLE_Z":        MIDDLE_HOLE_Z,
                                                    "MIDDLE_HOLE_DEPTH":    MIDDLE_HOLE_DEPTH,
                                                    "MIDDLE_HOLE_RADIUS":   MIDDLE_HOLE_RADIUS,
                                                    "MIDDLE_HOLE_CONE_Y":   MIDDLE_HOLE_CONE_Y,                                                    
                                                    "CHAMFER_R1":           CHAMFER_R1,  
                                                    "CHAMFER_R2":           CHAMFER_R2,
                                                    "CHAMFER_HEIGHT":       CHAMFER_HEIGHT })

       
        ############################################################
        #
        #  make main body
        #
        ###########################################################
        
        stepped_points = [
            (0.0, 0.0), (12, 0.0), (12, 5), (17, 5),
            (17, 10), (22, 10), (22, 15), (27, 15),
            (27, 20), (32, 20), (32, 25), (37, 25),
            (37, 30), (42, 30), (42, 65), (0.0, 65)
        ]
        
        sketch = cad.make_custom_profile_sketch(root_comp, planes["xy"], stepped_points)
        half_body = cad.extrude_sketch(root_comp, sketch, "BODY_DEPTH / 2", symmetric=True)
        cad.translate(root_comp, half_body, -BODY_WIDTH / 2, 0, 0)
        mirrored = cad.mirror(root_comp, half_body, "yz")
        body = cad.join(root_comp, half_body, mirrored)
               
        ############################################################
        #
        #  drill holes
        #
        ###########################################################
        
        # PIN HOLE — symmetric, cuts full depth centered at Z=0
        sketch = cad.make_circles_sketch( root_comp, planes["xy"], [
                                        ( PIN_HOLE_X, PIN_HOLE_Y, PIN_HOLE_RADIUS),
                                        ( -PIN_HOLE_X, PIN_HOLE_Y, PIN_HOLE_RADIUS), ])
                                        
        cad.extrude_sketch( root_comp, sketch, "BODY_DEPTH", symmetric=True,
                            operation="cut", target_body=body, all_profiles=True )

        ###########################################################
        #
        # GUIDE GROOVES — both sides, cut down from top face
        #
        ###########################################################
        
        top_plane = cad.make_plane(root_comp, "xz", BODY_HEIGHT)

        sketch = cad.make_circles_sketch( root_comp, top_plane, [
                                        (GUIDE_GROOVE_X, GUIDE_GROOVE_Z, GUIDE_GROOVE_RADIUS),
                                        (-GUIDE_GROOVE_X, GUIDE_GROOVE_Z, GUIDE_GROOVE_RADIUS),] )
                                        
        cad.extrude_sketch( root_comp, sketch, "BODY_HEIGHT", flip=True,
                            operation="cut", target_body=body, all_profiles=True)
        
        ###########################################################
        #
        # MIDDLE HOLE — opens from top face (Y = BODY_HEIGHT), runs down along Y
        #
        ###########################################################
        
        top_plane = cad.make_plane(root_comp, "xz", "BODY_HEIGHT")

        # 1. Main bore
        sketch = cad.make_circle_sketch(root_comp, top_plane, MIDDLE_HOLE_X, MIDDLE_HOLE_Z, MIDDLE_HOLE_RADIUS)
        cad.extrude_sketch( root_comp, sketch, "MIDDLE_HOLE_DEPTH", flip=True,
                            operation="cut", target_body=body)

        # 2. Top chamfer (annular ring at entrance)
        sketch = cad.make_circles_sketch( root_comp, top_plane,                                          
                                          [(MIDDLE_HOLE_X, MIDDLE_HOLE_Z, CHAMFER_R1),
                                          (MIDDLE_HOLE_X, MIDDLE_HOLE_Z, CHAMFER_R2), ])
        cad.extrude_sketch( root_comp, sketch, "CHAMFER_HEIGHT", flip=True,
                            operation="cut", target_body=body,
                            all_profiles=True, taper_angle=45.0 )

        # 3. Drill point cone — plane at bottom of bore
        cone_plane = cad.make_plane(root_comp, "xz", "BODY_HEIGHT - MIDDLE_HOLE_DEPTH")
        
        sketch = cad.make_circle_sketch(root_comp, cone_plane, MIDDLE_HOLE_X, MIDDLE_HOLE_Z, MIDDLE_HOLE_RADIUS)
        cad.extrude_sketch( root_comp, sketch, "MIDDLE_HOLE_CONE_Y", flip=True,
                            operation="cut", target_body=body,
                            taper_angle=-59.0 )
                            
        ui.messageBox("moving_jaw complete!")
        
    except Exception as e:
        import traceback
        ui.messageBox("Error:\n" + traceback.format_exc())
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
