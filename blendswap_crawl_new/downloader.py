"""
page,id,title,cc,download,like,is_download
1,1588,5 Point Lighting Setup,CC-0,1744,4,no
1,1589,Cocktail Shaker,CC-0,250,3,yes
"""
import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime
import signal
import re
import os
import bpy
import mesh2txt
from contextlib import contextmanager
import func_timeout
import getCookie
import fixBlend

download_num_per_cookie = 10
max_file_size = 100
min_file_size = 0.00018310546875
csv_file_path = 'data_original_reversed_copy.csv'
start_line = 0 
download_path = 'E:/data/'
base_url = 'https://blendswap.com/blend/{}/download'
max_download_time = 600
keyword = ''

class TimeoutException(Exception): pass

def contains1(text, keyword):
    pattern = r'\b{}\b'.format(keyword)
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False

def contains(text, keyword:str):
    if keyword=='':
        return True
    words = keyword.split('-')
    res = False
    for word in words:
        if word != '':
            res = res or contains1(text=text, keyword=word)
    return res
    
    
def timeout_handler(signum, frame):
    raise TimeoutError("timeout....")


def download(id, cookie):
    """
    :param id:
    :return:
    """
    url = base_url.format(id)
    cookie = {
        'session': cookie
    }
    signal.signal(signal.SIGABRT, timeout_handler)
    #signal.alarm(max_download_time)
    try:
        response = requests.get(url, cookies=cookie, stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        total_size_MB = total_size / (1024 * 1024)
        is_download = 'no'
        path = 'no'
        if total_size == 0:
            print('Download quota used up... or cookie invalid...')
            return ['no', 'no', 'no']
        if min_file_size < total_size_MB <= max_file_size:
            filename = str(id) + '.blend'
            path = download_path + filename
            progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
            with open(path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))
            progress_bar.close()
            is_download = 'yes'
    except TimeoutError as e:
        print(e)
        return ['no', 'no', 'no']
    return [is_download, str(total_size_MB), path]

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        print("Timed out!")
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def parse_mesh():
    try:
        mesh2txt.to_txt()
    except:
        print("Mesh2txt failed!")
        raise(Exception)

def main():
    try:
        df = pd.read_csv(csv_file_path)
    except:
        df = pd.read_csv(csv_file_path, encoding = 'utf-8')
    with open('cookie.txt', 'r') as f:
        cookie = f.read()
    cookieList = cookie.strip().split('\n')
    cookie = cookieList.pop(0)
    print('--------------------------------------\ncookie:', cookie)

    # from getCookie import CookieMaker
    # cookieMaker = CookieMaker(headless=True, implicitlyWait=5)
    # print("-------------------------------")
    # print("create cookie...")
    # cookie = cookieMaker.getCookie()
    # print(cookie)
    cookie_create = True
    download_count = 0
    cookieMaker = getCookie.CookieMaker(headless=True, implicitlyWait=1)
    while True:
        for line_index in range(start_line, len(df)):

            try:

                line = df.iloc[line_index]
                if line['is_download'] == 'no':
                    id = line['id']
                    title = line['title']
                    if not contains(title, keyword):
                        continue

                    #if filename already in data
                    id_as_blend = str(id) + ".blend"
                    if id_as_blend in os.listdir("E:/data"):
                        print(f"{id_as_blend} is already downloaded. Moving on.")
                        #continue

                    print('start downloading...  id:', id, 'title:',title)
                    #try:
                    data = download(id, cookie)
                    #except:
                        #data = ['no', 'no', 'no']
                    df.loc[line_index, ['is_download', 'size(MB)', 'path']] = data
                    df.to_csv(csv_file_path, index=False)
                    current_datetime = datetime.now()
                    print('time:', current_datetime.date(), current_datetime.time())
                    print('id:', line['id'], line['title'], data)
                    download_count += 1

                    id_as_txt = str(id) + ".txt"
                    if id_as_txt not in os.listdir("C:/Users/tohet/Desktop/txt_test/"):
                        try:
                            try:
                                bpy.ops.wm.open_mainfile(filepath=f"E:/data/{id_as_blend}")
                            except:
                                fixBlend.unzip_blend(id)
                                bpy.ops.wm.open_mainfile(filepath=f"E:/data/{id_as_blend}")
                            mesh2txt.to_txt()
                            print(f"Parsed {id_as_blend}")
                            bpy.ops.wm.quit_blender()
                        except:
                            print(f"Failed to parse {id_as_blend}")
                    else:
                        print(f"{id_as_blend} is already parsed.")

                    if download_count >= download_num_per_cookie or data == ['no', 'no', 'no']:
                        download_count = 0
                        print("-------------------------------")
                        print("update cookie...")

                        # open cookie.txt file
                        # delete the previous cookie
                        # get cookie list again

                        #if cookie_create == True:
                            #try:
                        while True:
                            cookie = cookieMaker.getCookie()
                            if cookie != "1":
                                break
                            else:
                                print("Cookie is 1 again")
                            #except:
                                #print("Get cookie failed")
                            #finally:
                                #cookie_create = False

                        #else:
                            #cookie = cookieList.pop()
                            #cookie_create = True
                        print('--------------------------------------\ncookie:', cookie)


            except:
                print("Download error. Moving on.")
                continue



        for line_index in range(start_line, len(df)):
            line = df.iloc[line_index]
            if line['is_download'] == 'no':
                continue
        break


if __name__ == '__main__':
    main()

