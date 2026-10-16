from re import*
# from unicodedata import*

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    #norm_text = " ".join(text.strip().split()) <- такой вариант не учитывает скрытые символы помимо лишних пробелов и переходов на следующую строку.
    return ' '.join(sub(r'[\x00-\x1F\x7F]', ' ', text).strip().split()) #<- поэтому изменено на регулярку

def tokenize(text: str) -> list[str]:
    norm_text = normalize(text)
    return findall(r'\w+(?:-\w+)*', norm_text)

def count_freq(tokens: list[str]) -> dict[str, int]:
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    return freq_dict

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    sorted_freq = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    return sorted_freq[:n]


if __name__ == '__main__':
    normalize_tests = [
        ("ПрИвЕт\nМИр\t", True, False), 
        ("ёжик, Ёлка", False, True),
        ("Hello\r\nWorld", True, False),
        ("  двойные   пробелы  ", True, False)
    ]
    # for test in normalize_tests:
    #    print(test, ' => \"', normalize(test[0], casefold=test[1], yo2e=test[2]), '\"', sep='')
    # text = "Привет! 14 Октября на e-mail пришел социально-экономический опрос. Emoji 😀 в нём не было."
    # print(findall(r'\w+(?:-\w+)*', text))
    tokenize_tests = [
        "привет мир",
        "hello,world!!!",
        "по-настоящему круто",
        "2025 год",
        "emoji 😀 не слово",
        "Привет! 14 Октября на e-mail кое-кто-то прислал социально-экономический опрос. Emoji 😀 в нём не было."
    ]
    # for test in tokenize_tests:
    #     print(test, '=>', tokenize(test))
    # print(top_n(count_freq(['привет', 'мир', 'привет', 'привет', 'привет', 'я', 'я', 'aa', 'aa', 'aa', 'aa'])))

    count_freq_top_n_tests = [
        ["a","b","a","c","b","a"],
        ["bb","aa","bb","aa","cc"],
        tokenize('ёжик, ежик; ёжик= ёжик: ежик !крош          ')
    ]
    for test in count_freq_top_n_tests:
        print(test, '=>', count_freq(test), '=>', top_n(count_freq(test), n=2))