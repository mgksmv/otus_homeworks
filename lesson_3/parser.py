import requests
from bs4 import BeautifulSoup


class YcombinatorParser:
    def __init__(self, page: int):
        self.url = f'https://news.ycombinator.com/news?p={page}'

    def get_soup(self):
        response = requests.get(self.url, timeout=1)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def get_links(self):
        all_a_tags = self.get_soup().find_all('a', 'titlelink')
        all_links = []
        for link in all_a_tags:
            if 'https://' not in link.get('href'):
                all_links.append('https://news.ycombinator.com/' + link.get('href'))
            else:
                all_links.append(link.get('href'))
        return all_links

    def get_inner_links(self, links):
        all_inner_links = []
        for link in links:
            try:
                all_a_tags = self.get_soup().find_all('a')
                inner_links = [inner_link.get('href') for inner_link in all_a_tags if inner_link.get('href') and 'https://' in inner_link.get('href')]
                all_inner_links.append(inner_links)
            except Exception as e:
                print(e)
        return all_inner_links


def main():
    parser = YcombinatorParser(1)
    while True:
        user_input = input(
            'Вывести ссылки на консоль или записать в txt файл? (введите 1 для вывода на консоль, 2 - для записи): '
        )
        if user_input == '1':
            print('Ссылки на сайты:')
            for link in parser.get_links():
                print(link)
            print('\nВнутренние ссылки с сайтов:')
            for inner_links in parser.get_inner_links(parser.get_links()):
                for inner_link in inner_links:
                    print(inner_link)
            break
        elif user_input == '2':
            file_name = input('Введите название для файла: ')
            with open(f'{file_name}.txt', 'w', encoding='utf-8') as file:
                file.write('Ссылки на сайты: \n')
                for link in parser.get_links():
                    file.write(link + '\n')
                file.write('\nВнутренние ссылки с сайтов:\n')
                for inner_links in parser.get_inner_links(parser.get_links()):
                    for inner_link in inner_links:
                        file.write(inner_link + '\n')
            break
        else:
            print('Выберите либо 1, либо 2!')


if __name__ == '__main__':
    main()
