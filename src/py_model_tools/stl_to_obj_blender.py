import bpy
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

stl_in = argv[0]
obj_out = argv[1]

# Please be aware of this axis_forward and axiz_up parameter,
# becarefull upon convertion that the axis are correct
bpy.ops.import_mesh.stl(filepath=stl_in)
bpy.ops.export_scene.obj(filepath=obj_out, axis_forward='Y', axis_up='Z',
                         use_materials=False)
