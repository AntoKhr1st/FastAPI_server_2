import re


def identify_data_type(input_string):
    # Паттерн для проверки email
    email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')

    # Паттерн для проверки телефона с форматом +7...
    phone_pattern = re.compile(r'^\+7[ -]?\d{3}[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$')

    # Паттерн для проверки даты в форматах DD.MM.YYYY или YYYY-MM-DD
    date_pattern = re.compile(r'^(\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})$')

    # Если соответствует паттерну email
    if email_pattern.match(input_string):
        return "email"
    # Если соответствует паттерну телефона
    elif phone_pattern.match(input_string):
        return "phone"
    # Если соответствует паттерну даты
    elif date_pattern.match(input_string):
        return "date"
    # В противном случае считаем это текстом
    else:
        return "text"


# input_string = "+78005553535"
# result = identify_data_type(input_string)
# print(result)  # Выведет "email"

def get_field_types(query_params):
    # Создаем словарь для хранения типов полей
    field_types = {}

    # Порядок проверки типов данных: дата, телефон, email, текст
    for field in query_params:
        if (query_params[field]) == "date":
            field_types[field] = "date"
        elif (query_params[field]) == "phone":
            field_types[field] = "phone"
        elif (query_params[field]) == "email":
            field_types[field] = "email"
        else:
            field_types[field] = "text"

    return field_types


def max_dict_from_list(list_of_dicts):
    max_length = max(map(len, list_of_dicts))
    longest_dicts = [d for d in list_of_dicts if len(d) == max_length]
    return longest_dicts
