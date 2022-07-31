from pprint import pprint
import csv
from pathlib import Path
import re

DIR_NAME = 'files'
file_name = 'phonebook_raw.csv'
path = Path(Path.cwd(), DIR_NAME, file_name)

def open_and_read_file_csv(file_path):
    with open(file_path) as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)
    return contacts_list


def _index_output_as_tuple(list):
    index = -1
    new_tuple = {}
    for item in list:
        index += 1
        _list = []
        _list.append(index)
        if f'{item[0]} {item[1]}' not in new_tuple:
            new_tuple[f'{item[0]} {item[1]}'] = _list
        else:
            new_tuple[f'{item[0]} {item[1]}'].append(index)
    return new_tuple


def split_full_name(patern, item):
    list_words_i0 = re.findall(patern, item[0])
    if len(list_words_i0) == 3:
        item[0] = list_words_i0[0]
        item[1] = list_words_i0[1]
        item[2] = list_words_i0[2]
    elif len(list_words_i0) == 2:
        item[0] = list_words_i0[0]
        item[1] = list_words_i0[1]
    list_words_i1 = re.findall(patern, item[1])
    if len(list_words_i1) == 2:
        item[1] = list_words_i1[0]
        item[2] = list_words_i1[1]
    return item


def _do_in_(index_tuple, el_list):
    index_for_add = []
    new_el_list = []
    for value in index_tuple.values():
        if len(value) == 2:
            a = el_list[value[0]]
            b = el_list[value[1]]
            for i in range(len(a)):
                if a[i] == '':
                    a[i] = b[i]
            el_list[value[0]] = a
            index_for_add.append(value[0])
        else:
            new_el_list.append(el_list[value[0]])
    for index in index_for_add:
        new_el_list.append(el_list[index])
    return new_el_list


def phones(list):
    change_list = []
    for element in list:
        phone_number = element[-2]
        if len(re.findall(r'[а-яёА-ЯЁ.]+', phone_number)) > 0:
            phone_number = re.sub(r'(\+7|8)\s*\(?(\d{3})[\)\s-]*(\d{3})[-]?(\d{2})[-]?(\d{2})\s\(?([а-яёА-ЯЁ.]+)\s(\d+)', r'7(\2)\3-\4-\5 \6\7', phone_number)
            # print(phone_number)
        else:
            phone_number = re.sub(r'(\+7|8)\s*\(?(\d{3})[\)\s-]*(\d{3})[-]?(\d{2})[-]?(\d{2})', r'+7(\2)\3-\4-\5', phone_number)
            # print(phone_number)
        element[-2] = phone_number
        change_list.append(element)
    return change_list


def do_in_list(data:list):
    el_list = []
    for el in data[1:]:
        el_list.append(split_full_name(r'\w+', el))
    index_tuple = _index_output_as_tuple(el_list)
    el_list = _do_in_(index_tuple, el_list)
    return phones(el_list)


def close_and_write_file_csv(file_path, list_to_wtite):
    with open(file_path, "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_to_wtite)


def main():
    file = open_and_read_file_csv(path)
    close_and_write_file_csv(path, do_in_list(file))


if __name__ == '__main__':
    main()

