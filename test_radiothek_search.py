import time

import pytest as pytest
from selenium.webdriver import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def chrome_driver():
    # setup web Browser
    settings = webdriver.ChromeOptions()
    settings.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=settings)

    # open radiothek webpage
    url = "https://radiothek.orf.at/search"
    driver.get(url)

    # search accept cookie button
    expectation = EC.presence_of_element_located((By.CSS_SELECTOR, '#didomi-notice-agree-button'))

    # click button if appear
    accept_button = WebDriverWait(driver, 5).until(expectation)
    time.sleep(1)
    accept_button.click()
    time.sleep(1)

    # return browser setup
    yield driver

    # close driver at the end of test
    driver.quit()


def test1_basic_search(chrome_driver):
    search_element = chrome_driver.find_element(By.CSS_SELECTOR, "input[type=search]")
    search_text = "Nachmittag"
    search_element.send_keys(search_text)

    submit = chrome_driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit.click()

    #result_is_present = EC.presence_of_element_located((By.CSS_SELECTOR, "class[results-title]"))
    result_is_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".search-has-query h2"))

    # Try all 500 milliseconds if expectation is fulfilled, timeout after 10 seconds
    result_header_element = WebDriverWait(chrome_driver, 5).until(result_is_present)
    # print(result_header_element.text)
    assert result_header_element.text == f'Suchergebnis für "{search_text}"'



def test2_search_collect(chrome_driver):
    #Enter search text
    search_element = chrome_driver.find_element(By.CSS_SELECTOR, "input[type=search]")
    search_text = "Nachmittag"
    search_element.send_keys(Keys.CONTROL, 'a')  # it navigates to the begin of the search field
    search_element.send_keys(search_text)
    submit = chrome_driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit.click()

    #Wait for search result
    result_is_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".search-has-query h2"))
    # Try all 500 milliseconds if expectation is fulfilled, timeout after 5 seconds
    WebDriverWait(chrome_driver, 5).until(result_is_present)

    #add search result to a list
    result_list = chrome_driver.find_elements(By.CSS_SELECTOR, 'span.type')

    #analyze result and put it in a dictionary
    result_dict = {}
    for x in result_list:
        name = x.text
        if name in result_dict.keys():
            result_dict[name] += 1
        else:
            result_dict.update({name: 1})

    print("\n\nwhat did you find?:")
    print(result_dict)

    assert len(result_dict.keys()) > 1


def test3_search_with_options(chrome_driver):
    # Enter search text
    search_element = chrome_driver.find_element(By.CSS_SELECTOR, "input[type=search]")

    search_text = "Jazz"
    search_element.click()
    #search_element.clear()
    search_element.send_keys(Keys.CONTROL, 'a')   #it navigates to the begin of the search field
    search_element.send_keys(search_text)
    submit = chrome_driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit.click()

    # select senders in combo box
    sender = chrome_driver.find_element(By.CSS_SELECTOR, "div[title='Nach Sendern filtern']")
    sender.click()

    oe1 = chrome_driver.find_element(By.XPATH, "//li[contains(@id, 'results-oe1')]")
    # oe1.location_once_scrolled_into_view
    chrome_driver.execute_script("arguments[0].click();", oe1)

    sender.click()
    wie = chrome_driver.find_element(By.XPATH, "//li[contains(@id, 'results-wie')]")
    # wie.location_once_scrolled_into_view  #does not work!!

    # wie_present=EC.presence_of_element_located((By.XPATH, "//li[contains(@id, 'results-wie')]"))
    # WebDriverWait(chrome_driver, 5).until().click()
    chrome_driver.execute_script("arguments[0].click();",
                                 wie)  # unknown reason why this works. This is an Idee from stackowerflow.

    chrome_driver.refresh()
    # Wait for search result
    result_is_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".search-has-query h2"))
    # Try all 500 milliseconds if expectation is fulfilled, timeout after 5 seconds
    WebDriverWait(chrome_driver, 5).until(result_is_present)

    # add search result to a list
    result_list = chrome_driver.find_elements(By.CSS_SELECTOR, "span.type")
    result_dict = {}
    for x in result_list:
        name = x.text
        if name in result_dict.keys():
            result_dict[name] += 1
        else:
            result_dict.update({name: 1})

    print("\n\nwhat did you find?:")
    print(result_dict)

    assert 'Ö1' in result_dict.keys()
    assert 'Radio Wien' in result_dict.keys()
