from aiogram import Bot, Dispatcher, types, Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, InputFile
from database import Database
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters import Command
import json
import random
import datetime
from aiogram.types import KeyboardButton
import asyncio
import logging
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from data.markup import Markup_konkurs


print("бот запущен [+]")



logging.basicConfig(level=logging.INFO)



bot = Bot(token="6755841005:AAF8A6JxjhxwMaHo0Kq02ApRWO7iEn3dwjg")
dp = Dispatcher(storage=MemoryStorage(), bot=bot)




router = Router()
#id админа



admin_id = 1679659889





dp.include_router(router=router)




db = Database("data.db")




class AwaitMessages(StatesGroup):
    name_state = State()
    tickets_state = State()
    wintickets_state = State()
    photo_state = State()
    markup_konkurs = State()
    add_name = State()

class Awaitkonkurs(StatesGroup):
    add_name = State()

def generate_win_num(num, win_num):
    sp = [i for i in range(1, num)]

    win = []

    for i in range(win_num):
        ww = random.choice(sp)
        win.append(ww)
        sp.remove(ww)

    return win


def add_konkurs(name, num, win_num, photo):

    with open("data/data.json", "r", encoding="UTF-8") as file:
        data = json.load(file)

        win = generate_win_num(num, win_num)
        wolodya = []
        for i in range(1, num):

            if i in win:
                wolodya.append({
                    int(i): "win"
                })

            else:
                wolodya.append({
                    i: "lose"
                })

        data[name] = {
            "Название": name,
            "Билеты": wolodya,
            "Номера": num,
            "фото": photo
        }

    with open("data/data.json", "w+", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False)


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    if message.chat.id == admin_id:
        main_menu = types.ReplyKeyboardMarkup(
            keyboard=[

                [types.KeyboardButton(text="Профиль")],

                [types.KeyboardButton(text="Конкурсы")],

                [types.KeyboardButton(text="Админочка")]

            ]
        )
        await message.answer("Привет, ты админ", reply_markup=main_menu)

    else:
        menu = types.ReplyKeyboardMarkup(
            kb=[

                [types.KeyboardButton(text="Профиль")],

                [types.KeyboardButton(text="Конкурсы")]

            ]
        )
        await message.answer(f"Привет, если ты хочешь поучаствовать в конкурсах, то нажми на кнопку ниже, если хочешь посмотреть свой профиль, то нажми на кнопку профиль", reply_markup = menu)


@router.message(F.text == "Конкурсы")
async def konkurss(message: types.Message, state: FSMContext):
    competition_data = Database.get_konkurs()  
    if competition_data:
        markup = Markup_konkurs.get_markup()  
        await message.answer("Конкурсы:", reply_markup=markup)
    else:
        await message.answer(f"В данный момент конкурсов нет")



@router.callback_query(F.data == "⚡️ LIT ENERGY")
async def apply_konkurs(call: types.CallbackQuery, state: FSMContext):
    verification = types.InlineKeyboardMarkup(
        inline_keyboard=[
                [types.InlineKeyboardButton(text="✅Да", callback_data="yes_konkurs_verif"), types.InlineKeyboardButton(text="❌Нет", callback_data="no_konkurs_verif")]             
            ]
        )
    await call.message.edit_text("Вы хотите принять участие в конкурсе?", reply_markup=verification)

@router.callback_query(F.data == "yes_konkurs_verif")
async def konkurs_verif(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Вы принимаете участие в конкурсе")

@router.callback_query(F.data == "no_konkurs_verif")
async def konkurs_verif(call: types.CallbackQuery, state: FSMContext):
    competition_data = Database.get_konkurs()  
    if competition_data:
        markup = Markup_konkurs.get_markup()  
        await call.message.edit_text("Конкурсы:", reply_markup=markup)
    else:
        await call.message.edit_text("В данный момент конкурсов нет")

    





@router.message(F.text == "Админочка")
async def adminochka(message: types.Message, state: FSMContext):
    if message.chat.id == admin_id:
        admin = types.ReplyKeyboardMarkup(
            keyboard=[

                [types.KeyboardButton(text="Добавить конкурс")],

                [types.KeyboardButton(text="Назад<-")]
            ]
        )
        await message.answer("Вы в админ панельке", reply_markup=admin)


@router.message(F.text == "Назад<-")
async def back(message: types.Message, state: FSMContext):
    if message.chat.id == admin_id:
        all_back = types.ReplyKeyboardMarkup(
            keyboard=[

                [types.KeyboardButton(text="Профиль")],

                [types.KeyboardButton(text="Конкурсы")],

                [types.KeyboardButton(text="Админочка")]
            ]
        )
        await message.answer("Привет, ты админ", reply_markup=all_back)

    else:
        do_not_back = types.ReplyKeyboardMarkup(
            keyboard = [
                [types.KeyboardButton(text="Профиль")],

                [types.KeyboardButton(text="Конкурсы")]

            ]
        )
        await message.answer(f"Привет, если ты хочешь поучаствовать в конкурсах, то нажми на кнопку ниже, если хочешь посмотреть свой профиль, то нажми на кнопку профиль", reply_markup=do_not_back)




@router.message(F.text == "Профиль")
async def send_welcome(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = db.get_user(telegram_id)

    if user is None:
        registration_date = datetime.datetime.now().strftime("%Y-%m-%d")
        db.add_user(telegram_id, registration_date)
        user = db.get_user(telegram_id)

    user_id = user[0]
    registration_date = user[2]

    await message.answer(f"Мой профиль\n\n"
                         f"Дата регистрации: {registration_date}\n"
                         f"Внутренний ID: {user_id}")
    





@router.message(F.text == "Добавить конкурс")
async def state_name(message: types.Message, state: FSMContext):
    await message.answer("Введите название конкурса")
    await state.set_state(AwaitMessages.name_state)





@router.message(AwaitMessages.name_state)
async def process_name(message: types.Message, state: FSMContext):
    Database.add_konkurs(message.text)
    await state.update_data(name=message.text)
    await message.answer("Введите количество билетов")
    await state.set_state(AwaitMessages.tickets_state)




@router.message(AwaitMessages.tickets_state)
async def process_tickets(message: types.Message, state: FSMContext):
    await state.update_data(tickets=int(message.text))
    await message.answer("Введите количество победных билетов")
    await state.set_state(AwaitMessages.wintickets_state)

@router.message(AwaitMessages.tickets_state)
async def process_tickets(message: types.Message, state: FSMContext):
    await state.update_data(tickets=int(message.text))
    await message.answer("Введите количество победных билетов")
    await state.set_state(AwaitMessages.wintickets_state)


@router.message(AwaitMessages.wintickets_state)
async def process_wintickets(message: types.Message, state: FSMContext):
    await state.update_data(wintickets=int(message.text))
    data = await state.get_data()
    add_konkurs(name=data['name'], num=data['tickets'], win_num=data['wintickets'], photo="any")
    await message.answer("Конкурс создан")
    await state.clear()










  
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



