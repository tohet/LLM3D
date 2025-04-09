import bpy
import re

objects = bpy.data.objects

for obj in objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        
bpy.ops.object.join()

name = re.sub(".blend", ".txt", bpy.data.filepath.split('\\')[-1]) 

save_to_file = f'C:/Users/tohet/Desktop/учёба 2/попытка в 3D/{name}'
 
vertices = [(vert.co.x, vert.co.y, vert.co.z) for vert in bpy.context.object.data.vertices]
 
faces = [[vert for vert in polygon.vertices] for polygon in bpy.context.object.data.polygons]
 
with open(save_to_file, 'w') as file:
    file.write('verts = ' + str(vertices) + '\n' + 'faces = ' + str(faces) + '\n')
    file.close()