from datetime import datetime, timedelta
from collections import defaultdict
from database import crud
from week_days import NUMBER_OF_THE_WEEK_DAY as NWD


def get_date_of_lesson(target_number_day_of_week: int) -> datetime.date:
    """Возвращает дату урока в зависимости от выбранного дня текущей недели"""
    current_weekday = datetime.now().weekday()
    time_delta = timedelta(days=(target_number_day_of_week - current_weekday))
    return datetime.now().date() + time_delta


def get_date_start_week() -> datetime.date:
    """Возвращает дату текущего дня"""
    return datetime.now().date()


def get_date_end_of_week() -> datetime.date:
    """Возвращает дату текущего дня + 7 дней"""
    return get_date_start_week() + timedelta(days=7)


def show_week_timetable(date_start, date_end):
    """Возвращает расписание в диапазоне дат date_start - date_end"""
    output_dict = defaultdict(list)
    output_data = ''

    lessons = crud.get_week_timetable(date_start, date_end)

    for lesson in lessons:
        key = f'{NWD[lesson.date.weekday()]} {".".join(str(lesson.date)[:10].split("-")[::-1])}'

        if lesson.comment in [0, '0']:
            lesson.comment = '&#10060;'

        if lesson.is_audition:
            if lesson.comment:
                output_dict[key].append(
                    f'{lesson.time} - {lesson.pupil_name} (Прослушивание) ({lesson.comment})')
            else:
                output_dict[key].append(f'{lesson.time} - {lesson.pupil_name} (Прослушивание)')
        else:
            if lesson.comment:
                output_dict[key].append(f'{lesson.time} - {lesson.pupil_name} ({lesson.comment})')
            else:
                output_dict[key].append(f'{lesson.time} - {lesson.pupil_name}')

    for key, values in output_dict.items():
        output_data += f'{key}:\n'

        for value in values:
            output_data += f'\t\t\t{value}\n'
        output_data += '\n\n'

    return output_data


def get_list_dates_and_weekdays():
    """Возвращает список дат от текущего дня до даты: текущий день + 7"""
    output_dates = []
    current_date = datetime.now().date()

    for t_delta in range(8):
        new_date = current_date + timedelta(days=t_delta)
        current_weekday = new_date.weekday()
        output_dates.append((str(new_date), current_weekday))

    return output_dates


def get_list_dates():
    return [item[0] for item in get_list_dates_and_weekdays()]


