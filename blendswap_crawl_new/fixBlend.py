import zipfile
import os
import shutil
import bpy

unzip_file = 'E:/tempfile'
data_path = 'E:/data'


def unzip(zip_file_path, target_path):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(target_path)
    zip_ref.close()


def find_blend_files(folder_path):
    blend_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".blend"):
                blend_files.append(os.path.join(root, file))
    return blend_files


def rename_file(src_file, new_name):
    dir_path = os.path.dirname(src_file)
    new_file_path = os.path.join(dir_path, new_name)
    os.rename(src_file, new_file_path)
    return new_file_path


def move(src_file, dst_file):
    if os.path.exists(dst_file):
        os.remove(dst_file)
    shutil.move(src_file, dst_file)
    return


def main():
    start_id = 23096
    end_id = 23098
    zip_file_path = os.path.join(data_path, "{}.blend")
    for id in range(start_id, end_id + 1):
        try:
            unzip(zip_file_path.format(id), unzip_file)
        except:
            continue
        blend_files = find_blend_files(unzip_file)
        print('---', id, ''.join(blend_files))
        for i in range(len(blend_files)):
            if i == 0:
                file_name = str(id) + '.blend'
            else:
                file_name = str(id) + '-{}.blend'.format(i)
            blend_files[i] = rename_file(blend_files[i], file_name)
            move(blend_files[i], os.path.join(data_path, file_name))
        shutil.rmtree(unzip_file)
    return

def unzip_blend(id):
    # start_id = 23096
    # end_id = 23098
    zip_file_path = os.path.join(data_path, "{}.blend")
    try:
        unzip(zip_file_path.format(id), unzip_file)
    except:
        pass
    blend_files = find_blend_files(unzip_file)
    print('---', id, ''.join(blend_files))
    for i in range(len(blend_files)):
        if i == 0:
            file_name = str(id) + '.blend'
        else:
            file_name = str(id) + '-{}.blend'.format(i)
        blend_files[i] = rename_file(blend_files[i], file_name)
        move(blend_files[i], os.path.join(data_path, file_name))
    shutil.rmtree(unzip_file)

if __name__ == '__main__':
    unzip_blend('23130')
