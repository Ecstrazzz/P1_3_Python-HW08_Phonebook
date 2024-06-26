"""
Знакомство с языком Python (семинары)

Урок 8. Работа с файлами

Задача №49

Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате ".csv". Фамилия, имя, номер телефона - данные,
которые должны находиться в файле.

1. Программа должна выводить данные
2. Программа должна сохранять данные в файле
3. Пользователь может ввести одну из характеристик для
поиска определенной записи (Например имя или фамилию
человека)
4. Использование функций. Ваша программа не должна
быть линейной

Дополнить справочник возможностью копирования данных
из одного файла в другой. Пользователь вводит номер
строки, которую необходимо перенести из одного файла
в другой.

Формат сдачи: ссылка на свой репозиторий
"""

# Решение

import os
import difflib
from csv import DictReader, DictWriter
from os.path import exists


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    flag = False
    while not flag:
        try:
            first_name = input("Введите Имя: ")
            if len(first_name) < 2 or not first_name.isalpha():
                raise NameError("Слишком короткое имя или недопустимые символы")
            second_name = input("Введите Фамилию: ")
            if len(second_name) < 3 or not second_name.isalpha():
                raise NameError("Слишком короткая фамилия или недопустимые символы")
            phone_number = input("Введите номер телефона: ")
            if len(phone_number) != 11 or not phone_number.isdigit():
                raise NameError("Неверно указан номер телефона. (Пример: 81239876543)")
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]


def create_file(file_name):
    with open(file_name + ".csv", "w", encoding="utf-8", newline="") as file:
        f_w = DictWriter(file, fieldnames=["first_name", "second_name", "phone_number"])
        f_w.writeheader()


def write_file(file_name):
    res = read_file(file_name)
    user_data = get_info()
    new_obj = {
        "first_name": user_data[0],
        "second_name": user_data[1],
        "phone_number": user_data[2],
    }
    res.append(new_obj)
    standart_write(file_name, res)


def read_file(file_name):
    with open(file_name + ".csv", encoding="utf-8") as file:
        f_r = DictReader(file)
        return list(f_r)  # список со словарями


def remove_row(file_name):
    search = int(input("Введите номер строки для удаления: "))
    res = read_file(file_name)
    if search <= len(res):
        res.pop(search - 1)
        standart_write(file_name, res)
    else:
        print("Номер строки превышает количество строк в файле")


def standart_write(file_name, res):
    with open(file_name + ".csv", "w", encoding="utf-8", newline="") as file:
        f_w = DictWriter(file, fieldnames=["first_name", "second_name", "phone_number"])
        f_w.writeheader()
        f_w.writerows(res)


def list_csv_files():
    files = [f for f in os.listdir() if f.endswith(".csv")]
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    return files


def select_file(files):
    while True:
        try:
            choice = int(input("Выберите номер файла из списка: "))
            if 1 <= choice <= len(files):
                return files[choice - 1][:-4]  # Убираем расширение .csv из имени файла
            else:
                print("Неверный номер файла. Попробуйте снова")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите номер файла")


def copy_data(source_file, target_file):
    source_data = read_file(source_file)
    if not source_data:
        print("Исходный файл пуст или отсутствует")
        return

    row_number = int(input("Введите номер строки для копирования: "))
    if row_number <= 0 or row_number > len(source_data):
        print("Номер строки превышает количество строк в файле")
        return

    row_to_copy = source_data[row_number - 1]

    if not exists(target_file + ".csv"):
        create_file(target_file)

    target_data = read_file(target_file)
    target_data.append(row_to_copy)
    standart_write(target_file, target_data)


def search_by_name_and_surname(file_name):
    query = (
        input("Введите имя и/или фамилию для поиска (минимум 3 буквы): ")
        .strip()
        .lower()
    )

    if len(query) < 3:
        print("Запрос должен содержать минимум 3 буквы")
        return

    data = read_file(file_name)

    results = []

    for entry in data:
        full_name = f"{entry['first_name']} {entry['second_name']}".lower()
        matcher = difflib.SequenceMatcher(None, query, full_name)
        if matcher.find_longest_match(0, len(query), 0, len(full_name)).size >= 3:
            results.append((matcher.ratio(), entry))

    # Сортируем результаты по степени совпадения (в порядке убывания)
    results.sort(key=lambda x: x[0], reverse=True)

    if results:
        for i, (_, result) in enumerate(results, start=1):
            print(
                f"{i}. {result['first_name']} {result['second_name']} {result['phone_number']}"
            )
    else:
        print("Записи не найдены")


file_default = "phone"


def main():
    while True:
        print("\nМеню команд:")
        print("q - выход")
        print("w - запись данных")
        print("r - чтение данных")
        print("d - удаление строки")
        print("c - копирование данных")
        print("s - поиск по имени и фамилии")

        command = input("Введите команду: ")

        if command == "q":
            break

        elif command == "w":
            write_file(file_default)

        elif command == "r":
            if not exists(file_default + ".csv"):
                print("Файл отсутствует, пожалуйста создайте файл")
                continue
            print(*read_file(file_default))

        elif command == "d":
            if not exists(file_default + ".csv"):
                print("Файл отсутствует, пожалуйста создайте файл")
                continue
            remove_row(file_default)

        elif command == "c":
            files = list_csv_files()

            # Выбор исходного файла
            if files:
                source_file = select_file(files)

                # Выбор целевого файла
                target_files_listed_again = list_csv_files()

                # Убираем исходный файл из списка целевых
                target_files_listed_again.remove(source_file + ".csv")

                if target_files_listed_again:
                    print("Выберите целевой файл или создайте новый:")
                    for i, file in enumerate(target_files_listed_again):
                        print(f"{i + 1}. {file}")

                    choice = input(
                        "Введите номер для выбора существующего файла или 'n' для создания нового: "
                    )

                    if choice.lower() == "n":
                        target_file = input("Введите имя нового целевого файла: ")
                    else:
                        try:
                            choice = int(choice)
                            if 1 <= choice <= len(target_files_listed_again):
                                target_file = target_files_listed_again[choice - 1][:-4]
                            else:
                                print("Неверный выбор.")
                                continue
                        except ValueError:
                            print("Некорректный ввод. Пожалуйста, введите номер файла")
                            continue

                else:
                    target_file = input(
                        "Нет доступных файлов. Введите имя нового целевого файла: "
                    )

                copy_data(source_file, target_file)

            else:
                print(
                    "Нет доступных CSV файлов. Создайте файл при помощи команды w - запись данных"
                )

        elif command == "s":
            if not exists(file_default + ".csv"):
                print("Файл отсутствует, пожалуйста создайте файл")
                continue
            search_by_name_and_surname(file_default)


main()