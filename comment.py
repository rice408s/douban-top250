import re
import threading
import requests
from utools import Add_to_excel, Get_movie_url_list, headers
from bs4 import BeautifulSoup  # type: ignore


class Comment:
    def __init__(
        self,
        movie,
        movie_id,
        user_id,
        comment_time,
        comment,
        rate,
    ):
        self.movie = movie
        self.movie_id = movie_id
        self.user_id = user_id
        self.comment_time = comment_time
        self.comment = comment
        self.rate = rate


# 数据处理函数
def data_is_null(data):
    if data:
        return data[0].get_text()
    else:
        return ""


def Get_comment_info(url, header, page_num, id, comment_list=[]):
    url = url + "/comments?start=" + str(page_num) + "&limit=20"
    # print(url)
    res = requests.get(url=url, headers=header)
    context = res.text
    # print(context)
    soup = BeautifulSoup(context, "html.parser")
    # print(soup)
    movie = data_is_null(soup.find_all("title")).split(" ")[0].strip()
    # print(movie)
    comments = soup.find_all("div", class_="comment-item")
    for x in comments:
        # print(x)
        uid = x.find("img", class_="").get("src").split("/")[-1].split("-")[0][1:]
        content = x.find("span", class_="short").get_text().strip()
        # print(uid)
        # print(content)
        pattern = '<span class="allstar(.*?) rating"'
        if re.findall(pattern, str(x), re.S):
            rate = int(re.findall(pattern, str(x), re.S)[0]) / 10
        else:
            rate = 0
        # print(rate)
        comment_time = x.find("span", class_="comment-time").get_text().strip()
        # print(comment_time)
        C = Comment(movie, id, uid, comment_time, content, rate)
        comment_list.append(C)


def Get_comment_info_in_thread(url, headers, id, comment_list=[]):
    print("downloading:", url, "......\n")
    for i in range(1, 11):
        Get_comment_info(url, headers, (i - 1) * 20, id, comment_list)


def Spider():
    url_list = Get_movie_url_list()
    
    comment_list = []
    Thread_list = []
    for i in range(0, len(url_list)):
        t = threading.Thread(
            target=Get_comment_info_in_thread,
            args=(url_list[i], headers, i + 2, comment_list),
        )

        t.start()
        Thread_list.append(t)
        
    for t in Thread_list:
        t.join()
        
    comment_list.sort(key=lambda x: x.movie_id)
    Add_to_excel(comment_list, "comment.xlsx")
    

if __name__ == "__main__":
    Spider()
