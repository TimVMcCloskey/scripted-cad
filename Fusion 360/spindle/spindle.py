import adsk.core, adsk.fusion, traceback
import sys
import importlib
import math
from . import fusion_cad_lib as cad

if "fusion_cad_lib" in sys.modules or f"{__name__}.fusion_cad_lib" in sys.modules:
    importlib.reload(cad)
    
#******************************************
#
# DIMENSIONS
#
#******************************************

THREAD_LENGTH    = 160.0

NECK_RADIUS    = 15.0
NECK_HEIGHT    = 10.0
NECK_Y         = THREAD_LENGTH

TOP_RADIUS      = 23.0
TOP_HEIGHT      = 30.0
TOP_HOLE_RADIUS = 9.0
TOP_Y           = NECK_Y + NECK_HEIGHT

BOTTOM_RADIUS    = 12.0
BOTTOM_HEIGHT    = 20.0
BOTTOM_Y         = -BOTTOM_HEIGHT

GROOVE_RADIUS        = 3.0
GROOVE_CENTER_RADIUS = 12.0
GROOVE_Y             = BOTTOM_Y + 10.0


CORE_RADIUS = 13.835

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design, root_comp, planes = cad.init(app, { "THREAD_LENGTH":        THREAD_LENGTH,
                                                    "NECK_RADIUS":          NECK_RADIUS,
                                                    "NECK_Y":               NECK_Y,
                                                    "TOP_RADIUS":           TOP_RADIUS,
                                                    "TOP_HEIGHT":           TOP_HEIGHT,
                                                    "TOP_HOLE_RADIUS":       TOP_HOLE_RADIUS,
                                                    "TOP_Y":                TOP_Y,
                                                    "BOTTOM_RADIUS":        BOTTOM_RADIUS,
                                                    "BOTTOM_HEIGHT":        BOTTOM_HEIGHT,
                                                    "BOTTOM_Y":             BOTTOM_Y,
                                                    "GROOVE_RADIUS":        GROOVE_RADIUS,
                                                    "GROOVE_CENTER_RADIUS": GROOVE_CENTER_RADIUS,
                                                    "GROOVE_Y":             GROOVE_Y,
                                                    "CORE_RADIUS":          CORE_RADIUS })

                                                                                                    
        profile_points = [
            (0,            BOTTOM_Y),                    # (0, -20)
            (BOTTOM_RADIUS, BOTTOM_Y),                   # (12, -20)
            (BOTTOM_RADIUS, 0),                          # (12, 0)
            (CORE_RADIUS,  0),                           # (13.835, 0)
            (CORE_RADIUS,  THREAD_LENGTH),               # (13.835, 160)
            (NECK_RADIUS,  NECK_Y),                      # (15, 160)
            (NECK_RADIUS,  NECK_Y + NECK_HEIGHT),        # (15, 170)
            (TOP_RADIUS,   TOP_Y),                       # (23, 170)
            (TOP_RADIUS,   TOP_Y + TOP_HEIGHT),          # (23, 200)
            (0,            TOP_Y + TOP_HEIGHT),          # (0, 200)
        ]

        ###########################################################
        #
        # spindle body
        #
        ###########################################################
        
        y_axis = root_comp.yConstructionAxis

        sketch = cad.make_custom_profile_sketch(root_comp, planes["xy"], profile_points)
        body = cad.revolve_sketch(root_comp, sketch, y_axis)

        # Groove cut — circle in XY plane at (GROOVE_CENTER_RADIUS, GROOVE_Y)
        groove_sketch = cad.make_circle_sketch(root_comp, planes["xy"],
                                                GROOVE_CENTER_RADIUS, GROOVE_Y, GROOVE_RADIUS)
        cad.revolve_sketch(root_comp, groove_sketch, y_axis,
                           operation="cut", target_body=body)
                           
        ###########################################################
        #
        # top hole
        #
        ###########################################################         
                                                       
        hole_sketch = cad.make_circle_sketch(root_comp, planes["xy"],
                                      0, TOP_Y + TOP_HEIGHT / 2, TOP_HOLE_RADIUS)
                                                      
        cad.extrude_sketch( root_comp, hole_sketch, "TOP_RADIUS", symmetric=True,
                            operation="cut", target_body=body)
        

        ###########################################################
        #
        # thread
        #
        ###########################################################   
        
        cad.make_thread(root_comp, body, CORE_RADIUS,
                "ACME Screw Threads", "1.2500", "2G", THREAD_LENGTH,
                modeled=True)

            
            
        ###########################################################
        #
        # finished
        #
        ########################################################### 
        
        ui.messageBox("spindle complete!")
        
    except Exception as e:
        import traceback
        ui.messageBox("Error:\n" + traceback.format_exc())
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
