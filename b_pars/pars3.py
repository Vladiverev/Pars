from bs4 import BeautifulSoup
import requests
import re
import urllib.request

urllib.request.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")


def get_response(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()

    return response


def get_page_url(url):
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return [item.find('a')['href'] for item in soup.find_all("div", class_='item-info')]


def get_product_image(url, name):
    file_path = 'image/' + name
    urllib.request.urlretrieve(url, file_path)

    return name


def getlistings(base_url, home_url, img=None):
    list_url = get_page_url(base_url)

    response = get_response(home_url + list_url[0])
    soup = BeautifulSoup(response.text, 'html.parser')

    product_params = {}

    for rows in soup.find_all('div', class_='table-row'):

        if 'Размер' in rows.get_text():
            name = soup.find('h1', datatype='card-title').get_text()
            full_size = re.findall(r"\d+[,.]*\d*", rows.find('p').get_text())
            params = {}
            for n, size in enumerate(full_size):
                params['size_' + str(n)] = size

            product_params[name] = params

    if img:
        image_url = soup.find('img', class_='img-product busy')['src']
        image_name = re.findall(r'\w+.jpg', image_url)
        product_params['img'] = get_product_image(image_url, image_name[0])

    return product_params


if __name__ == "__main__":
    home_page = 'https://hotline.ua'
    baseurl = 'https://hotline.ua/sr/?q='
    product = 'Sony PlayStation'

    url = baseurl + product

    product_params = getlistings(url, home_page, img=True)

    print(product_params)
