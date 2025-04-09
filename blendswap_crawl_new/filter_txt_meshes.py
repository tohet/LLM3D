import os
import shutil

#takes
def check_mesh_chars(folder_path, txt_mesh_path, train_path, approximating):
    full_mesh_path = folder_path + txt_mesh_path
    # check file size - must be under 200 kb (204800 bytes) (roughly 100k tokens and 2000)
    # must also be higher than 10 to exclude all particle tests
    # 104800 bytes for 1000 faces
    if os.path.getsize(full_mesh_path) > 10240 and os.path.getsize(full_mesh_path) < 104800:
        # create verts and faces litst
        print(full_mesh_path)
        with open(full_mesh_path) as f:
            exec(f.read(),globals())
        # calculate the amount of quads and check if it exeeds all other face types
        vert_valences = [len(x) for x in faces]
        try:
            vert_mode = max(set(vert_valences), key=vert_valences.count)

            # check if mode is 4
            if vert_mode == 4:
                # save the txt in another folder for training
                
                if approximating:
                    approx_by = 3
                    vertices = [(round(vert[0], approx_by), round(vert[1], approx_by), round(vert[2], approx_by)) for vert in verts]
                    new_mesh_path = train_path + txt_mesh_path

                    with open(new_mesh_path, 'w') as file:
                        file.write('verts = ' + str(vertices) + '\n' + 'faces = ' + str(faces) + '\n')
                        file.close()
                else:
                    shutil.copy(full_mesh_path, train_path)

                
        except:
            print("Failed to count mesh faces")
        pass
    pass

# quantization ?
# 0.22169925272464752 - vert in data (18 nums after dot 8 tokens)
# 0.854431 m(?)


if __name__ == '__main__':
    # orig_folder_path = "D:/diploma/txt_test/"
    # txt_train_path = "D:/diploma/txt_model_train/"

    orig_folder_path = "D:/diploma/txt_model_train/"
    txt_train_path = "D:/diploma/txt_100_kb/"
    for file in os.listdir(orig_folder_path):
        filename = os.fsdecode(file)
        check_mesh_chars(orig_folder_path, filename, txt_train_path, True)