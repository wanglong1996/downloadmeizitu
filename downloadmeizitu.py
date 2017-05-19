#_*_ coding:utf8 _*_
import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool
img_urls = []

def next_page(page_num):
    for i in range(1,page_num+1):
        url = 'http://www.meizitu.com/a/list_1_{}.html'.format(str(i))
        get_img_url(url)
            
            
def get_img_url(url):
    
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    
    for i in soup.select('.pic > a '):
        #print(i['href'])
        img_urls.append(i['href'])

def downloadimg(url):
    
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    for item in soup.select('#picture > p > img'):
        img = item['src']
        print('正在下载{}'.format(img))
        cont = requests.get(img,stream=True)
        file_name = '{}/img/{}'.format(os.getcwd(),"".join(img.split('/')[-4:]))
        
        if not os.path.exists(file_name):
            with open(file_name,'wb') as f:
                for bloc in cont.iter_content(1024):
                    if bloc:
                        f.write(bloc)
        
 
 
if __name__ == '__main__':
    next_page(15)
    groups = [i for i in img_urls]
    print(len(groups),type(groups[8]))
    pool = Pool()
    pool.map(downloadimg,groups)