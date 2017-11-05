from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from picture_operation import BeautifulPicture
from multiprocessing import Manager, Pool, cpu_count

def scroll_down(driver, times):
    ''' simulate scrolling down the page
    Args:
        driver (webdriver): selenium's webdriver
        times (int): times to execute the action

    Returns:
        None
    '''
    i = 1
    while i <= times:
        print('scroll down', i, 'times')
        curr_len = len(driver.page_source)
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            if len(driver.page_source) > curr_len:
                break
        i += 1

def click_btn(driver, times, find_btn):
    ''' simulate clicking button
    Args:
        driver (webdriver): selenium's webdriver
        times (int): times to execute the action
        find_btn (function): find the button (driver) -> button

    Returns:
        None
    '''
    i = 1
    while i <= times:
        print('click button', i, 'times')
        curr_len = len(driver.page_source)
        while True:
            btn = find_btn(driver)
            btn.click()
            time.sleep(1)
            if len(driver.page_source) > curr_len:
                break
        i += 1

def get_pexels_pic():
    ''' get pictures from https://www.pexels.com/search/summer/
    '''
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    web_url = 'https://www.pexels.com/search/summer/'
    folder_path = 'd:\pexels_pic'
    driver = webdriver.PhantomJS()
    driver.get(web_url)
    scroll_down(driver, 5)
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
        img_uri = img['src']
        img_name = img_uri.split('/')[-1].split('?')[0]
        input_q.put((img_uri, img_name))
        cnt += 1

    while cnt > 0:
        img_uri, ok = output_q.get()
        if ok:
            cnt -= 1
        else:
            input_q.put(img_uri)
    
    p.close()
    p.terminate()

def get_NASA_pic():
    ''' get pictures from https://www.nasa.gov/multimedia/imagegallery/iotd.html
    '''
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    web_url = 'https://www.nasa.gov/multimedia/imagegallery/iotd.html'
    folder_path = r'd:\NASA_pic'
    prefic_url = 'https://www.nasa.gov'

    driver = webdriver.PhantomJS()
    driver.get(web_url)

    def NASA_find_btn(driver):
        return driver.find_element_by_id('trending')

    click_btn(driver, 5, NASA_find_btn)
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
        img_uri = prefic_url + img['src']
        img_name = img_uri.split('/')[-1]
        input_q.put((img_uri, img_name))
        cnt += 1

    while cnt > 0:
        img_uri, ok = output_q.get()
        if ok:
            cnt -= 1
        else:
            input_q.put(img_uri)
    
    p.close()
    p.terminate()

    
def consumer(input_q, output_q, bp):
    ''' save image
    Args:
        input_q (Queue): to-do queue
        output_q (Queue): job-result queue
        bp (BeautifulPicture): object to handle image save

    Returns:
        None
    '''
    while True:
        img_uri, img_name = input_q.get()
        ok = bp.save_img(img_uri, img_name)
        output_q.put((img_uri, ok))

if __name__ == '__main__':
    start = time.time()
    get_NASA_pic() #https://www.nasa.gov/multimedia/imagegallery/iotd.html
    get_pexels_pic() #https://www.pexels.com/search/summer/
    print(time.time()-start)