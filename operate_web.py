import time
import aiohttp
import asyncio
import os

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


#why efficiency not promoted
# loop = asyncio.get_event_loop()
# with aiohttp.ClientSession() as session:
#     tasks = create_tasks(jobs, output_q, session)
#     loop.run_until_complete(asyncio.wait(tasks))
# async def save_img(url, name, output_q, session):
#     try:
#         print(os.getpid(),'start')
#         headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
#         async with session.get(url, headers=headers) as response:
#             img = await response.read()
#             with open('D:\pexels_pic' + '\\' + name, 'wb') as f: 
#                 f.write(img)
#         print(os.getpid(),'end')
#         output_q.put((url, True))
#     except:
#         print('*******FAIL******', name, '  ', url)
#         output_q.put((url, True))

# def create_tasks(jobs, output_q, session):
#     tasks = []
#     for img_uri, img_name in jobs:
#         tasks.append(save_img(img_uri, img_name, output_q, session))
#     return tasks


#why it not work
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop, job, output_q)) 
# async def main(loop, jobs, output_q):
#     async with aiohttp.ClientSession(loop=loop) as session:
#         for img_uri, img_name in jobs:
#             #is_ok, user, data = await fetch(session, people, page)
#             ok = await save_img(img_uri, img_name, session)
#             output_q.put((img_uri, ok))

# async def save_img(url, name, session):
#         try:
#             print(os.getpid(), 'start')
#             headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
#             async with session.get(url, headers=headers) as response:
#                 img = await response.read()
#             print(os.getpid(), 'end')
#             return True
#         except Exception as e:
#             print('*******FAIL******', name, '  ', url)
#             return False

            

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
            if len(driver.page_source) != curr_len:
                break
        i += 1



