import csv
import requests
from bs4 import BeautifulSoup
import time


def scrape_krisha():
    # Если хотим поменять фильтр
    base_url = 'https://krisha.kz/prodazha/doma/almaty-bostandykskij/'
    page = 1
    data = []

    while True:
        print(page)
        url = base_url + '?page=' + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        ads = soup.find_all('div', class_='a-card__descr')

        if not ads:
            break

        for ad in ads:
            room_count_elem = ad.find('a', class_='a-card__title')
            room_count = room_count_elem.text.split(
                '-')[0].strip() if room_count_elem else 'N/A'

            area_elem = ad.find('a', class_='a-card__title')
            area = area_elem.text.split(',')[1].strip() if area_elem else 'N/A'

            land_area_elem = ad.find('a', class_='a-card__title')
            land_area = ''
            if land_area_elem:
                land_area_parts = land_area_elem.text.split(',')
                if len(land_area_parts) >= 3:
                    land_area = land_area_parts[2].strip().split(' ')[0]

            print(room_count, area)

            price_elem = ad.find('div', class_='a-card__price')
            price = price_elem.text.replace('\xa0', '').split(' ')[
                0] if price_elem else 'N/A'

            subtitle_elem = ad.find('div', class_='a-card__subtitle')
            if subtitle_elem:
                subtitle_text = subtitle_elem.text
                district = subtitle_text.split(',')[0].strip()
                microdistrict = subtitle_text.split(',')[1].strip()
            else:
                district = 'N/A'
                microdistrict = 'N/A'

            description_elem = ad.find('div', class_='a-card__text-preview')
            description = description_elem.text.strip() if description_elem else 'N/A'

            data.append({
                'Room Count': room_count,
                'Area': area,
                'Land Area': land_area,
                'Price': price,
                'District': district,
                'Microdistrict': microdistrict,
                'Description': description
            })

        page += 1

        # Добавляем задержку в 1 секунду между запросами
        time.sleep(1)

    with open('krisha_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print("Данные успешно записаны в файл krisha_data.csv")
    return data


scrape_krisha()
