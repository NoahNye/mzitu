import os
import random
import time

import requests

from bs4 import BeautifulSoup


class Mztu:

    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

    def all_url(self, url):
        html = self.request(url)
        print(html.text)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        print(all_a)
        for a in all_a:
            title = a.get_text()
            print('开始保存：', title)
            path = str(title).replace("?", "_")
            self.mkdir(path)
            href = a['href']
            self.html(href)

    def request(self, url):
        req = requests.get(url, headers=self.headers)
        return req

    def html(self, href):
        html = self.request(href)
        self.headers['referer'] = href
        page = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi')
        if page is not None:
            max_span = page.find_all('span')[-2].get_text()
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                print('page_url', page_url)
                self.img(page_url)

    def img(self, page_url):
        ###随机时间间隔调用
        time.sleep(random.randint(0, 3))
        img_html = self.request(page_url)
        img_url = None
        try:
            img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        except:
            print('dom解析失败', BeautifulSoup(img_html.text, 'lxml').prettify())
        if img_url is not None:
            self.save(img_url)

    def save(self, img_url):
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):
        path = path.strip()
        exists = os.path.exists(os.path.join("/mztu/download", path))
        if not exists:
            os.makedirs(os.path.join("/mztu/download", path))
            os.chdir(os.path.join("/mztu/download", path))
            return True
        else:
            return False


mztu = Mztu()
mztu.all_url("https://www.mzitu.com/all")
