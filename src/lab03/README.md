#ЛР_3 по ПиА.
##Задание А.
###normalize
Через if в начале проверяем соответствия условий во входных данных, при нужных значениях активируем определённые действия (casefold, yo2e). В таблице ASCII все служебные символы располагаются с первого (Null) по 31 (US, Unit Separator) + к этому 127 символ (DEL). Соответственно, в регулярке прописываем: заменить все такие символы на пробел в нашем тексте. Далее очищаем лишние пробелы и сплитуем. В конце возвращаем пересобранный текст, приведённый к нормали.
Обработка ошибок не предусматривается.
```
from re import*

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    #norm_text = " ".join(text.strip().split()) <- такой вариант не учитывает скрытые символы помимо лишних пробелов и переходов на следующую строку.
    return ' '.join(sub(r'[\x00-\x1F\x7F]', ' ', text).strip().split()) #<- поэтому изменено на регулярку
```
###Образец вывода
![text_normalize](/images/lab03/text_normalize.png)
###tokenize
При помощи регулярки (метода findall) ищем полные слова, либо слова по шаблону n символов, дефис, n символов.
Обработка ошибок не предусматривается.
```
def tokenize(text: str) -> list[str]:
    norm_text = normalize(text)
    return findall(r'\w+(?:-\w+)*', norm_text)
```
###Образец вывода
![text_tokenize](/images/lab03/text_tokenize.png)
###count_freq + top_n
В этом коде сразу две функции. Вывод понимать так: (входные данные) => (вывод count_freq) => (вывод top_n)
count_freq: цикл бежит по вводному списку, смотрит: 'такой токен есть в словаре'? Нет => записать, придать значение 1. Да => прибавить 1 к имеющемуся значению.
top_n: сортирует словарик через безымянную функцию. По стандарту сортировка будет возрастающей. Раз нам нужна убывающая по количеству токена, но возрастающая по его алфавитному значению - просто ставим минус перед item[1]. Следом записываем item[0] - этот параметр 'менее приоритетен' при сортировке. Возвращаем срез списка по n-ный элемент.
```
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
```
###Образец вывода
![text_freq_top_n](/images/lab03/text_freq_top_n.png)
##Задание B
Пояснения находятся внутри кода.
```
import sys
from src.lib.text import normalize, tokenize, count_freq, top_n

# \/\/\/\/ константа для вывода таблицей
TABLE_MODE = True


if __name__ == '__main__':
#\/\/\/ Избытычно, но делает режим через клавишу 'play' удобнее. Помогает игнорировать мусор, который мог бы залиться в stdin.
    if sys.stdin.isatty():
        print("--- Интерактивный режим ввода ---")
        print("Введите ваш текст ниже. После окончания ввода нажмите Enter, Ctrl+Z и затем ещё раз Enter:")
        # Читаем строки по одной (это игнорирует мусор от старта VS Code)
        lines = [] # <- сюда принимаем введённые строки
        try:
            for line in sys.stdin:
                lines.append(line)
        except KeyboardInterrupt: # <- на случай экстренного завершения/поломки (ctrl + c)
            pass 

        user_input = "".join(lines) # <- соединяем список строк в цельный текст.
    else:
        # Если данные вливаются через пайп в консоли (echo "текст" | ...), читаем мгновенно до EOF
        user_input = sys.stdin.read()

    tokens = tokenize(user_input)
    freq = count_freq(tokens)
    top = top_n(freq)

    print(f'Всего слов: {len(tokens)}\nУникальных слов: {len(freq)}')
        # Вместо print("Топ-5:", top_5_words) пишем:
    print("Топ-5:")
    if TABLE_MODE:
        max_word_len = max(max(len(word) for word, _ in top), len('слово')) # <- высчитываем максимальную длинну слов в таблице.
        print(f'{'Слово':<{max_word_len}} | Частота') # <- через f строку делаем красивый вывод, со сносом равным длинне самого длинного.
        print("-" * (max_word_len + 3 + len('Частота'))) # 3 - три символа: ' | '
        for word, count in top: # <- быстрая распаковка кортежей из списка.
            print(f'{word:<{max_word_len}} | {count}')
    else:
        for word, count in top:
            print(f"{word}:{count}")
```
###Для нормального вывода сначала переключите консоль и питон на кодировку UTF-8, иначе будет выводить рандомные символы.
```
chcp 65001 && echo "Привет, мир! Привет!!!" | python src/lab03/text_stats.py
```
###Образец вывода в стандартном режиме:
![text_stats](/images/lab03/text_stats.png)
###Образец вывода в интерактивном режиме:
![text_stats_interactive](/images/lab03/text_stats_interactive.png)
###Стресс-тест 'Лигурией':
![text_stats_stress_test](/images/lab03/text_stats_stress_test.png)