import requests
import json
import os
import time
import random
import jieba
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from PIL import Image


filename = "F:\\pythonprogram\\PythonTest\\test1.txt"

def spider_comment(page = 0):
    '''
    爬取指定页面的评价数据
    :param page: 爬取的页数，默认值为0
    :return:
    '''
    # 评论
    url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6134&" \
          "productId=11993134&score=0&sortType=5&page=%d&pageSize=10&isShadowSku=0&fold=1" % page
    kv = {'Referer': 'https://item.jd.com/11993134.html', 'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=kv)   # 添加了请求头参数
        r.raise_for_status()
        # print(r.text[:500])
    except:
        print("爬取失败")
    # 截取json数据字符串
    r_json_str = r.text[26:-2]
    # 字符串转json对象
    r_json_obj = json.loads(r_json_str)
    # 获取评价列表数据
    r_json_comments = r_json_obj['comments']
    # 遍历评论对象列表
    for r_json_comment in r_json_comments:
        # 以追加模式换行写入每条评价
        with open(filename, 'a+', encoding='utf-8') as file:
            file.write(r_json_comment['content'] + '\n')
        # 获取评论对象中的评论内容
        # print(r_json_comment['content'])

def batch_spider_comment():
    '''
    批量爬取数据
    :return:
    '''
    # 写入数据之前先清空之前的数据
    if os.path.exists(filename):
        os.remove(filename)
    for i in range(50):
        spider_comment(i)
        # 模拟用户浏览，设置一个爬虫间隔，防止ip被封
        time.sleep(random.random() * 5)

def cut_word():
    '''
    对数据分词
    :return: 分词后的数据
    '''
    with open(filename, encoding='utf-8') as file:
        test_txt = file.read()
        wordlist = jieba.cut(test_txt, cut_all=True)
        wl = " ".join(wordlist)
        print(wl)
        return wl

def create_word_cloud():
    '''
    生成词云
    :return:
    '''
    # 设置词云的形状
    coloring = np.array(Image.open("picture.png"))
    # 设置词云的一些配置，如：字体，颜色，形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=coloring, scale=4,
                   max_font_size=50, random_state=50, font_path="C:\\Windows\\Fonts\\simhei.ttf")
    # 生成词云
    wc.generate(cut_word())
    # 在只设置mask的情况下，你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()



if __name__ == "__main__":
    # spider_jd()
    # batch_spider_comment()
    # cut_word()
    create_word_cloud()