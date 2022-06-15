# ------------------------------------
# парсинг данных с сайта www.sulpak.kg
# ------------------------------------
from bs4 import BeautifulSoup
import requests
import csv

CSV = 'sulpak_parsing.csv'
URL = 'https://www.sulpak.kg/f/noutbuki'
HOST = 'https://www.sulpak.kg'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.127 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 '
}


def get_html(url, headers, **params):
    response = requests.get(url, headers=headers, params=params, verify=False)
    return response


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    goods = soup.findAll('div', class_='goods-tiles')
    list_data = []
    for good in goods:
        list_data.append({
            'Наименование товара': good.find('h3', class_='title').get_text(
                strip=True),
            'Ссылка на страницу с товаром': HOST + good.find('a').get('href'),
            'Цена товара': good.find('div', class_='price').get_text(
                strip=True),
        })
    return list_data


def save(goods, csv_):
    with open(csv_, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование товара', 'Ссылка на страницу с товаром', 'Цена товара'])
        for good in goods:
            writer.writerow([good['Наименование товара'], good['Ссылка на страницу с товаром'], good['Цена товара']])


def parse():
    pages = int(input('Введите кол-во страниц: '))
    results_list = []
    for page in range(1, pages + 1):
        print(f'Страница {page} готова!')
        html = get_html(URL, HEADERS, params={'page': page})
        results_list.extend(get_data(html.text))
    save(results_list, CSV)
    print('Данные успешно сохранены')


if __name__ == '__main__':
    parse()


