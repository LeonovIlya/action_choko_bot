from aiogram import Dispatcher, types

from utils import keyboards


async def some_function(message: types.Message):
    await message.answer(text='Данная функция в разработке',
                         reply_markup=keyboards.main_menu)


def register_handlers_best_practice(dp: Dispatcher):
    dp.register_message_handler(some_function,
                                text='Инструменты🛠',
                                state='*')
