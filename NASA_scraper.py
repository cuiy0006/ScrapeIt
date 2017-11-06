from selenium import webdriver
from bs4 import BeautifulSoup
import time
from picture_operation import BeautifulPicture
from multiprocessing import Manager, Pool, cpu_count
from operate_web import scroll_down, click_btn
from worker import consumer, wait_for_complete


def get_NASA_gallery_pic():
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