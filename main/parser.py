import threading
import requests
import bs4
import zlib
import sqlite3
import hashlib
import random
from .models import Products
import shutil, os

class Pars_Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Initialized thread" + str(self))

    def run(self):
        def find_max_page(h):
            html = requests.get(h.replace('%', str(1))).text
            soup = bs4.BeautifulSoup(html, 'lxml')
            strani = soup.find_all('a', class_='pagination-item')
            maximum_lst = []
            for i in strani:
                maximum_lst.append(int(i.text))
            maxs_ = max(maximum_lst)
            return maxs_

        base_url = 'https://www.wildberries.ru'
        hresf = ['https://www.wildberries.ru/catalog/elektronika/avtoelektronika?page=%']
        for h in hresf:
            maxs_ = find_max_page(h)
            print(maxs_)
            for num in range(1, maxs_ + 1):
                html = requests.get(h.replace('%', str(num))).text
                soup = bs4.BeautifulSoup(html, 'lxml')
                print(f'{h} , num={num}')
                prod_s = [item.get('href') for item in
                          soup.find_all('a', class_='ref_goods_n_p j-open-full-product-card')]
                results = []
                for prod in prod_s:
                    one_item = {}
                    one_item['href'] = base_url + prod
                    inner_html = requests.get(base_url + prod).text
                    inner_soup = bs4.BeautifulSoup(inner_html, 'lxml')
                    one_item['name'] = inner_soup.find('span', class_='name').text.replace(u'\xa0', ' ').replace(
                        u'\u2009', '').lstrip()
                    one_item['price'] = inner_soup.find('span', class_='final-cost').text.replace(u'\xa0',
                                                                                                  ' ').replace(
                        u'\u2009', '').replace('\n', '').replace(' ', '')
                    one_item['img'] = 'https:' + inner_soup.find('img', class_='MagicZoomFullSizeImage').get(
                        'src').replace('big', 'c252x336')
                    results.append(one_item)

                    Products(**one_item, hash=hashlib.md5(one_item['href'].encode()).hexdigest(),
                             stock_balance=random.randint(1, 100)).save()

                    hashed = hashlib.md5(one_item['href'].encode()).hexdigest()
                    r = requests.get(one_item['img'], stream=True)
                    path= os.path.join(os.getcwd(),'main','static','main','imgs', hashed +'.jpeg')
                    if r.status_code == 200:
                        with open(path, 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                print(f'srt-{num} len-{len(results)}, i allive')