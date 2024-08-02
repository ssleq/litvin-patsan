from aiogram import types
from database import Database


class Markup_konkurs:
    def get_markup():
        competition_data = Database.get_konkurs()
        if not competition_data:  
            return None  
        verification = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text=i[0], callback_data=i[0])]
                for i in competition_data
            ]
        )
        return verification