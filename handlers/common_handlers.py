from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import find_dotenv, load_dotenv
from aiogram import Bot
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import reply
from parse import parse
from aiogram.fsm.state import StatesGroup, State
from database.schemas import LessonCreate, LessonEdit
from database import crud
from common.white_users import white_users_id

DENY_ACCESS_MESSAGE = 'У вас нет прав доступа к этому боту!'

load_dotenv(find_dotenv())

handlers_router = Router()


class FSMLessonForm(StatesGroup):
    pupil_name = State()  # Состояние ожидания ввода имени ученика
    date = State()  # Состояние ожидания ввода даты
    time = State()  # Состояние ожидания ввода времени
    comment = State()  # Состояние ожидания ввода комментария
    is_audition = State()  # Состояние ожидания ввода прослушивания


# Bot greeting
@handlers_router.message(Command('start'))
async def process_command_start(message: types.Message, state: FSMContext):
    if message.from_user.id not in white_users_id:
        await message.reply(DENY_ACCESS_MESSAGE)
    else:
        await message.reply('<b>Добро пожаловать в телеграм бот!</b>', reply_markup=reply.inline_kb1)
        # Сбрасываем состояние и очищаем данные, полученные внутри состояний
        await state.clear()


# Bot clear chat
@handlers_router.message(Command('clear'))
async def cmd_clear(message: types.Message, bot: Bot) -> None:
    if message.from_user.id not in white_users_id:
        await message.reply(DENY_ACCESS_MESSAGE)
    else:
        try:
            # Все сообщения, начиная с текущего и до первого (message_id = 0)
            for i in range(message.message_id, 0, -1):
                await bot.delete_message(message.from_user.id, i)
        except TelegramBadRequest as ex:
            # Если сообщение не найдено (уже удалено или не существует),
            # код ошибки будет "Bad Request: message to delete not found"
            if ex.message == "Bad Request: message to delete not found":
                return 'Все сообщения удалены'


# Show timetable via Command
@handlers_router.message(Command('show_timetable'))
async def show_weekly_timetable_via_command(message: types.Message):
    if message.from_user.id not in white_users_id:
        await message.reply(DENY_ACCESS_MESSAGE)
    else:
        date_start = parse.get_date_start_week()
        date_end = parse.get_date_end_of_week()
        output_data = parse.show_week_timetable(date_start, date_end)
        if output_data:
            await message.answer(output_data)
        else:
            await message.answer('<b>На данной неделе занятий нет!</b>')


# Show timetable via inline button
@handlers_router.callback_query(F.data == 'show_timetable')
async def show_weekly_timetable_via_inline_btn(callback: types.CallbackQuery):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        date_start = parse.get_date_start_week()
        date_end = parse.get_date_end_of_week()
        output_data = parse.show_week_timetable(date_start, date_end)
        if output_data:
            await callback.message.answer(output_data)
        else:
            await callback.message.answer('<b>На данной неделе занятий нет!</b>')


# Get dates for timetable
@handlers_router.callback_query(F.data == 'show_timetable_by_dates')
async def get_dates_for_timetable_for_period(callback: types.CallbackQuery):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        await callback.message.answer('<b>Введите период дат в следующем формате:\n15.01.2000 - 19.01.2000</b>')


import re


# Show timetable for period
@handlers_router.message(F.text.regexp(re.compile(r'\d{2}.\d{2}.\d{4} - \d{2}.\d{2}.\d{4}')))
async def show_timetable_for_period(message: types.Message):
    if message.from_user.id not in white_users_id:
        await message.answer(DENY_ACCESS_MESSAGE)
    else:
        input_data = message.text.split('-')

        date_start = input_data[0].strip()
        date_start = f'{date_start[6:]}-{date_start[3:5]}-{date_start[:2]}'

        date_end = input_data[1].strip()
        date_end = f'{date_end[6:]}-{date_end[3:5]}-{date_end[:2]}'
        print(f'{date_start=} {date_end=}')

        output_data = parse.show_week_timetable(date_start, date_end)
        print(f'{output_data}')

        if output_data:
            await message.answer(output_data)
        else:
            await message.answer('<b>На данной неделе занятий нет!</b>')


# Process edit lesson
@handlers_router.callback_query(F.data == 'edit_lesson')
async def process_edit_lesson_1(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        inline_keyboard_buttons = []
        data = await state.get_data()

        for idx, item in enumerate(list(crud.get_list_times_by_date(data['date']))):
            inline_keyboard_buttons.append([
                InlineKeyboardButton(text=f'{item[0]}', callback_data=f'time_{idx}')
            ])

        select_time_for_edit_lesson = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard_buttons
        )
        await callback.message.answer(
            '<b>Выберите время для редактирования занятия:</b>', reply_markup=select_time_for_edit_lesson
        )


# Process edit lesson
@handlers_router.callback_query(F.data.in_([f'time_{x}' for x in range(20)]))
async def process_edit_lesson_2(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        temp_dict = {}
        data = await state.get_data()

        for idx, item in enumerate(list(crud.get_list_times_by_date(data['date']))):
            temp_dict[f'time_{idx}'] = item[0]

        current_lesson = crud.get_lesson_by_date_and_time(data['date'], temp_dict[callback.data])

        await state.update_data(time=temp_dict[callback.data])
        msg_text = f'Введите время занятия и имя ученика в формате:\n\n' \
                   f'<b>р: {current_lesson.time} - {current_lesson.pupil_name}</b>\n\n' \
                   f'Если нужно добавить комментарий, то отправьте сообщение в формате:\n\n' \
                   f'<b>р: {current_lesson.time} - {current_lesson.pupil_name} - тут ваш комментарий</b>'
        await callback.message.answer(msg_text)


# Edit lesson
@handlers_router.message(F.text.lower().contains('р:'))
async def process_edit_lesson_3(message: types.Message, state: FSMContext):
    if message.from_user.id not in white_users_id:
        await message.reply(DENY_ACCESS_MESSAGE)
    else:
        updated_lesson = None
        lesson_pupil_name = None
        lesson_time = None
        data = await state.get_data()
        lesson_comment = ''
        if len(message.text[2:].split('-')) == 2:
            lesson_time, lesson_pupil_name = message.text[2:].split('-')

        if len(message.text[2:].split('-')) == 3:
            lesson_time, lesson_pupil_name, lesson_comment = message.text[2:].split('-')

        try:
            update_lesson = LessonEdit(
                pupil_name=lesson_pupil_name.strip(),
                date=data['date'],
                time=lesson_time.strip(),
                comment=lesson_comment.strip()
            )
            updated_lesson = crud.edit_lesson(data['date'], data['time'], update_lesson)
        except:
            await message.answer('<b>Вы ввели данные в неправильном формате. Попробуйте еще раз!</b>')

        if updated_lesson:
            await message.answer('<b>Вы отредактировали текущее занятие!</b>')
        await state.clear()


# Process delete lesson
@handlers_router.callback_query(F.data == 'delete_lesson')
async def process_delete_lesson(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        inline_keyboard_buttons = []
        data = await state.get_data()

        for idx, item in enumerate(list(crud.get_list_times_by_date(data['date']))):
            inline_keyboard_buttons.append([
                InlineKeyboardButton(text=f'{item[0]}', callback_data=f'del_time_{idx}')
            ])

        select_time_for_delete_lesson = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard_buttons
        )
        await callback.message.answer(
            '<b>Выберите время занятия для удаления:</b>', reply_markup=select_time_for_delete_lesson
        )


# Delete lesson
@handlers_router.callback_query(F.data.in_([f'del_time_{x}' for x in range(20)]))
async def delete_lesson_by_date_and_time(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        temp_dict = {}
        data = await state.get_data()

        for idx, item in enumerate(list(crud.get_list_times_by_date(data['date']))):
            temp_dict[f'del_time_{idx}'] = item[0]

        result = crud.delete_lesson(data['date'], temp_dict[callback.data])

        if result:
            await callback.message.answer('<b>Занятие было удалено!</b>')
        else:
            await callback.message.answer('<b>Такого занятия не существует!</b>')
        await state.clear()


# Choose week day via Command(week timetable)
@handlers_router.message(Command('editing_timetable'))
async def process_select_weekday_via_command(message: types.Message, state: FSMContext):
    if message.from_user.id not in white_users_id:
        await message.answer(DENY_ACCESS_MESSAGE)
    else:
        await message.answer('<b>Выберите день недели:</b>', reply_markup=reply.get_inline_keyboard())
        await state.update_data(date=F.data)


# Choose week day (week timetable)
@handlers_router.callback_query(F.data == 'editing_timetable')
async def process_select_weekday(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        await callback.message.answer('<b>Выберите день недели:</b>', reply_markup=reply.get_inline_keyboard())
        await state.update_data(date=F.data)


# Create, edit or delete lesson
@handlers_router.callback_query(F.data.in_(parse.get_list_dates()))
async def process_select_actions(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        await state.update_data(date=callback.data,
                                comment='',
                                is_audition=False)
        await callback.message.answer(
            '<b>Выберите действие:</b>', reply_markup=reply.new_edit_or_delete_lesson_kb1
        )


# Choose type of lesson
@handlers_router.callback_query(F.data == 'new_lesson')
async def process_create_lesson_1(callback: types.CallbackQuery):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        await callback.message.answer(
            '<b>Выберите действие:</b>', reply_markup=reply.select_the_type_of_person_involved_kb1
        )


# Process create lesson
@handlers_router.callback_query(F.data.in_(['usual_lesson', 'listening']))
async def process_create_lesson_2(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in white_users_id:
        await callback.message.answer(DENY_ACCESS_MESSAGE)
    else:
        if callback.data == 'listening':
            await state.update_data(is_audition=True)
        await callback.message.answer(
            '<b>Введите время занятия и имя ученика в формате: 09:00 - Иванов Иван</b>'
        )
        await state.set_state(FSMLessonForm.pupil_name)


# Create lesson
@handlers_router.message(F.text.regexp(r'^\d{2}:\d{2}\D*'))
async def process_create_lesson_3(message: types.Message, state: FSMContext):
    if message.from_user.id not in white_users_id:
        await message.reply(DENY_ACCESS_MESSAGE)
    else:
        input_text = message.text
        input_data = input_text.split('-')
        await state.update_data(pupil_name=input_data[1].strip(), time=input_data[0].strip())

        data = await state.get_data()
        new_lesson = LessonCreate(**data)

        if not crud.create_lesson(new_lesson):
            msg_text = '<b>На данное время уже есть занятие!</b>'
        else:
            msg_text = (f'<b>Вы добавили новое занятие:\n'
                        f'\t Дата: {".".join(data.get("date").split("-")[::-1])}\n'
                        f'\t Время: {data.get("time")}\n'
                        f'\t Занимающийся: {data.get("pupil_name")}</b>')

        await message.answer(msg_text)
        await state.clear()
