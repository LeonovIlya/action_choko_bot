import re
import aiofiles

from datetime import datetime as dt
from aiopath import AsyncPath
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from loader import db
from utils import decorators, keyboards, queries
from utils.states import UserState

R_STR = r'(^\d{6},)|(\w+\sобл,)|(\w+-\w+\sр-н,)|(\w+\sр-н,)|(\w+\sрн,' \
        r')|(\s№\s)|(\sг,)'

KPI = ('PSS:', 'WOSA:', 'TO:', 'VISITS:', 'ISA-OSA:', 'DP CHOCO:', 'DP GUM:',
       'DMP_MAHS:', 'DMP_AHS:')


async def convert_datetime(value: str):
    return dt.strptime(value, '%Y-%m-%d %H:%M:%S').strftime('%d %B %Y')


async def replace_symbols(text: str) -> str:
    return text.replace('_', '\\_') \
        .replace('.', '\\.') \
        .replace('-', '\\-') \
        .replace('*', '\\*') \
        .replace('@', '\\@') \
        .replace('[', '\\[') \
        .replace(']', '\\]') \
        .replace('~', '\\~') \
        .replace('`', '\\`') \
        .replace('>', '\\>') \
        .replace('#', '\\#') \
        .replace('+', '\\+') \
        .replace('=', '\\=') \
        .replace('|', '\\|') \
        .replace('{', '\\{') \
        .replace('}', '\\}') \
        .replace('(', '\\(') \
        .replace(')', '\\)') \
        .replace('!', '\\!') \
        .replace('&', '\\&')


async def kpi_menu(message: types.Message):
    await message.answer(text='Выберите пункт из меню:',
                         reply_markup=keyboards.kpi_menu)
    await UserState.kpi_menu.set()


# @decorators.error_handler_message
async def kpi_mr(message: types.Message, state: FSMContext):
    query = await db.get_one(
        await queries.get_value(
            value='*',
            table='users'),
        tg_id=int(message.from_user.id))
    up_date = await convert_datetime(query[32])
    await message.answer(
        text=f'```\n'
             f'             план|    факт|результат\n'
             f'{KPI[0]:<4}'
             f'{query[11]:>12.2f}%|{query[12]:>7.2f}%|{query[13]:>8.2%}\n'
             f'{KPI[1]:<4}'
             f'{query[14]:>12.2%}|{query[15]:>8.2%}|{query[16]:>8.2%}\n'
             f'{KPI[2]:<4}'
             f'{query[17]:>13}|{query[18]:>8}|{query[19]:>8.2%}\n'
             f'{KPI[3]:<7}'
             f'{query[20]:>10}|{query[21]:>8}|{query[22]:>8.2%}\n'
             f'{KPI[4]:<7}{query[23]:>27}\n'
             f'{KPI[5]:<4}'
             f'{query[24]:>8.2%}|{query[25]:>8.2%}|{query[26]:>8.2%}\n'
             f'{KPI[6]:<4}'
             f'{query[27]:>10.2%}|{query[28]:>8.2%}|{query[29]:>8.2%}\n'
             f'{KPI[7]:<4}{query[30]:>26}\n'
             f'{KPI[8]:<4}{query[31]:>27}\n'
             f'\n\nАктуальность данных:\n{up_date}```',
        reply_markup=keyboards.back,
        parse_mode='MarkdownV2')


async def kpi_tt(message: types.Message):
    await message.answer(
        text='Введите 5-и значный номер ТТ:',
        reply_markup=keyboards.back)
    await UserState.kpi_search_tt.set()


# "@decorators.error_handler_message
async def kpi_search_tt(message: types.Message, state: FSMContext):
    tt_num = re.sub(r'\s', '', str(message.text))
    if re.match(r'\d{5}', tt_num) and len(tt_num) == 5:
        query = await db.get_one(
            await queries.get_value(
                value='*',
                table='tt'),
            tt_num=tt_num)
        if query:
            n = 0
            for i in query:
                print(n, ')', i, '-', type(i))
                n += 1
            tt_address = await replace_symbols(re.sub(R_STR, '', query[5]))
            mr_name = await replace_symbols(query[6])
            kas_name = await replace_symbols(query[7])
            cm_name = await replace_symbols(query[8])
            up_date = await convert_datetime(query[30])
            await message.answer(
                text=f'*TT №* {tt_num}\n'
                     f'*Сеть:* {query[4]}\n'
                     f'*Адрес:* {tt_address}\n'
                     f'*MR:* {mr_name}\n'
                     f'*KAS:* {kas_name}\n'
                     f'*CM:* {cm_name}\n\n'
                     f'```\n'
                     f'             план|    факт|результат\n'
                     f'{KPI[0]:<4}'
                     f'{query[9]:>12.2f}%|{query[10]:>7.2f}%|'
                     f'{query[11]:>8.2%}\n'
                     f'{KPI[1]:<4}'
                     f'{query[12]:>12.2%}|{query[13]:>8.2%}|'
                     f'{query[14]:>8.2%}\n'
                     f'{KPI[2]:<4}'
                     f'{query[15]:>13}|{query[16]:>8}|'
                     f'{query[17]:>8.2%}\n'
                     f'{KPI[3]:<7}'
                     f'{query[18]:>10}|{query[19]:>8}|'
                     f'{query[20]:>8.2%}\n'
                     f'{KPI[4]:<7}{query[21]:>27}\n'
                     f'{KPI[5]:<4}'
                     f'{query[22]:>8.2%}|{query[23]:>8.2%}|'
                     f'{query[24]:>8.2%}\n'
                     f'{KPI[6]:<4}'
                     f'{query[25]:>10.2%}|{query[26]:>8.2%}|'
                     f'{query[27]:>8.2%}\n'
                     f'{KPI[7]:<4}{query[28]:>26}\n'
                     f'{KPI[8]:<4}{query[29]:>27}\n'
                     f'\n\nАктуальность данных:\n{up_date}```',
                reply_markup=keyboards.back,
                parse_mode='MarkdownV2')
        else:
            await message.answer(
                text='❗ ТТ с таким номером не найдена!\n'
                     'Попробуйте еще раз!',
                reply_markup=keyboards.back)
    else:
        await message.answer(
            text='❗ Номер ТТ не соответствует формату ввода!\n'
                 'Введите еще раз!',
            reply_markup=keyboards.back)


async def get_bonus_info(message: types.Message):
    file_link = './files/kpi/bonus.jpg'
    file = AsyncPath(file_link)
    if await file.is_file():
        await message.answer_chat_action(
            action='upload_document')
        async with aiofiles.open(file, 'rb') as photo:
            await message.answer_photo(
                photo=photo,
                reply_markup=keyboards.back)
    else:
        await message.answer(
            text='Файл не найден!',
            reply_markup=keyboards.back)


def register_handlers_kpi(dp: Dispatcher):
    dp.register_message_handler(
        kpi_menu,
        text='Назад↩',
        state=(UserState.kpi_menu,
               UserState.kpi_search_tt))
    dp.register_message_handler(
        kpi_menu,
        text='KPI📈',
        state=(UserState.auth_mr,
               UserState.auth_kas,
               UserState.auth_cm))
    dp.register_message_handler(
        kpi_mr,
        text='Мой KPI📈',
        state=UserState.kpi_menu)
    dp.register_message_handler(
        kpi_tt,
        text='KPI TT🏬',
        state=UserState.kpi_menu)
    dp.register_message_handler(
        kpi_search_tt,
        state=UserState.kpi_search_tt)
    dp.register_message_handler(
        get_bonus_info,
        text='Информация по бонусу💰',
        state=UserState.kpi_menu)
