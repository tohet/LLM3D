import bpy
import os
import re
import mesh2txt

if __name__ == '__main__':
    for filename in os.listdir("E:/data"):
        txt_name = re.sub(".blend", ".txt", filename) 
        if txt_name in os.listdir("E:/txt_test"):
            print(f"{filename} is already parsed. Moving on.") 
        else:
            try:

                bpy.ops.wm.open_mainfile(filepath=f"E:/data/{filename}")
                mesh2txt.to_txt()
                print(f"Parsed {filename}")
            except:
                print(f"Failed to parse {filename}")
                continue