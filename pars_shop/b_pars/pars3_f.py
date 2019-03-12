from bs4 import BeautifulSoup
import requests
import re
import urllib.request
from fake_useragent import UserAgent


def get_response(url):
    ua = UserAgent().random
    headers = {'User-Agent': ua}
    print(ua)

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()

    return response


def get_page_url(url):
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return [item.find('a')['href'] for item in soup.find_all("div", class_='r')]


def get_product_image(url, name):
    file_path = 'image/' + name
    urllib.request.urlretrieve(url, file_path)

    return name


def getlistings(product_name, img=None):

    product_url = 'https://google.com/search?q=' + product_name + '%20site:f.ua'
    print(product_url)

    list_url = get_page_url(product_url)
    print(list_url)
    if len(list_url) == 0:
       return 'not find product'
    response = get_response(list_url[0])

    soup = BeautifulSoup(response.text, 'html.parser')

    product_params = {}

    for rows in soup.find_all('tr', class_='full gray'):
        if rows.find('td', class_='name') is not None:
            for i in ['Ширина', 'Высота', 'Толщина']:
                if i in rows.find('td', class_='name').get_text():
                    product_params[i] = rows.find('td', class_='value').get_text()

    if img:
        image_url = ''
        for i in soup.find_all('div', class_='img_part_big'):
            image_url = i.find('img')['src']

        image_name = re.findall(r'\w+.jpg', image_url)
        product_params['img'] = get_product_image(image_url, image_name[0])

    return product_params


if __name__ == "__main__":

    product = 'fly+mx330pg*'

    product_params = getlistings(product_name=product, img=True)


    print(product_params)
