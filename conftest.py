import pytest
from selenium import webdriver
from pages.key_pages import *


@pytest.fixture(scope='class')
def web_browser():
    driver = webdriver.Chrome('chromedriver112.exe')
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def pre_logout_key(web_browser):
    page = KeyCodeAuthPage(web_browser)
    if page.btn_logout.is_visible():
        page.btn_logout.click()
        page.wait_page_loaded()


@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options
