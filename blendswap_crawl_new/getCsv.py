"""
page,id,title,cc,download,like
1,1588,5 Point Lighting Setup,CC-0,1744,4
1,1589,Cocktail Shaker,CC-0,250,3
"""

from utils import *
import time
from bs4 import BeautifulSoup
import pandas as pd

start_page = 0
end_page = 1
wait_time_after_load_page = 3
username = '396839479@qq.com'
password = '20020528lyk'


def perItem(driver, xp, page):
    """
    :param driver:
    :return:
    """
    elem = xpath(driver, xp)
    html = getInnerHtml(driver, elem)
    soup = BeautifulSoup(html, "html.parser")
    id = int(soup.find('a').get("href").split('/')[-1])
    title = xpath(driver, xp + """/div/div/div[1]""").text
    data = xpath(driver, xp + """/div/div/div[2]""").text
    cc, download, like = data.replace(',', '').replace('"', '').split('\n')
    res = [page, id, title, cc, download, like, 'no', 'no', 'no']
    print(f"page:{page}", res)
    return res


def perPage(driver, page):
    """
    :param driver:
    :param page:
    :return:
    """
    driver.get("https://blendswap.com/blends/{}/oldest".format(page))
    time.sleep(wait_time_after_load_page)
    # driver.execute_script("document.querySelector('.close-button').click();")
    print("start... page {}".format(page))
    data = []
    itemID = 0
    baseXpath = """/html/body/div/div[2]/div[{}]"""
    allowFailTimes = 2
    failTime = 0
    while True:
        try:
            itemID += 1
            data.append(perItem(driver, baseXpath.format(itemID), page))
        except:
            failTime += 1
            print('fail, page:{}, itemID:{}'.format(page, itemID))
            if failTime > allowFailTimes:
                break
    print(len(data), f"pieces of information have been collected in page {page}.")
    return data


def main():
    driver = driverInit()
    login(driver, username, password)
    time.sleep(3)
    try:
        df = pd.read_csv('data.csv')
    except:
        df = pd.read_csv('data.csv', encoding='utf-8')
    for page in range(start_page, end_page + 1):
        pageData = perPage(driver, page)
        new_df = pd.DataFrame(pageData, columns=df.columns)
        df = pd.concat([df, new_df], ignore_index=True)
        try:
            df.to_csv('data.csv', index=False)
        except:
            print("Error saving file.")


if __name__ == '__main__':
    main()
