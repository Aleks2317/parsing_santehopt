import csv
import requests
from bs4 import BeautifulSoup
import fake_useragent

def parsing_go():
    ua = fake_useragent.UserAgent()
    url = 'https://santehshop.by/catalog/vanny/'
    shema = 'https://santehshop.by'


    count = 0
    cout_card = 0
    col = 0
    cound_k = 0


    # функция для извлечения данных
    def request_soup(url, ua):
        """
        извлечение данных при помощи requests и BeautifulSoup
        :param url: url
        :param ua: UserAgent
        :return: объект BeautifulSoup
        """
        fake_ua = {'user-agent': ua.random}
        respons = requests.get(url=url, headers=fake_ua)
        if respons.status_code != 200:
            print(f"Страница {url} не найдена - выходим")
            exit(0)
        respons.encoding = 'utf-8'
        return BeautifulSoup(respons.text, 'lxml')


    # # создадим файл 1 с нужными категориями
    with open('santehshop_category.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'id', 'Ссылка', 'Наименование',
        ])


    # создадим файл 2 с нужными категориями
    with open('santehshop_goods.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Категория', 'Ссылка на категорию', 'Наименование',
            'Артикул', 'Материал', 'Наличие', 'Цена', 'Старая цена',
            'Ссылка на карточку с товаром', 'Страна производитель',
            'Производитель', 'Импортер в РБ', 'Гарантия', 'Код товара'
        ])


    # проход по разделам
    soup = request_soup(url, ua)

    section_compact_list = soup.find('div', class_="row margin0 flexbox").find_all('a', class_="thumb shine")
    sektions_link = [f"{shema}{i['href']}" for i in section_compact_list]

    sektions_name = [i.text for i in soup.find('div', class_="row margin0 flexbox").find_all('a', class_='section-compact-list__link dark_link option-font-bold')]

    id_sections = [id_['id'] for id_ in soup.find_all('div', class_="section-compact-list__item item bordered box-shadow flexbox flexbox--row")]

    for sektion, sektion_link, id_section in zip(sektions_name, sektions_link, id_sections):

        count += 1

        print(f"[+] {count}  - {id_section} - {sektion} --- {sektion_link}")

        sektion_ = sektion  # 'Категория'
        sektion_link_ = sektion_link  # 'Ссылка на категорию'

        # файл 1 с нужными категориями
        with open('santehshop_category.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([
                id_section, sektion_link_, sektion_
            ])

        pages = []

        soup_sektion = request_soup(sektion_link, ua)
        count_ = 0

        # проверяем наличие страниц и собераем их
        try:

            shema_p = soup_sektion.find('div', class_="module-pagination").find_all('a')[-1]['href'][:-1]
            next_page = int(soup_sektion.find('div', class_="module-pagination").find_all('a')[-1].text)
            pages = [f"{shema}{shema_p}{l}" for l in range(1, next_page + 1)]
            print('True', pages)

        except:
            pages.append(sektion_link)
            print('PASS', pages)

        #  проход по страницам
        for p in pages:
            cout_card += 1

            soup_page = request_soup(p, ua)

            # ссылки на карточки

            card = [f"{shema}{i['href']}" for i in soup_page.find_all('a', class_="thumb")]
            col += len(card)
            print(f'Раздел - {count} \nСтраница раздела - {cout_card} \nКолличество карточек - {col} \nКарточек на странице - {len(card)}')
            print('* ' * 20)
            print()



            # cбор данных с карточки товара
            for card_link in card:

                soup_card_link = request_soup(card_link, ua)

                link = card_link  # Ссылка на карточку

                name = soup_card_link.find('h1', id='pagetitle').text.strip()  # наименование
                try:
                    value_ = soup_card_link.find('div', class_='view_sale_block v2 grey').text.strip().split()[-2]  # наличие
                except:
                    value_ = 'No'
                try:
                    price = soup_card_link.find('div', class_='price font-bold font_mxs').find('span', class_='price_value').text  # цена
                except:
                    price = 'No price'

                try:
                    old_price = soup_card_link.find('div', class_='price discount').find('span', class_='price_value').text  # старая цена
                except:
                    old_price = 'No'


                characteristics = {}

                try:
                    name_wrap = [i.text.strip(',""\n') for i in soup_card_link.find_all('div', class_='properties-group__name-wrap')]
                    value_wrap = [j.text.strip() for j in soup_card_link.find_all('div', class_='properties-group__value-wrap')]
                    #ordered_block = {}
                    for k, v in zip(name_wrap, value_wrap):
                        characteristics[k] = v
                except:
                    characteristics = "No ordered_block"

                try:
                    article = characteristics['Артикул']
                except:
                    article = 'No'

                try:
                    country_of_origin = characteristics['Страна производства ']
                except:
                    country_of_origin = '-'

                try:
                    material = characteristics['Материал']
                except:
                    material = 'No information'

                try:
                    manufacturer = characteristics['Производитель']
                except:
                    manufacturer = 'No information'

                try:
                    importer = characteristics['Импортер в РБ']
                except:
                    importer = 'No information'

                try:
                    guranti = characteristics['Гарантия']
                except:
                    guranti = 'No information'

                try:
                    cod = characteristics['Код товара']
                except:
                    cod = 'No information'
                cound_k += 1
                print(f'Карточек пройдено - {cound_k}, осталось - {col - cound_k}')

                # запись
                # файл 2 с нужными категориями
                with open('santehshop_goods.csv', 'a', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([
                        sektion_, sektion_link_, name, article, material, value_,
                        price, old_price, link, country_of_origin, manufacturer,
                        importer, guranti, cod
                    ]
                    )

    # file.close()




    print('Программа завершена')