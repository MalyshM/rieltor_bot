key_dict = {'name': 'Имя в тг', 'id': 'Айди в тг', 'url': 'Ссылка на пользователя через айди в тг',
            'username': 'Ссылка на пользователя стандартная', 'type_of_object_buy': 'Тип объекта к покупке',
            'cost_range': 'Разброс стоимости',
            'number_of_rooms': 'Количество комнат', 'square': 'Площадь',
            'location': 'Желаемый район/тракт/населенный пункт', 'calculation_format': 'Тип расчета',
            'years': 'Количество полных лет', 'children': 'Количество детей',
            'family_mortgage': 'Семейная ипотека', 'rural_mortgage': 'Сельская ипотека', 'base_rate': 'Базовая ставка',
            'IT_mortgage': 'ИТ ипотека', 'state_support_2020': 'Господдержка 2020',
            'full_name': 'ФИО', 'birth_date': 'Дата рождения', 'phone': 'Личный телефон',
            'monthly_income': 'Месячный доход', 'workplace': 'Место работы', 'work_phone': 'Рабочий телефон',
            'credit_amount': 'Желаемое количество денег на ипотеку', 'is_approved': 'Одобрена ли ипотека',
            'IS_TRUE': 'Есть ли желание рассчитать стоимость своей недвижимости', 'TYPE_OF_OBJECT': 'Тип объекта',
            'address': 'Адрес недвижимости',
            'type_of_object_buy_detail': 'Тип объекта к покупке детально',
            'land_square': 'Площадь земельного участка', }


def prettify_dict_str(data: dict):
    result_str = '\n'
    for key, item in data.items():
        try:
            result_str += f'{key_dict[key]} - {item},\n'
        except Exception:
            pass
    return result_str[:-2]
