import requests
from bs4 import BeautifulSoup


def get_url(page_num: int):
    return f'https://news.ycombinator.com/news?p={page_num}'


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_links():
    url = get_url(1)
    all_a_tags = get_soup(url).find_all('a', 'titlelink')
    all_links = []
    for link in all_a_tags:
        if 'https://' not in link.get('href'):
            all_links.append('https://news.ycombinator.com/' + link.get('href'))
        else:
            all_links.append(link.get('href'))
    return all_links


def get_inner_links(links):
    all_inner_links = []
    for link in links:
        try:
            all_a_tags = get_soup(link).find_all('a')
            inner_links = [inner_link.get('href') for inner_link in all_a_tags if 'https://' in inner_link.get('href')]
            all_inner_links.append(inner_links)
        except:
            pass
    return all_inner_links


def main():
    while True:
        user_input = input('Вывести ссылки на консоль или записать в txt файл? (введите 1 для вывода на консоль, 2 - для записи): ')
        if user_input == '1':
            print('Ссылки на сайты:')
            for link in get_links():
                print(link)
            print('\nВнутренние ссылки с сайтов:')
            for inner_links in get_inner_links(get_links()):
                for inner_link in inner_links:
                    print(inner_link)
            break
        elif user_input == '2':
            file_name = input('Введите название для файла: ')
            with open(f'{file_name}.txt', 'w', encoding='utf-8') as file:
                file.write('Ссылки на сайты: \n')
                for link in get_links():
                    file.write(link + '\n')
                file.write('\nВнутренние ссылки с сайтов:\n')
                for inner_links in get_inner_links(get_links()):
                    for inner_link in inner_links:
                        file.write(inner_link + '\n')
            break
        else:
            print('Выберите либо 1, либо 2!')


if __name__ == '__main__':
    main()
