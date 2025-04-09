# from blendswap_crawl_new.utils import *
# from bs4 import BeautifulSoup
# import time
import pandas as pd
import os
import re
import json
import jsonlines

username = '396839479@qq.com'
password = '20020528lyk'


#https://blendswap.com/blend/29187
# base_url = 'https://blendswap.com/blend/{}'
# path_to_orig_csv = "D:/diploma/blenswap_orig_data.csv"
# df = pd.read_csv(path_to_orig_csv)
# title = df.loc[df['id'] == 29187]['title'].item()
# print(title)
# get mesh poly count

# save mesh as jsonl entry

def main():
    # get mesh name 
    entry_list = []
    txt_path = "D:/diploma/txt_100_kb/"
    path_to_orig_csv = "D:/diploma/blenswap_orig_data.csv"
    df = pd.read_csv(path_to_orig_csv)
    for file in os.listdir(txt_path):
        filename = os.fsdecode(file)
        with open(txt_path + filename, encoding='utf-8') as f:
            coords = f.read()
            exec(coords,globals())
            
        face_count = len(faces)
        #check_mesh_chars(orig_folder_path, filename, txt_train_path, True)
        mesh_id = int(re.sub(".txt", "", filename))#29187
        #print(mesh_id)
        #coords = ""
        try:
            title = df.loc[df['id'] == mesh_id]['title'].item()
            print(title)
            print(face_count)
            print(coords)

            entry = {
            "messages": [{"role": "user", "content":
                          f"""Create a 3D model of {title} that has {face_count} polygons.
Write coordinates of verteces and vertex definitions of polygons in the following format:
verts = [(-1.001, -1.043, 0.031), (1.123, -1.441, 0.124), (-1.124, 1.655, 1.331), (1.433, 1.1, 0.009), ...]
faces = [[0, 1, 3, 2], ... ]
where verts is a python list of tuples of x, y, z coordinates in 3D space and faces is a list of indeces for the verts list. Write only the coordinates and face definitions and nothing else. Create as many verteces and as many polygons as possible. Model as many parts of an object as possible.
                            """.strip()}, 
                        {"role": "assistant", "content": f"""
                            {coords}
                            """.strip()}]
            }

            entry_list.append(entry)
        except:
            print("Failed to get "+ str(mesh_id))
    # get mesh pol
    # with open(r"D:/diploma/test.jsonl", "r") as read_file:
    #     data = json.load(read_file)
    # with open('output2.jsonl', 'w') as outfile:
    #     for
    with jsonlines.open('output3.jsonl', 'w') as writer:
        writer.write_all(entry_list)

if __name__ == '__main__':
    main()