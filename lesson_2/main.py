from __future__ import annotations
import random
import time
import os


class Player:
    def __init__(self, card: Card, name=None):
        self.card = card
        self.name = name

    def __str__(self):
        return str(self.card)


class Card:
    def __init__(self):
        self.numbers = []
        self.generate_card()

    def __str__(self):
        return ' '.join(str(number) for number in self.numbers)

    def generate_card(self):
        all_numbers = []
        while len(all_numbers) < 15:
            random_number = random.randint(1, 90)
            if not random_number in all_numbers:
                all_numbers.append(random_number)
        self.numbers.extend(sorted(all_numbers))


class Bag:
    def __init__(self):
        self.barrels = [num for num in range(1, 91)]

    def __len__(self):
        return len(self.barrels)

    def get_new_barrel(self):
        barrel = random.choice(self.barrels)
        self.barrels.remove(barrel)
        return barrel


class Game:
    def __init__(self):
        self.bag = Bag()
    
    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def check_input(user, barrel, user_name=False):
        while True:
            if user_name:
                user_input = input(f'\n{user.name}, зачеркнуть цифру? (y/n) ')
            else:
                user_input = input('\nЗачеркнуть цифру? (y/n) ')

            if user_input == 'q':
                return False
            elif user_input == 'y':
                if barrel in user.card.numbers:
                    for index, number in enumerate(user.card.numbers):
                        if number == barrel:
                            user.card.numbers[index] = '-'
                else:
                    if user_name:
                        print(
                            f'\n{user.name}, у вас нет этой цифры! Вы проиграли.\n')
                    else:
                        print('\nУ вас нет этой цифры! Вы проиграли.\n')
                    return False
                break
            elif user_input == 'n':
                if barrel in user.card.numbers:
                    if user_name:
                        print(
                            f'\n{user.name}, у вас была эта цифра, но вы не зачеркнули её! Вы проиграли.\n')
                    else:
                        print(
                            '\nУ вас была эта цифра, но вы не зачеркнули её! Вы проиграли.\n')
                    return False
                break
            else:
                print('\nВыберите правильный вариант!')
        return True

    @staticmethod
    def play_again():
        user_input = input('Будете играть ещё? (y/n) ')
        if user_input == 'y':
            main()

    @staticmethod
    def check_player_win(users):
        winners_list = []

        for user in users.values():
            if len(set(user.card.numbers)) <= 1:
                winners_list.append(user)

        if len(winners_list) == 1:
            print(f'{winners_list[0].name}, поздравляем, вы выиграли!\n')
            return True
        elif len(winners_list) > 1:
            print('Победителей несколько:')
            for user in winners_list:
                print(f'{user.name}')
            print('\nПоздравляем!\n')
            return True

    def human_vs_ai(self):
        card_user = Card()
        card_ai = Card()

        user = Player(card_user)
        ai = Player(card_ai)

        while True:
            self.cls()

            if len(set(user.card.numbers)) <= 1 and len(set(ai.card.numbers)) <= 1:
                print('\nНичья!')
                break
            elif len(set(user.card.numbers)) <= 1:
                print('\nПоздравляем, вы выиграли!')
                break
            elif len(set(ai.card.numbers)) <= 1:
                print('\nВы проиграли.')
                break

            new_barrel = self.bag.get_new_barrel()

            print('*** Чтобы выйти из игры, введите "q" ***\n')
            print(f'Новый бочонок: {new_barrel} (осталось {len(self.bag)})')
            print(f'Ваша карточка: {user.card}')
            print(f'Карточка компьютера: {ai.card}')

            if self.check_input(user, new_barrel) == False:
                break

            for index, number in enumerate(ai.card.numbers):
                if number == new_barrel:
                    ai.card.numbers[index] = '-'

        self.play_again()

    def ai_vs_ai(self):
        card_ai_1 = Card()
        card_ai_2 = Card()

        ai_1 = Player(card_ai_1)
        ai_2 = Player(card_ai_2)
        all_ai = [ai_1, ai_2]

        while True:
            self.cls()

            if len(set(ai_1.card.numbers)) <= 1 and len(set(ai_2.card.numbers)) <= 1:
                print('\nНичья!')
                break
            elif len(set(ai_1.card.numbers)) <= 1:
                print('\nПобедил компьютер 1!')
                break
            elif len(set(ai_2.card.numbers)) <= 1:
                print('\nПобедил компьютер 2!')
                break

            new_barrel = self.bag.get_new_barrel()

            print(f'Новый бочонок: {new_barrel} (осталось {len(self.bag)})')
            print(f'Карточка компьютера 1: {ai_1.card}')
            print(f'Карточка компьютера 2: {ai_2.card}')

            for ai in all_ai:
                for index, number in enumerate(ai.card.numbers):
                    if number == new_barrel:
                        ai.card.numbers[index] = '-'

            time.sleep(1)

        self.play_again()

    def multiplayer(self, players):
        self.cls()

        cards = {}
        for i in range(players):
            cards[i] = Card()

        users = {}
        for i in range(players):
            while True:
                name = input(f'Игрок {i + 1}, введите ваше имя: ')
                if not name:
                    print('Введите имя!')
                else:
                    break
            users[f'user_{i}'] = Player(cards[i], name)

        is_on = True
        while is_on:
            self.cls()

            if self.check_player_win(users) == True:
                break

            new_barrel = self.bag.get_new_barrel()

            print('*** Чтобы выйти из игры, введите "q" ***\n')
            print(f'Новый бочонок: {new_barrel} (осталось {len(self.bag)})')
            for user in users.values():
                print(f'Карточка {user.name}: {user.card}')

            for user in users.values():
                if self.check_input(user, new_barrel, user_name=True) == False:
                    is_on = False
                    break

        self.play_again()


def main():
    game = Game()
    game.cls()

    print('Какой режим игры выбираете? Ввведите соотвествующую цифру: \
        \n1 - Классический (человек против компьютера) \
        \n2 - Один на один (человек против человека) \
        \n3 - Мультиплеер (несколько человек друг против друга) \
        \n4 - Компьютер против компьютера \
        \nq - Выйти из игры\n'
          )

    while True:
        user_choice = input('Ваш выбор: ')
        if user_choice == '1':
            game.human_vs_ai()
            break
        elif user_choice == '2':
            game.multiplayer(2)
            break
        elif user_choice == '3':
            while True:
                try:
                    number_of_players = int(
                        input('Введите количество игроков: '))
                    if number_of_players < 2:
                        print('Игроков должно быть как минимум двое!')
                        continue
                    game.multiplayer(number_of_players)
                    break
                except ValueError:
                    print('Введите цифру!')
            break
        elif user_choice == '4':
            game.ai_vs_ai()
            break
        elif user_choice == 'q':
            print('\nПока!')
            break
        else:
            print('Введите вариант из предложенных!')


if __name__ == '__main__':
    main()
