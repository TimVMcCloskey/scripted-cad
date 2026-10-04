# Scripted CAD --- Parametric Pipe Vise

A complete parametric 3D model of a mechanical pipe vise assembly
written in Python using **build123d** and the **Open CASCADE** geometry
kernel.

The project models the complete vise as scripted solid geometry rather
than a sequence of manual CAD operations. Dimensions and construction
logic are defined in source code, allowing the parts and assembly to be
revised, reproduced, version controlled, and exported for downstream CAD
and visualization workflows.

## Project Status

The pipe vise is now modeled as a **complete assembly in build123d**.
All vise components have been created, positioned into the assembled
model, and can also be displayed in an exploded configuration.

## Parts

The build123d project is organized into separate modules whose filenames
correspond to the modeled parts:

-   `fixed_jaw`
-   `moving_jaw`
-   `connecting_wages`
-   `spindle`
-   `handle`
-   `handle_cap`
-   `mounting_shaft`
-   `holding_pin`
-   `support_pin`

The project also contains:

-   `assembly` --- constructs and positions the complete pipe-vise
    assembly
-   `vise_utils.py` --- shared project utilities

The models use parameter-driven dimensions and scripted construction
operations including solid primitives, Boolean operations,
transformations, and threaded geometry.

## Assembly

Individual build123d parts are positioned programmatically to create the
complete pipe-vise assembly.

The project supports both:

-   **Assembled view** --- components positioned in their working
    mechanical relationship
-   **Exploded view** --- components separated to show part
    relationships and assembly structure

## CAD Pipeline

``` text
Named Parameters
      ↓
Python + build123d
      ↓
Open CASCADE B-rep Solids
      ↓
Assembly / Exploded Configuration
      ↓
STEP / glTF Export
      ↓
FreeCAD / Blender / Engineering Visualization
```

## CastVR Integration

The completed pipe-vise assembly was exported from the build123d
workflow and imported into **CastVR**, my C/OpenGL/OpenXR application
for interactive visualization of mechanical CAD assemblies in VR.

This demonstrates an end-to-end workflow from parameter-driven CAD
geometry to an interactive 3D engineering application:

``` text
Python / build123d
      ↓
CAD Geometry
      ↓
Exported Assembly
      ↓
CastVR
      ↓
Interactive VR Visualization
```

In CastVR, the pipe vise can be viewed as a mechanical assembly and used
with interactive assembly features such as explode/assemble
visualization.

## Dependencies

``` bash
pip install build123d bd-warehouse
```

The project uses **build123d**, **Open CASCADE**, **bd_warehouse**, STEP
and glTF export, FreeCAD for CAD inspection, and Blender for
presentation and rendering.

## Why Scripted CAD?

Traditional CAD workflows typically store a model as a sequence of
interactive modeling operations. In this project, the geometry is
expressed directly as source code.

That makes dimensions and construction logic explicit and makes the
model suitable for:

-   Version control with Git
-   Reproducible geometry generation
-   Parameter-driven design changes
-   Automated generation of design variants
-   CAD automation and computational design workflows
-   Integration with other Python engineering tools

## Author

**Tim McCloskey** --- Algorithmic 3D Modeling and Parametric CAD
Automation · Denver, CO

Portfolio: timvmccloskey.github.io\
GitHub: github.com/TimVMcCloskey
