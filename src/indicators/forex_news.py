#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json


options = Options()
options.add_argument('--headless')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')


def news():
    url = 'https://www.forexfactory.com/'
    news_path = 'forexnews.json'

    chromedriver_path = './geckodriver.exe'
    driver = Firefox(options=options, executable_path=chromedriver_path)
    #driver.set_window_size(800, 600)

    driver.get(url)
    time.sleep(10)
    driver.refresh()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    try:
        table_src = soup.find('table', {'class': 'calendar__table'})
        tr_list = table_src.find_all('tr')

        result = dict()
        time_holder = ''

        for tr in tr_list:
            timedate = (
                    tr.find(
                        'td',
                        {'class': 'calendar__cell calendar__time time'}
                    ).text.strip() if tr.find(
                        'td',
                     {'class': 'calendar__cell calendar__time time'}
                    ) is not None else '')
            time_holder = (datetime.strptime(timedate, '%I:%M%p') if timedate else time_holder)
            timedate = time_holder

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

            if currency:
                result.update(
                        {
                            currency: {
                                'hour': timedate.hour,
                                'min': timedate.minute,
                                'impact': impact
                            }
                        }
                )

        driver.close()
        driver.quit()

        with open(news_path, 'w') as file:
            file.write(json.dumps(result))

    except Exception as ex:
        print('===== News ===> ',ex)
        driver.close()
        driver.quit()

    return result

def news_task():
    try:
        news()
    except Exception as ex:
        print('===== News ===> ',ex)