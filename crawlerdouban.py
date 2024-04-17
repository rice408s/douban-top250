import threading
import pandas as pd  # type: ignore
import requests
import re
from bs4 import BeautifulSoup  # type: ignore
from utools import Get_movie_url_list, Add_to_excel,headers, mainUrl



# 定义电影类
class Movie:
    def __init__(
        self,
        title,
        director,
        screenwriter,
        region,
        language,
        release_time,
        length,
        other_name,
        introduction,
        rate,
        url,
        INDb,
    ):
        self.title = title
        self.director = director
        self.screenwriter = screenwriter
        self.region = region
        self.language = language
        self.release_time = release_time
        self.length = length
        self.other_name = other_name
        self.introduction = introduction
        self.rate = rate
        self.url = url
        self.INDb = INDb



# 数据处理函数
def data_is_null(data):
    if data:
        return data[0]
    else:
        return ""


def Get_movie_info(url, header, movie_list=[]):
    print("downloading:", url, "......\n")
    res = requests.get(url=url, headers=header)
    context = res.text

    soup = BeautifulSoup(context, "html.parser")
    title = soup.find("span", property="v:itemreviewed").get_text()
    introduction = soup.find("span", property="v:summary").get_text().strip()
    rate = soup.find("strong", property="v:average").get_text().strip()
    info = soup.find("div", id="info").get_text()
    director = data_is_null(re.findall("导演: (.*?)\n", info, re.S))
    screenwriter = data_is_null(re.findall("编剧: (.*?)\n", info, re.S))
    region = data_is_null(re.findall("制片国家/地区: (.*?)\n", info, re.S))
    language = data_is_null(re.findall("语言: (.*?)\n", info, re.S))
    release_time = data_is_null(re.findall("上映日期: (.*?)\n", info, re.S))
    length = data_is_null(re.findall("片长: (.*?)\n", info, re.S))
    other_name = data_is_null(re.findall("又名: (.*?)\n", info, re.S))
    INDb = re.findall("IMDb: (.*?)\n", info, re.S)[0]

    mv = Movie(
        title,
        director,
        screenwriter,
        region,
        language,
        release_time,
        length,
        other_name,
        introduction,
        rate,
        url,
        INDb,
    )
    movie_list = movie_list.append(mv)


# 每个线程的任务
def get_movie_info_in_thread(url_list, header, movie_list):
    for url in url_list:
        Get_movie_info(url, header, movie_list)


# 爬虫函数
def Spider(url, header):
    print("downloading:", url)
    # 获取电影url列表
    url_list = Get_movie_url_list()
    movie_list = []
    threads = []

    url_parts = [url_list[i : i + 10] for i in range(0, len(url_list), 10)]
    for i in url_parts:
        t = threading.Thread(
            target=get_movie_info_in_thread, args=(i, header, movie_list)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # 将movie_list的url按照page_url_list的顺序排序
    movie_list = sorted(movie_list, key=lambda x: url_list.index(x.url))
    Add_to_excel(movie_list, "douban.xlsx")


if __name__ == "__main__":
    Spider(mainUrl, headers)
