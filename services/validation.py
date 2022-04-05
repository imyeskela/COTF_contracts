def are_there_ru_words(text):
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())


def are_there_special_symbols(text):
    special_symbols = set('!@#$^&*()_+="№;:?:;<>/|{}[]~`')
    return special_symbols.isdisjoint(text.lower())


def are_there_nums(text):
    nums = set('1234567890')
    return nums.isdisjoint(text.lower())


def is_valid_(text):

    if are_there_ru_words(text.lower()) == True and are_there_special_symbols(text.lower()) == True and are_there_nums(text.lower()) == True:
        return True
    else:
        return False

