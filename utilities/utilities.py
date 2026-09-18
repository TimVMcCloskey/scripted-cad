import cadquery as cq
import vtk
from cadquery.vis import show
    
 
#******************************************
#
# cone
#
#****************************************** 

def cone(rad1, rad2, height, pnt_x, pnt_y, pnt_z, dir_x, dir_y, dir_z):

    return cq.Solid.makeCone(
        radius1=rad1,
        radius2=rad2,
        height=height,
        pnt=cq.Vector(pnt_x, pnt_y, pnt_z),
        dir=cq.Vector(dir_x, dir_y, dir_z)
    )



#******************************************
#
# cylinder
#
#****************************************** 

def cylinder(radius, height, pnt_x, pnt_y, pnt_z, dir_x, dir_y, dir_z):

    return cq.Solid.makeCylinder(
        radius=radius, 
        height=height,
        pnt=cq.Vector(pnt_x, pnt_y, pnt_z),
        dir=cq.Vector(dir_x, dir_y, dir_z)
    )


#******************************************
#
# torus
#
#****************************************** 

def torus(radius1, radius2, pnt_x, pnt_y, pnt_z, dir_x, dir_y, dir_z):

    return cq.Solid.makeTorus(
        radius1=radius1,
        radius2=radius2,
        pnt=cq.Vector(pnt_x, pnt_y, pnt_z),
        dir=cq.Vector(dir_x, dir_y, dir_z)
    )



#******************************************
#
# VIEW FUNCTIONS
#
#****************************************** 

def front(obj, zoom=1.0):

    """Front view — XY plane"""
    show(obj, elevation=0, azimuth=0, roll=0, zoom=zoom, clipping_range=(0.1, 10000))

def top(obj, zoom=1.0):

    """Top view — X right, Z down"""
    vtk.vtkObject.GlobalWarningDisplayOff()
    show(obj, elevation=-90, azimuth=0, roll=90, zoom=zoom,
         viewup=(0, 0, -1), clipping_range=(0.1, 10000))
    vtk.vtkObject.GlobalWarningDisplayOn()

def right(obj, zoom=1.0):

    """Right side view"""
    show(obj, elevation=0, azimuth=90, roll=0, zoom=zoom, clipping_range=(0.1, 10000))

def left(obj, zoom=1.0):

    """Left side view"""
    show(obj, elevation=0, azimuth=-90, roll=0, zoom=zoom, clipping_range=(0.1, 10000))

def iso(obj, zoom=1.0):

    """Isometric view"""
    show(obj, elevation=-35, azimuth=45, roll=0, zoom=zoom, clipping_range=(0.1, 10000))
