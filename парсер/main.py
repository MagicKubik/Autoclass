import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv
import os

user = fake_useragent.UserAgent().random

header = {
    'User-Agent': user
}

'https://www.drom.ru/pdd/bilet_1/'
'https://www.drom.ru/pdd/bilet_40/'

# рпвельный ответ находится в <div id="a1">


def pdd():
    image_num = 1

    with open('test.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
        for num in range(1, 41):
            print(num)
            link = f'https://www.drom.ru/pdd/bilet_{num}/'
            res_test = requests.get(link, headers=header).text
            soup_test = BeautifulSoup(res_test, 'lxml')
            block_test = soup_test.find_all(class_='pdd-ticket b-media-cont')
            for test in block_test:
                quest = str()
                solution = []
                correct_solution = str()
                commentary = str()

                # картинка
                # Директория, в которую сохраняются изображения
                image_dir = 'picture'
                if not os.path.exists(image_dir):
                    os.makedirs(image_dir)
                test_image = test.find(class_='b-media-cont').find('img')
                if test_image is not None:
                    test_image_url = test.find(class_='b-media-cont').find('img').get('src')
                    image_bytes = requests.get(test_image_url, headers=header, stream=True)
                    image_path = os.path.join(image_dir, f'{image_num}.png')
                    with open(image_path, 'wb') as f:
                        for chunk in image_bytes.iter_content(chunk_size=1024):
                            f.write(chunk)
                image_num += 1

                # вопрос
                test_quest = test.find(class_="b-title b-title_type_h4 b-title_no-margin").text
                quest = str(test_quest).strip()

                # коментарий
                test_commentary = test.find(class_='b-media-cont b-media-cont_margin_huge').text
                for i in test_commentary.split(f'\n\n')[1:]:
                    commentary = str(i).strip()

                test_solution = test.find(
                    class_='b-media-cont b-media-cont_margin_huge b-random-group b-random-group_margin_b-size-s').find_all(
                    class_='b-flex b-flex_align_left b-random-group b-random-group_margin_r-size-s bm-forceFlex')

                # ответы
                for solutions in test_solution:
                    all_solution = solutions.contents[2:]
                    for variant in all_solution:
                        if 'id' in str(variant):
                            # правельный ответ
                            correct_solution = str(variant.text).strip()
                        # все ответы
                        solution.append(str(variant.text).strip())

                # Запись в CSV
                filtered_solution = [res for res in solution if res.strip()]
                resolution_str = ', '.join([f"'{res}'" for res in filtered_solution])
                writer.writerow([quest, resolution_str, correct_solution, commentary])


pdd()

# pyinstaller
# 'pyinstaller --onefile --collect-all fake_useragent main.py'

