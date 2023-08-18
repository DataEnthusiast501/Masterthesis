import bs4 as bs
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
from datetime import date, timedelta

link='http://www.kremlin.ru/'

chrome_path = "/Users/test/anaconda3/envs/Masterthesis/lib/python3.8/site-packages/chromedriver_binary/chromedriver"

screen_sizes = [[1366,768], [1920,1080]]


def get_proxy():
    response = requests.get('https://sslproxies.org/')
    soup = BeautifulSoup(response.text, 'lxml')
    tag = 'textarea'
    proxies = soup.find_all(tag)
    proxies = str(proxies).split('\n')
    proxies = [i for i in proxies if ':' in i][1:]
    return proxies


def set_driver(proxies=False):
    chrome_options = webdriver.ChromeOptions()
    if proxies != False:
        if len(proxies) > 0:
            chrome_options.add_argument('--proxy-server={}'.format(proxies[0]))
            proxies.pop(0)
        else:
            proxies = get_proxy()
            chrome_options.add_argument('--proxy-server={}'.format(proxies[0]))
    else:
        proxies = get_proxy()
        chrome_options.add_argument('--proxy-server={}'.format(proxies[0]))
        proxies.pop(0)
    print('proxies added', proxies)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.headless = True
    chrome_options.add_argument("--disable-gpu")

    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-browser-side-navigation")

    driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver.delete_all_cookies()
    screen = random.choice(screen_sizes)
    driver.set_window_size(screen[0], screen[1])
    chrome_options.add_argument("–disable-dev-shm-usage")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")
    # chrome_options.add_argument("referer=" + category_page)
    chrome_options.add_argument('accept-encoding=' + 'gzip, deflate, br')
    chrome_options.add_argument(
        'accept=' + 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    chrome_options.add_argument("upgrade-insecure-requests=" + "1")
    chrome_options.add_argument('cookies=' + 'yes')
    chrome_options.add_argument("timezone=" + "-360")
    chrome_options.add_argument("languages-js=" + "pt-BR,en-US,pt,en")
    chrome_options.add_argument(
        "plugins=" + "Plugin 0: Chrome PDF Plugin; Portable Document Format; internal-pdf-viewer. Plugin 1: Chrome PDF Viewer; ; mhjfbmdgcfjbbpaeojofohoefgiehjai. Plugin 2: Native Client; ; internal-nacl-plugin. ")
    chrome_options.add_argument("screen_depth=" + "24")
    chrome_options.add_argument("screen_left" + "0")
    chrome_options.add_argument("screen_top" + "0")
    chrome_options.add_argument('accept-language' + 'pt-BR,pt;q=0.9,en-US,en;q=0.8')
    connected = False
    while not connected:
        try:
            driver = webdriver.Chrome(chrome_path, options=chrome_options)
            connected = True
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            pass
    return driver, proxies


""" def try_driver(proxies, link):
    connected = False
    try:
        driver, proxies = set_driver(proxies)
        while not connected:
            try:
                driver.get(link)
                connected = True
            except:
                driver, proxies = set_driver(proxies)
    except:
        driver, proxies = set_driver(proxies)
        while not connected:
            try:
                driver.get(link)
                connected = True
            except:
                driver, proxies = set_driver(proxies)

    return driver, proxies """


def try_proxy(driver, proxies, link):
    soup = ''
    page = ''
    get_links_to_articles(driver, link, proxies)
    return driver, soup, proxies, page

def get_links_to_articles(driver, link, proxies):
    driver.get(link)
    links = pd.DataFrame()
    list_of_links = []
    dates_link = 'http://www.kremlin.ru/events/president/news/by-date/'

    start_date = date(2007, 8, 7)
    end_date = date(2009, 8, 7)
    delta = timedelta(days=1)
    driver, proxies = set_driver(proxies)

    while start_date <= end_date:
        try:
            print(start_date.strftime("%d.%m.%Y"))
            date_of_article = str(start_date.strftime("%d.%m.%Y"))
            driver.get(dates_link + date_of_article)
            driver.execute_script("window.stop();")
            page = driver.page_source
            soup = bs.BeautifulSoup(page, 'html.parser')
            link_id = 'data-id'
            for el in soup.find_all("div"):
                if el.has_attr(link_id):
                    list_of_links.append(el.attrs[link_id])

            links = links.append(pd.DataFrame(list_of_links)
                                 )
            links = links.drop_duplicates()
            links.to_csv('list_of_links.csv', index=False)
            start_date += delta

        except:
            driver, proxies = set_driver(proxies)
            date_of_article = str(start_date.strftime("%d.%m.%Y"))
            driver.get(dates_link + date_of_article)
            driver.execute_script("window.stop();")

            page = driver.page_source
            soup = bs.BeautifulSoup(page, 'html.parser')
            link_id = 'data-id'
            for el in soup.find_all("div"):
                if el.has_attr(link_id):
                    print('values:', el.attrs[link_id])
                    list_of_links.append(el.attrs[link_id])
            links = links.append(pd.DataFrame(list_of_links))
            links = links.drop_duplicates()
            links.to_csv('list_of_links.csv', index=False)
            start_date += delta

    return links

proxies = get_proxy()
driver, proxies = set_driver(proxies)

try_proxy(driver, proxies, link)