from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from parse import parse
from week_days import NUMBER_OF_THE_WEEK_DAY as NWD

# Main menu
inline_btn_1 = InlineKeyboardButton(text='Просмотр расписания', callback_data='show_timetable')
inline_btn_2 = InlineKeyboardButton(text=f'Расписаниe за определенный период',
                                    callback_data='show_timetable_by_dates')
inline_btn_3 = InlineKeyboardButton(text='Редактирование', callback_data='editing_timetable')

inline_kb1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_btn_1],
        [inline_btn_2],
        [inline_btn_3],
    ]
)


def get_inline_keyboard() -> InlineKeyboardMarkup:
    dates_list = parse.get_list_dates_and_weekdays()

    # Submenu week days
    week_days_btn_1 = InlineKeyboardButton(text=NWD[dates_list[0][1]], callback_data=dates_list[0][0])
    week_days_btn_2 = InlineKeyboardButton(text=NWD[dates_list[1][1]], callback_data=dates_list[1][0])
    week_days_btn_3 = InlineKeyboardButton(text=NWD[dates_list[2][1]], callback_data=dates_list[2][0])
    week_days_btn_4 = InlineKeyboardButton(text=NWD[dates_list[3][1]], callback_data=dates_list[3][0])
    week_days_btn_5 = InlineKeyboardButton(text=NWD[dates_list[4][1]], callback_data=dates_list[4][0])
    week_days_btn_6 = InlineKeyboardButton(text=NWD[dates_list[5][1]], callback_data=dates_list[5][0])
    week_days_btn_7 = InlineKeyboardButton(text=NWD[dates_list[6][1]], callback_data=dates_list[6][0])
    week_days_btn_8 = InlineKeyboardButton(text=NWD[dates_list[7][1]], callback_data=dates_list[7][0])

    week_days_kb1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [week_days_btn_1],
            [week_days_btn_2],
            [week_days_btn_3],
            [week_days_btn_4],
            [week_days_btn_5],
            [week_days_btn_6],
            [week_days_btn_7],
            [week_days_btn_8],
        ]
    )
    return week_days_kb1


# Create, edit or delete lesson
new_lesson_btn_1 = InlineKeyboardButton(text='Добавить занятие', callback_data='new_lesson')
edit_lesson_bth2 = InlineKeyboardButton(text='Редактировать занятие', callback_data='edit_lesson')
delete_lesson_btn3 = InlineKeyboardButton(text='Удалить занятие', callback_data='delete_lesson')

new_edit_or_delete_lesson_kb1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [new_lesson_btn_1],
        [edit_lesson_bth2],
        [delete_lesson_btn3],
    ]
)

# Choose type of lesson
usual_lesson_btn_1 = InlineKeyboardButton(text='Обычное занятие', callback_data='usual_lesson')
listening_btn_3 = InlineKeyboardButton(text='Прослушивание', callback_data='listening')

select_the_type_of_person_involved_kb1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [usual_lesson_btn_1],
        [listening_btn_3],
    ]
)
