def validate_room_name(name):
    if not name:
        return "Название помещения не может быть пустым"
    if len(name) > 128:
        return f"Название слишком длинное (макс. 128 символов)"
    return None


def validate_volume(vol):
    if vol <= 0:
        return "Объём должен быть положительным числом"
    return None


def validate_temperature(temp, field_name):
    if temp < -50 or temp > 60:
        return f"{field_name} должен быть в диапазоне от -50 до 60"
    return None


def validate_temp_range(min_t, max_t):
    if min_t > max_t:
        return f"Минимальная температура ({min_t}) не может быть больше максимальной ({max_t})"
    return None


def validate_humidity(hum, field_name):
    if hum < 0 or hum > 100:
        return f"{field_name} должен быть в пределах 0..100"
    return None


def validate_humid_range(min_h, max_h):
    if min_h > max_h:
        return f"Минимальная влажность ({min_h}) не может быть больше максимальной ({max_h})"
    return None


def validate_positive_int(value, name):
    try:
        v = int(value)
        if v <= 0:
            return f"{name} должно быть целым положительным числом"
        return None
    except ValueError:
        return f"{name} должно быть целым числом"


def validate_positive_number(value, name):
    try:
        v = float(value)
        if v <= 0:
            return f"{name} должно быть положительным числом"
        return None
    except ValueError:
        return f"{name} должно быть числом"
