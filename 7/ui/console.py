import os


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def input_str(prompt, allow_empty=False, max_len=None):
    while True:
        val = input(prompt).strip()
        if not allow_empty and not val:
            print("Поле не может быть пустым. Попробуйте снова.")
            continue
        if max_len and len(val) > max_len:
            print(f"Слишком длинное (макс. {max_len} символов).")
            continue
        return val


def input_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Значение должно быть >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Значение должно быть <= {max_val}")
                continue
            return val
        except ValueError:
            print("Введите целое число.")


def input_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Значение должно быть >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Значение должно быть <= {max_val}")
                continue
            return val
        except ValueError:
            print("Введите число.")


def display_table(columns, rows, row_numbers=True):
    """Универсальный вывод таблицы.
    columns: список названий колонок
    rows: список кортежей записей (без номеров)
    row_numbers: добавлять колонку '№' слева
    """
    if not rows:
        print("Нет данных.")
        return
    if row_numbers:
        cols = ["№"] + list(columns)
        data = [(i + 1,) + row for i, row in enumerate(rows)]
    else:
        cols = columns
        data = rows

    # Динамическая ширина (не менее 10, не более 30)
    widths = []
    for i in range(len(cols)):
        max_width = max(
            len(str(cols[i])), max((len(str(row[i])) for row in data), default=0)
        )
        widths.append(min(max(max_width, 10), 30))

    # Заголовок
    header = " | ".join(cols[i].ljust(widths[i]) for i in range(len(cols)))
    print(header)
    print("-" * len(header))
    for row in data:
        line = " | ".join(str(row[i]).ljust(widths[i]) for i in range(len(cols)))
        print(line)


def select_from_list(items, prompt="Выберите"):
    """items: список кортежей (номер_для_показа, значение_возврата, описание)
    возвращает выбранное значение_возврата или None
    """
    if not items:
        print("Нет доступных элементов.")
        return None
    print(prompt)
    for num, ret_val, desc in items:
        print(f"  {num}. {desc}")
    while True:
        try:
            choice = int(input("=> Номер: "))
            for num, ret_val, _ in items:
                if num == choice:
                    return ret_val
            print("Неверный номер.")
        except ValueError:
            print("Введите число.")


def menu_loop(title, options, handler):
    """options: dict {key: description}
    handler: функция, принимающая key"""
    while True:
        clear()
        print(f"--- {title} ---")
        for k, desc in options.items():
            print(f"{k}. {desc}")
        print("0. Выход / Назад")
        choice = input("=> ").strip()
        if choice == "0":
            break
        if choice in options:
            handler(choice)
        else:
            print("Неизвестная опция. Нажмите Enter.")
            input()
