import threading
import pandas as pd  # type: ignore
import requests
import re
from bs4 import BeautifulSoup  # type: ignore

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
}
url = "https://movie.douban.com/top250/"


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
        self.introduction=introduction
        self.url = url
        self.INDb = INDb


# 获取每一页的url
def Get_page_url(page_num, url, header, page_url_list=[]):
    res = requests.get(url=url + "?start=" + (str((page_num - 1) * 25)), headers=header)
    context = res.text
    pattern = "<li>(.*?)</li>"
    res = re.findall(pattern, context, re.S)
    pattern = '<a href="(.*?)/">'
    for i in range(0, 25):
        url = re.findall(pattern, res[i], re.S)
        page_url_list.append(url[0])


def if_null(data):
    if data:
        return data[0]
    else:
        return ""


def Get_movie_info(url, header, movie_list=[]):
    print("downloading:", url)
    res = requests.get(url=url, headers=header)
    context = res.text
    # print(context)
    soup = BeautifulSoup(context, "html.parser")
    title = soup.find("span", property="v:itemreviewed").get_text()
    introduction = soup.find("span", property="v:summary").get_text().strip()
    # print(introduction)
    info = soup.find("div", id="info").get_text()
    director = if_null(re.findall("导演: (.*?)\n", info, re.S))
    screenwriter = if_null(re.findall("编剧: (.*?)\n", info, re.S))
    region = if_null(re.findall("制片国家/地区: (.*?)\n", info, re.S))
    language = if_null(re.findall("语言: (.*?)\n", info, re.S))
    release_time = if_null(re.findall("上映日期: (.*?)\n", info, re.S))
    length = if_null(re.findall("片长: (.*?)\n", info, re.S))
    other_name = if_null(re.findall("又名: (.*?)\n", info, re.S))
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
        url,
        INDb,
    )
    movie_list = movie_list.append(mv)


def add_to_excel(data):
    # 显示所有列
    pd.set_option("display.max_columns", None)
    # 显示所有行
    pd.set_option("display.max_rows", None)
    # 设置value的显示长度为100，默认为50
    pd.set_option("max_colwidth", 100)
    variables = list(data[0].__dict__.keys())
    
    df = pd.DataFrame(
        [[getattr(i, j) for j in variables] for i in data], columns=variables
    )

    
    df.to_excel("douban.xlsx", index=False)


def get_movie_info_in_thread(url_list, header, movie_list):
    for url in url_list:
        Get_movie_info(url, header, movie_list)


# 爬虫函数
def Spider(url, header):
    print("downloading:", url)
    page_url_list = []
    # 获取前10页的url
    for i in range(1, 11):
        Get_page_url(i, url, header, page_url_list)
    # 电影列表
    movie_list = []
    # 线程列表
    threads = []
    # Get_movie_info(page_url_list[18], header, movie_list)

    # return
    url_parts = [page_url_list[i : i + 10] for i in range(0, len(page_url_list), 10)]
    for i in url_parts:
        t = threading.Thread(
            target=get_movie_info_in_thread, args=(i, header, movie_list)
        )
        # 启动线程
        t.start()
        # 添加线程到线程列表
        threads.append(t)

    # 等待所有线程结束
    for t in threads:
        t.join()

    # 将movie_list的url按照page_url_list的顺序排序
    movie_list = sorted(movie_list, key=lambda x: page_url_list.index(x.url))
    add_to_excel(movie_list)


if __name__ == "__main__":
    Spider(url, headers)
