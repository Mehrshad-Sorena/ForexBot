from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup


class ForexNews:
    def __init__(self):
        self._url = 'https://www.forexfactory.com/'

        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        self.driver = Chrome(options=options)
        self.driver.set_window_size(2048, 1024)

        self.driver.get(self._url)
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')

    def getData(self):
        table_src = self.soup.find('table', {'class': 'calendar__table'})
        tr_list = table_src.find_all('tr')

        result = dict()

        for tr in tr_list:
            time = (
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
                            'time': time,
                            'impact': impact,
                        }
                    }
            )

        return result
