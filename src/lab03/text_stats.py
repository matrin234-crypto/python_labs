import sys
from src.lib.text import normalize, tokenize, count_freq, top_n

# константа для вывода таблицей \/\/\/\/
TABLE_MODE = True


if __name__ == '__main__':
#Избытычно, но делает режим через клавишу 'play' немного удобнее. Помогает игнорировать мусор, который мог бы залиться в stdin.
    if sys.stdin.isatty():
        print("--- Интерактивный режим ввода ---")
        print("Введите ваш текст ниже. После окончания ввода нажмите Enter, Ctrl+Z и затем ещё раз Enter:")
        # Читаем строки по одной (это игнорирует мусор от старта VS Code)
        lines = []
        try:
            for line in sys.stdin:
                lines.append(line)
        except KeyboardInterrupt:
            pass

        user_input = "".join(lines)
    else:
        # Если данные вливаются через пайп (echo "текст" | ...), читаем мгновенно до EOF
        user_input = sys.stdin.read()

    tokens = tokenize(user_input)
    freq = count_freq(tokens)
    top = top_n(freq)

    print(f'Всего слов: {len(tokens)}\nУникальных слов: {len(freq)}')
        # Вместо print("Топ-5:", top_5_words) пишем:
    print("Топ-5:")
    if TABLE_MODE:
        max_word_len = max(max(len(word) for word, _ in top), len('слово'))
        print(f'{'Слово':<{max_word_len}} | Частота')
        print("-" * (max_word_len + 3 + len('Частота'))) # 3 - три символа: ' | '
        for word, count in top:
            print(f'{word:<{max_word_len}} | {count}')
    else:
        for word, count in top:
            print(f"{word}:{count}")

    