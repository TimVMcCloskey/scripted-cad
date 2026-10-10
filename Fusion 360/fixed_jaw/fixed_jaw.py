import adsk.core, adsk.fusion, traceback
import sys
import importlib
from . import fusion_cad_lib as cad

if "fusion_cad_lib" in sys.modules or f"{__name__}.fusion_cad_lib" in sys.modules:
    importlib.reload(cad)

body_width = 228
body_height = 74
body_depth = 80
mounting_hole_x = 54
mounting_hole_y = 52
trough_y = 30
trough_width = 148
trough_height = 44
trough_depth = 40
body_hole_x = body_width / 2 - 20
body_hole_z = 0
body_hole_depth = body_height
hole_radius = 10

        
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design, root_comp, planes = cad.init(app, { "body_width":               body_width,
                                                    "body_height":              body_height,
                                                    "body_depth":               body_depth,
                                                    "mounting_hole_x":          mounting_hole_x,
                                                    "mounting_hole_y":          mounting_hole_y,
                                                    "trough_y":                 trough_y,
                                                    "trough_width":             trough_width,
                                                    "trough_height":            trough_height,
                                                    "trough_depth":             trough_depth,
                                                    "body_hole_x":              body_hole_x,
                                                    "body_hole_z":              body_hole_z,
                                                    "body_hole_depth":          body_hole_depth,
                                                    "hole_radius":              hole_radius })
        
        
        
        ############################################################
        #
        # main body
        #
        #############################################################
        
        body_points = [
                    (0.0, 0.0), (228, 0.0), (228, 30), (188, 30),
                    (188, 74), (148, 74), (114, 40), (80, 74),
                    (40, 74), (40, 30), (0, 30)
                ]

        # Main body
        sketch = cad.make_custom_profile_sketch(root_comp, planes["xy"], body_points)
        body = cad.extrude_sketch(root_comp, sketch, "body_depth / 2", symmetric=True)
        cad.translate(root_comp, body, -body_width / 2, 0, 0)
        
        ############################################################
        # 
        # Mounting holes — both sides, cut through full depth
        #
        ############################################################
        
        hole_sketch = cad.make_circles_sketch( root_comp, planes["xy"], [
                                               (- mounting_hole_x,  mounting_hole_y, hole_radius),
                                               (mounting_hole_x, mounting_hole_y, hole_radius), ])
        
        cad.extrude_sketch(root_comp, hole_sketch, "body_depth", symmetric=True,
                           operation="cut", target_body=body, all_profiles=True)
        
        ############################################################
        # 
        # trough
        #
        ############################################################
        
        sketch = cad.make_rectangle_sketch( root_comp, planes["xy"], -trough_width / 2, trough_y, 
                                            trough_width / 2, trough_y + trough_height)
                                           
        cad.extrude_sketch(root_comp, sketch, "trough_depth / 2", symmetric=True, operation="cut", target_body=body)
                                            
        ############################################################
        # 
        # body holes
        #
        ############################################################
        
        top_plane = cad.make_plane(root_comp, "xz", body_height)

        sketch = cad.make_circles_sketch( root_comp, top_plane, [
                                         (-body_hole_x, body_hole_z, hole_radius),
                                         (body_hole_x, body_hole_z, hole_radius),] )
                                        
                                        
        cad.extrude_sketch( root_comp, sketch, "body_hole_depth", flip=True,
                            operation="cut", target_body=body, all_profiles=True)
                
        ui.messageBox("fixed_jaw complete!")        

    except Exception as e:
        import traceback
        ui.messageBox("Error:\n" + traceback.format_exc())
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
