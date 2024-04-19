# 获取每一页的url
import re
import requests
import pandas as pd  # type: ignore

mainUrl = "https://movie.douban.com/top250/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
}


# 获取每一页的url
def Get_urls_by_page(page_num, url, header, page_url_list=[]):
    res = requests.get(url=url + "?start=" + (str((page_num - 1) * 25)), headers=header)
    context = res.text
    # print(context)
    pattern = "<li>(.*?)</li>"
    res = re.findall(pattern, context, re.S)

    pattern = '<a href="(.*?)/">'
    print(len(res))
    for i in range(0, len(res)):
        url = re.findall(pattern, res[i], re.S)
        page_url_list.append(url[0])


def Get_movie_url_list():
    url_list = []
    # 获取前10页的url
    for i in range(1, 11):
        Get_urls_by_page(i, mainUrl, headers, url_list)
    return url_list


def Add_to_excel(data, name):
    # 显示所有列
    pd.set_option("display.max_columns", None)
    # 显示所有行
    pd.set_option("display.max_rows", None)
    # 设置value的显示长度为100，默认为50
    pd.set_option("max_colwidth", 100)
    print(data[0])
    variables = list(data[0].__dict__.keys())
    df = pd.DataFrame(
        [[getattr(i, j) for j in variables] for i in data], columns=variables
    )

    df.to_excel(name, index=False)



