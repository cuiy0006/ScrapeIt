from selenium import webdriver
from bs4 import BeautifulSoup
import time
from operate_picture import BeautifulPicture
from multiprocessing import Manager, Pool, cpu_count
from operate_web import scroll_down, click_btn
from worker import consumer, wait_for_complete


def get_163Album_pic():
    ''' get pictures from http://music.163.com/#/artist/album?id=101988&limit=10000&offset=0
    '''
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    web_url = 'http://music.163.com/#/artist/album?id=101988&limit=10000&offset=0'
    folder_path = r'd:\163_BeatlesAlbum_pic'

    print('########## 163 Album mission start! ##########')

    driver = webdriver.PhantomJS()
    driver.get(web_url)

    driver.switch_to.frame('g_iframe')
    m_song_module = driver.find_element_by_id('m-song-module')
    lis = m_song_module.find_elements_by_tag_name('li')

    all_li = BeautifulSoup(driver.page_source, 'lxml').find('ul', {'id':'m-song-module'}).find_all('li')
    bp = BeautifulPicture(headers, folder_path)

    p = Pool(cpu_count())
    m = Manager()
    input_q = m.Queue()
    output_q = m.Queue()

    for i in range(cpu_count()):
        p.apply_async(consumer, (input_q, output_q, bp))

    cnt = 0
    for li in all_li:
        img = li.find('img')
        img_uri = img['src'].split('?')[0]
        album_date = li.find('span', {'class': 's-fc3'}).get_text()
        img_name = album_date + '-' + li.find('p')['title'].replace('/', ' ')
        if len(img_name) > 20:
            img_name = img_name[:20]
        img_name += '.jpeg'
        input_q.put((img_uri, img_name))
        cnt += 1

    ok, fault_cnt = wait_for_complete(input_q, output_q, cnt)

    print('########## 163 Album mission completed:', ok, ' #### fault count:', fault_cnt)
    
    p.close()
    p.terminate()
    driver.quit()