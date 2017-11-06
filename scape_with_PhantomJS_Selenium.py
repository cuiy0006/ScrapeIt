from selenium import webdriver
from bs4 import BeautifulSoup
import time
from picture_operation import BeautifulPicture
from multiprocessing import Manager, Pool, cpu_count
from operate_web import scroll_down, click_btn
from worker import consumer, wait_for_complete


def get_pexels_pic():
    ''' get pictures from https://www.pexels.com/search/summer/
    '''
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    web_url = 'https://www.pexels.com/search/summer/'
    folder_path = 'd:\pexels_pic'
    scroll_for_more = 5

    print('########## pexel mission start! ##########')

    driver = webdriver.PhantomJS()
    driver.get(web_url)
    scroll_down(driver, scroll_for_more)
    all_img = BeautifulSoup(driver.page_source, 'lxml',).find_all('img', class_="photo-item__img")
    bp = BeautifulPicture(headers, folder_path)

    p = Pool(cpu_count())
    m = Manager()
    input_q = m.Queue()
    output_q = m.Queue()

    for i in range(cpu_count()):
        p.apply_async(consumer, (input_q, output_q, bp))

    cnt = 0
    for img in all_img:
        img_uri = img['src'].split('?')[0]
        img_name = img_uri.split('/')[-1]
        input_q.put((img_uri, img_name))
        cnt += 1

    ok, fault_cnt = wait_for_complete(input_q, output_q, cnt)

    print('########## pexels mission completed:', ok, ' #### fault count:', fault_cnt)
    
    p.close()
    p.terminate()
    driver.quit()

def get_NASA_pic():
    ''' get pictures from https://www.nasa.gov/multimedia/imagegallery/iotd.html
    '''
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    web_url = 'https://www.nasa.gov/multimedia/imagegallery/iotd.html'
    folder_path = r'd:\NASA_pic'
    prefic_url = 'https://www.nasa.gov'
    click_for_more = 5

    print('########## NASA mission start! ##########')
    driver = webdriver.PhantomJS()
    driver.get(web_url)

    def NASA_find_btn(driver):
        return driver.find_element_by_id('trending')

    click_btn(driver, click_for_more, NASA_find_btn)
    all_div = BeautifulSoup(driver.page_source, 'lxml',).find_all('div', class_="image")
    bp = BeautifulPicture(headers, folder_path)

    p = Pool(cpu_count())
    m = Manager()
    input_q = m.Queue()
    output_q = m.Queue()

    for i in range(cpu_count()):
        p.apply_async(consumer, (input_q, output_q, bp))

    cnt = 0
    for div in all_div:
        img = div.find('img')
        img_src = img['src']
        img_src_lst = img_src.split('/')
        img_src_lst[5] = 'full_width_feature'
        img_uri = prefic_url + '/' + '/'.join(img_src_lst)
        img_name = img_uri.split('/')[-1]
        input_q.put((img_uri, img_name))
        cnt += 1

    ok, fault_cnt = wait_for_complete(input_q, output_q, cnt)

    print('########## NASA mission completed:', ok, ' #### fault count:', fault_cnt)
    
    p.close()
    p.terminate()
    driver.quit()
    
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


if __name__ == '__main__':
    start = time.time()
    get_NASA_pic() #https://www.nasa.gov/multimedia/imagegallery/iotd.html
    get_pexels_pic() #https://www.pexels.com/search/summer/
    get_163Album_pic() #http://music.163.com/#/artist/album?id=101988&limit=10000&offset=0
    print(time.time()-start)