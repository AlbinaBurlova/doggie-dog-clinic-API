import os
import logging
import json

from dotenv import load_dotenv
from aiohttp import ClientSession

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

logging.basicConfig(level=logging.INFO)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class FSMFillForm(StatesGroup):
    create_dog = State()
    update_dog = State()
    get_dog_by_pk = State()


# Создаем объекты инлайн-кнопок
button_get_root = InlineKeyboardButton(
    text='Получить приветствие',
    callback_data='GET_ROOT'
)

button_post_post = InlineKeyboardButton(
    text='Получить записи',
    callback_data='POST_POST'
)

button_get_dogs = InlineKeyboardButton(
    text='Получить список собак',
    callback_data='GET_DOGS'
)

button_create_dog = InlineKeyboardButton(
    text='Добавить новую собаку',
    callback_data='CREATE_DOG'
)

button_get_dog_by_pk = InlineKeyboardButton(
    text='Получить информацию о собаке по идентификатору',
    callback_data='GET_DOG_BY_PK'
)

button_update_dog = InlineKeyboardButton(
    text='Обновить информацию о собаке',
    callback_data='UPDATE_DOG'
)

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_get_root, button_post_post],
        [button_get_dogs, button_create_dog],
        [button_get_dog_by_pk],
        [button_update_dog]
    ]
)


# добавим проверку на случай, если сервер не отвечает
async def is_server_available(url: str) -> bool:
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return response.status == 200
    except:
        return False


@dp.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    # на всякий случай скидываем состояние
    await state.clear()
    if await is_server_available(API_URL):
        await message.answer(
            text='Выберите действие, нажав на одну из кнопок ниже.',
            reply_markup=keyboard
        )
    else:
        await message.answer(
            text='Простите, но сервер сейчас недоступен, бот не может продолжить свою работу. Попробуйте позже через кнопку /start'
        )


@dp.callback_query(F.data == 'CREATE_DOG')
async def process_create_dog(callback_query: CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите данные о собаке в формате: имя, pk (идентификатор), вид. Не забудьте, что клиника работает только с тремя видами собак: terrier, bulldog или dalmatian")
    await state.set_state(FSMFillForm.create_dog)


@dp.message(StateFilter(FSMFillForm.create_dog))
async def process_dog_data(message: Message, state: FSMContext):
    # Обрабатываем данные, введенные пользователем. Отрабатываем возможные ошибки ввода
    dog_data = message.text.split(',')
    if len(dog_data) != 3:
        await bot.send_message(message.from_user.id, "Пожалуйста, введите данные в формате: имя, pk (идентификатор), вид - или начните сначала через /start")
        return
    try:
        dog = {"name": dog_data[0].strip(), "pk": int(dog_data[1]), "kind": dog_data[2].strip()}
    except ValueError:
        await bot.send_message(message.from_user.id, "PK должен быть числом. Пожалуйста, введите данные снова или начните сначала через /start")
        return

    async with ClientSession() as session:
        # Отправляем запрос POST к API
        async with session.post(f'{API_URL}/dog', json=dog) as response:
            data = await response.text()
            try:
                data = json.loads(data)
                if 'detail' in data:
                    if isinstance(data['detail'], list):
                        data = 'Ошибка ввода: ' + ', '.join([error['msg'] for error in data['detail']])
                    else:
                        data = 'К сожалению, собака с таким PK (идентификатором) уже существует. Введите другой PK или начните сначала через /start'
                    await bot.send_message(message.from_user.id, str(data))
                else:
                    await bot.send_message(message.from_user.id, "Вы добавили новую собаку: " + str(data))
                    await state.clear()
            except json.JSONDecodeError:
                pass


@dp.callback_query(F.data == 'UPDATE_DOG')
async def process_update_dog(callback_query: CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите PK собаки и новые данные о собаке в формате: pk, имя, вид")
    await state.set_state(FSMFillForm.update_dog)


@dp.message(StateFilter(FSMFillForm.update_dog))
async def process_update_dog_data(message: Message, state: FSMContext):
    # Обрабатываем данные, введенные пользователем. Отрабатываем возможные ошибки ввода
    dog_data = message.text.split(',')
    if len(dog_data) != 3:
        await bot.send_message(message.from_user.id, "Пожалуйста, введите данные в формате: pk, имя, вид - или начните сначала через /start")
        return
    try:
        pk = int(dog_data[0])
    except ValueError:
        await bot.send_message(message.from_user.id, "PK должен быть числом. Пожалуйста, введите данные снова или начните сначала через /start")
        return
    dog = {"name": dog_data[1].strip(), "pk": pk, "kind": dog_data[2].strip()}

    async with ClientSession() as session:
        # Отправляем запрос PATCH к API
        async with session.patch(f'{API_URL}/dog/{pk}', json=dog) as response:
            data = await response.text()
            try:
                data = json.loads(data)
                if 'detail' in data:
                    if isinstance(data['detail'], list):
                        data = 'Ошибка ввода: ' + ', '.join([error['msg'] for error in data['detail']])
                    else:
                        data = 'К сожалению, собака с таким PK (идентификатором) уже существует. Введите другой PK или начните сначала через /start'
                    await bot.send_message(message.from_user.id, str(data))
                else:
                    await bot.send_message(message.from_user.id, "Вы обновили данные собаки: " + str(data))
                    await state.clear()
            except json.JSONDecodeError:
                pass


@dp.callback_query(F.data == 'GET_DOG_BY_PK')
async def process_get_dog_by_pk(callback_query: CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите PK собаки")
    await state.set_state(FSMFillForm.get_dog_by_pk)


@dp.message(StateFilter(FSMFillForm.get_dog_by_pk))
async def process_get_dog_by_pk_data(message: Message, state: FSMContext):
    # Обрабатываем данные, введенные пользователем
    try:
        pk = int(message.text)
    except ValueError:
        await bot.send_message(message.from_user.id, "PK должен быть числом. Пожалуйста, введите данные снова или начните сначала через /start")
        return

    async with ClientSession() as session:
        # Отправляем запрос GET к API
        async with session.get(f'{API_URL}/dog/{pk}') as response:
            data = await response.text()
            try:
                data = json.loads(data)
                if 'detail' in data:
                    if data['detail'] == 'Dog not found':
                        data = 'К сожалению, собака с таким PK (идентификатором) не найдена.'
                    else:
                        data = 'Ошибка ввода: ' + data['detail']
                    await bot.send_message(message.from_user.id, str(data))
                else:
                    await bot.send_message(message.from_user.id, "Информация о собаке: " + str(data))
                    await state.clear()
            except json.JSONDecodeError:
                pass


# остальные функции, не требующие ввода
@dp.callback_query()
async def process_callback(callback_query: CallbackQuery):
    async with ClientSession() as session:
        if callback_query.data == 'GET_ROOT':
            async with session.get(f'{API_URL}/') as response:
                data = await response.text()
                data = json.loads(data)
                message = "\n".join(data)
                await bot.send_message(callback_query.from_user.id, message)
        elif callback_query.data == 'POST_POST':
            async with session.post(f'{API_URL}/post') as response:
                data = await response.text()
                data = json.loads(data)
                message = "\n".join([f"ID: {item['id']}, Timestamp: {item['timestamp']}" for item in data])
                await bot.send_message(callback_query.from_user.id, message)
        elif callback_query.data == 'GET_DOGS':
            async with session.get(f'{API_URL}/dog') as response:
                data = await response.text()
                data = json.loads(data)
                message = "\n".join([f"Имя: {item['name']}, PK: {item['pk']}, Вид: {item['kind']}" for item in data])
                await bot.send_message(callback_query.from_user.id, message)

    await bot.answer_callback_query(callback_query.id)


# обработка "пустых" сообщений
@dp.message()
async def send_to_menu(message: Message):
    await message.answer('К сожалению, такой функции нет. Нажмите /start, чтобы вернуться к кнопкам-действиям.')


if __name__ == '__main__':
    dp.run_polling(bot)
