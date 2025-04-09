folder = "D:/diploma/txt_100_kb/"
file_name = "29187.txt"
#execfile(folder+file_name)
# with open(folder+file_name) as f:
with open("C:/Users/Тоня/Desktop/beer_mus_gml_test2.txt") as f:
    exec(f.read())

import bpy
mesh_data = bpy.data.meshes.new("new_mesh")
mesh_data.from_pydata(verts, [], faces)
mesh_data.update()
mesh = bpy.data.objects.new("new_mesh", mesh_data)
bpy.context.scene.collection.objects.link(mesh)