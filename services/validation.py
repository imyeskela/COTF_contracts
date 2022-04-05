def are_there_ru_words(text):
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text)


def are_there_special_symbols(text):
    special_symbols = set('!@#$^&*()_+="№;:?:;<>/|{}[]~`')
    return not special_symbols.isdisjoint(text)


def are_there_nums(text):
    nums = set('1234567890')
    return not nums.isdisjoint(text)


def is_valid_(text):

    if are_there_ru_words(text) == True and are_there_special_symbols(text) == True and are_there_nums(text) == True:
        return True
    else:
        return False

