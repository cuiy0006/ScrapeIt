import requests
from bs4 import BeautifulSoup
from picture_operation import BeautifulPicture

if __name__ == '__main__':
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    web_url='https://pixabay.com/en/'

    bp = BeautifulPicture(headers, 'd:\scrape_requests')
    r=requests.get(web_url, headers=headers)

    all_div=BeautifulSoup(r.text, 'lxml').find_all('div', class_='item') #Avoid conflict with 'class' keyword

    for div in all_div:
        img = div.find('img')
        src = img['src']
        if src == '/static/img/blank.gif':
            src =img['data-lazy'] 
        name = src.split('/')[-1]
        bp.save_img(src, name)
        #print(src)


