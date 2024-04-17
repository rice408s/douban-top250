import re
import requests
from utools import Get_movie_url_list, headers
from bs4 import BeautifulSoup  # type: ignore


class Comment:
    def __init__(
        self,
        title,
        movie_id,
        username,
        user_id,
        comment_time,
        comment,
        rate,
    ):
        self.title = title
        self.username = username
        self.movie_id = movie_id
        self.user_id = user_id
        self.comment_time = comment_time
        self.comment = comment
        self.rate = rate

    def __str__(self):
        return (
            "title: "
            + self.title
            + "\n"
            + "movie_id: "
            + self.movie_id
            + "\n"
            + "username: "
            + self.username
            + "\n"
            + "user_id: "
            + self.user_id
            + "\n"
            + "comment_time: "
            + self.comment_time
            + "\n"
            + "comment: "
            + self.comment
            + "\n"
            + "rate: "
            + self.rate
            + "\n"
        )


# 数据处理函数
def data_is_null(data):
    if data:
        return data[0]
    else:
        return ""


def Get_comment_info(url, header, page_num, id,comment_list=[]):
    # print("downloading:", url, "......\n")
    res = requests.get(url=url, headers=header)
    context = res.text
    pattern='<span property="v:itemreviewed">(.*?)</span>'
    title=re.findall(pattern, context, re.S)[0]
    movie_id=id
    url = url + "/reviews?start=" + str(page_num)
    res = requests.get(url=url, headers=header)
    context = res.text
    soup = BeautifulSoup(context, "html.parser")
    comments = soup.findAll("div", class_="main review-item")
    # for comment in comments:
    print(comments[0])
    pattern='''<a class="avator" href="https://www.douban.com/people/bighead/">
<img height="24" src="(.*?)" width="24"/>
</a>'''
    re.findall(pattern, str(comments[0]), re.S)

def Spider():
    # url_list = Get_movie_url_list()
    u1 = "https://movie.douban.com/subject/1292052"
    # 先获取单部电影的评论
    comment_list = []
    # for i in range(1, 11):
    #     Get_comment_info(u1, headers, (i - 1) * 20, comment_list)
    Get_comment_info(u1, headers, 0,2,comment_list)


if __name__ == "__main__":
    Spider()
