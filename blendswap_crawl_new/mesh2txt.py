import bpy
import re
import time
from wrapt_timeout_decorator import *
from conf_my_program import conf_my_program

def to_txt():

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    objects = bpy.data.objects

    for obj in objects:
        if obj.type == 'MESH':
            try:
                obj.select_set(True)
            except:
                pass
            
    bpy.ops.object.join()

    name = re.sub(".blend", ".txt", bpy.data.filepath.split('\\')[-1]) 

    save_to_file = f'C:/Users/tohet/Desktop/txt_test/{name}'
    
    vertices = [(vert.co.x, vert.co.y, vert.co.z) for vert in bpy.context.object.data.vertices]
    
    faces = [[vert for vert in polygon.vertices] for polygon in bpy.context.object.data.polygons]

    # rewrite to put the text in a .csv file

    with open(save_to_file, 'w') as file:
        file.write('verts = ' + str(vertices) + '\n' + 'faces = ' + str(faces) + '\n')
        file.close()

    print(f"{name} converted to text")

def open_n_parse(id):
    print("Start ", conf_my_program.name)
    id_as_blend = str(id) + ".blend"
    bpy.ops.wm.open_mainfile(filepath=f"E:/data/{id_as_blend}")
    to_txt()
    bpy.ops.wm.quit_blender()

if __name__ == '__main__':
     open_n_parse('30806')