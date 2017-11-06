import time

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



