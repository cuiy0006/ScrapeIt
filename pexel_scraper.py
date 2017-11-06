from selenium import webdriver
from bs4 import BeautifulSoup
import time
from operate_picture import BeautifulPicture
from multiprocessing import Manager, Pool, cpu_count
from operate_web import scroll_down, click_btn
from worker import consumer, wait_for_complete


def get_pexels_summer_pic():
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