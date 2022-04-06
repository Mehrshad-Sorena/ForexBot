from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import time


options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

def getData():
    url = 'https://www.forexfactory.com/'

    chromedriver_path = './chromedriver.exe'
    driver = Chrome(options=options, executable_path=chromedriver_path)
    driver.set_window_size(2048, 1024)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')


    driver.refresh()
    time.sleep(5)
    table_src = soup.find('table', {'class': 'calendar__table'})
    tr_list = table_src.find_all('tr')

    result = dict()

    for tr in tr_list:
        timedate = (
                tr.find(
                    'td',
                    {'class': 'calendar__cell calendar__time time'}
                ).text.strip() if tr.find(
                    'td',
                    {'class': 'calendar__cell calendar__time time'}
                ) is not None else '')
        currency = (
                tr.find(
                    'td',
                    {'class': 'calendar__cell calendar__currency currency'}
                ).text.strip() if tr.find(
                    'td',
                    {'class': 'calendar__cell calendar__currency currency'}
                ) is not None else '')
        impact = (
                tr.find(
                    'div',
                    {'class': 'calendar__impact-icon calendar__impact-icon--screen'}
                ).span.get('class')[0] if tr.find(
                    'div',
                    {'class': 'calendar__impact-icon calendar__impact-icon--screen'}
                ) is not None else '')

        result.update(
                {
                    currency: {
                        'time': timedate,
                        'impact': impact,
                    }
                }
        )

    driver.close()
    driver.quit()
    return result

print(getData())