import time

import pytest as pytest

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
    time.sleep(5)

    # return browser setup
    yield driver

    # close driver at the end of test
    driver.quit()


"""

def test_basic_search(chrome_driver):
    search_element = chrome_driver.find_element(By.CSS_SELECTOR, "input[type=search]")
    search_text = "Jazz"
    search_element.send_keys(search_text)

    submit = chrome_driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit.click()

    #result_is_present = EC.presence_of_element_located((By.CSS_SELECTOR, "class[results-title]"))
    result_is_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".search-has-query h2"))

    # Try all 500 milliseconds if expectation is fulfilled, timeout after 10 seconds
    result_header_element = WebDriverWait(chrome_driver, 5).until(result_is_present)
    # print(result_header_element.text)
    assert result_header_element.text == f'Suchergebnis für "{search_text}"'
    time.sleep(5)



def test_search_collect(chrome_driver):
    #Enter search text
    search_element = chrome_driver.find_element(By.CSS_SELECTOR, "input[type=search]")
    search_text = "Nachmittag"
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
        count = 0
        for y in result_list:       #count the occurrence of this element in the list
            if name.upper() == y.text.upper():
                count += 1
        result_dict.update({name: count})  # dictionary do not allow duplicates, that is why no additional check

    print("\n\nwhat did you find?:")
    print(result_dict)

    assert len(result_dict.keys()) > 1
"""

def test_search_with_options(chrome_driver):
    #Enter search text
    search_element = chrome_driver.find_element(By.CSS_SELECTOR, "input[type=search]")
    search_text = "Nachmittag"
    search_element.send_keys(search_text)
    submit = chrome_driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    submit.click()

    #select senders in combo box
    select = Select(chrome_driver.find_element(By.CSS_SELECTOR, ""))

    select.select_by_value("oe3")  # select Ö3
    select.select_by_value("fm4")

    result_list = chrome_driver.find_elements(By.CSS_SELECTOR, 'span.type')
    result_dict = {}
    for x in result_list:
        name = x.text
        count = 0
        for y in result_list:  # count the occurrence of this element in the list
            if name.upper() == y.text.upper():
                count += 1
        result_dict.update({name: count})  # dictionary do not allow duplicates, that is why no additional check

    print("\n\nwhat did you find?:")
    print(result_dict)

    assert len(result_dict.keys()) > 1