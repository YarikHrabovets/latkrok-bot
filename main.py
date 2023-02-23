import os.path

import logging
from aiogram import Bot, Dispatcher, executor, types

from db import *
from markups import *
from utils import logo_media

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

local_storage = []


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    local_storage.clear()
    if not is_user_exist(message.from_user.id):
        add_user(message.from_user.id, message.from_user.username)
        await bot.send_message(message.chat.id, 'Добрий день, <b>{0}</b>!\nЦе офіційний бот Латкрок-Сервіс'.format(
            message.from_user.first_name), reply_markup=main_menu, parse_mode='html')
    else:
        await bot.send_message(message.chat.id, 'Добрий день, <b>{0}</b>!\nРаді бачити Вас знову!'.format(
            message.from_user.first_name), reply_markup=main_menu, parse_mode='html')


@dp.message_handler(content_types=[types.ContentType.TEXT])
async def keyboard(message: types.Message):
    if message.chat.type == 'private':
        local_storage.clear()

        if message.text == '📑 Документи':
            await bot.send_message(message.chat.id, "<b>Документи для укладання договору</b>\n\n<b>По безготівковому рахунку необхідно:</b>\n1) реквізити Вашого підприємства  ( свідоцтво про реєстрацію, ЄДРПОУ, ІПН, свідоцтво ПДВ, якщо є. Юридичний адрес, телефон. розрахунковий рахунок)\n\n<b>По готівковому рахунку:</b>\nПрізвище Ім'я та ідент. код, серія номер паспорта.", parse_mode='html')

        elif message.text in ('💲 Оренда', '🛍 Дивитися товари'):
            for product in get_all_products():
                await bot.send_photo(message.chat.id, product['url'], '<b>{0}</b>\n\n{1}'.format(
                    product['name'], product['description']), parse_mode='html', reply_markup=go_to_item(str(product['id'])))

        elif message.text == '💲 Logo-килими':
            await bot.send_media_group(message.chat.id, logo_media())
            await bot.send_message(message.chat.id, 'Більш детально про <b>Logo-килими</b> можна дізнатися на нашому сайті\n\nhttps://latkrok.in.ua/uk/logo/', parse_mode='html')

        elif message.text == '🚨 Акції':
            await bot.send_message(message.chat.id, '<b>На даний момент немає акцій.</b>\nСлідкуйте за подальшими новинами', parse_mode='html')

        elif message.text == '📞 Контакти':
            await bot.send_message(message.chat.id, '🏢 <b>07400, м.Бровари, бул.Незалежності 26/2</b>\n\n📞  (050) 552-42-92\n\n📞  (063) 316 39 93\n\n📧 roman@latkrok.ua\n\n<b>Є питання? Звертайтеся:</b>\n@Latkrok', parse_mode='html')

        elif message.text == '👥 Про нас':
            await bot.send_message(message.chat.id, "ТОВ «Латкрок-Сервіс» засноване 1996 р. Ми на ринку України понад 14 років. За цей час ми стали стабільними та надійними партнерами для наших клієнтів.\n\nУ зв'язку з реорганізацією компанії в 2008 році було змінено ім'я ТОВ Латкрок на ТОВ Латкрок-Сервіс. Основним видом діяльності підприємства є задоволення потреб населення та підприємств у сфері надання послуг із утримання житлових, офісних та виробничих приміщень у чистому стані.\n\nЗ початку своєї діяльності підприємство розвивається виключно за рахунок власних фінансових та технологічних можливостей, постійно збільшуючи обсяги надання послуг.")

        elif message.text == '👤 Профіль':
            user = get_user(message.from_user.id)
            await bot.send_message(message.chat.id, '''
            <b>Профіль:</b>\nІм'я: <b>{0}</b>\nВаш telegram id: <b>{1}</b>\nДата приєднання: <b>{2}</b>'''.format(
                user['name'], user['user_id'], user['join_date']), reply_markup=profile_menu, parse_mode='html')

        elif message.text == '📔 Мої товари':
            cart = get_user_cart(message.from_user.id)
            if len(cart) != 0:
                await bot.send_message(message.chat.id, '<b>Ваш кошик</b>', parse_mode='html', reply_markup=cart_menu)
                for item in cart:
                    product = get_product(item['product_id'])
                    caption = f"<b>{product['name']}</b>\n\n<b>К-сть обмінів:</b> {item['product_option']}\n\n<b>Колір:</b> {item['color']}\n\n<b>Кількість:</b> {item['quantity']}"
                    await bot.send_photo(message.chat.id, product['url'], caption, parse_mode='html', reply_markup=edit_cart(item['id']))
            else:
                with open(os.path.abspath('src/emptycart.png'), 'rb') as file:
                    await bot.send_photo(message.chat.id, file, '<b>Ваш кошик порожній</b>', parse_mode='html',
                                         reply_markup=empty_cart_menu)

        elif message.text == '🔙 Головне меню':
            await bot.send_message(message.chat.id, '🔙 Головне меню', reply_markup=main_menu)

        elif message.text == '📝 Оформити замовлення':
            cart = get_user_cart(message.from_user.id)
            if len(cart) != 0:
                for item in cart:
                    product = get_product(item['product_id'])
                    caption = f"<b>{product['name']}</b>\n\n<b>К-сть обмінів:</b> {item['product_option']}\n\n<b>Колір:</b> {item['color']}\n\n<b>Кількість:</b> {item['quantity']}\n\n@{message.from_user.username}"
                    await bot.send_photo(GROUP_ID, product['url'], caption, parse_mode='html')

                delete_all_user_product(message.from_user.id)
                await bot.send_message(message.chat.id, "<b>Ми отримали ваше замовлення! Незабаром з Вами зв'яжеться оператор.</b>\n\n<b>Документи для укладання договору, які Ви повинні надіслати оператору.</b>\n\n<b>По безготівковому рахунку необхідно:</b>\n1) реквізити Вашого підприємства  ( свідоцтво про реєстрацію, ЄДРПОУ, ІПН, свідоцтво ПДВ, якщо є. Юридичний адрес, телефон. розрахунковий рахунок)\n\n<b>По готівковому рахунку:</b>\nПрізвище Ім'я та ідент. код, серія номер паспорта.", parse_mode='html')


@dp.callback_query_handler(lambda c: len(c.data) < 3)
async def chose_price(call: types.CallbackQuery):
    local_storage.append(call.data)
    product = get_product(call.data)
    price = get_price(product['price_id'])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_photo(call.message.chat.id, product['url'],
                         '<b>{0}</b>\n\n{1}\n\n<b>Виберіть кількість обмінів:</b>'.format(
                             product['name'], product['description']), parse_mode='html',
                         reply_markup=get_price_markup(price))


@dp.callback_query_handler(lambda c: c.data.split('-')[0].strip() in rent_names)
async def chose_color(call: types.CallbackQuery):
    local_storage.append(call.data)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='<b>Виберіть колір:</b>', parse_mode='html', reply_markup=colors)


@dp.callback_query_handler(lambda c: c.data in ('Сталь', 'Граніт', 'Кедр'))
async def chose_quantity(call: types.CallbackQuery):
    local_storage.append(call.data)
    local_storage.append(1)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption='<b>Виберіть кількість килимів:</b>', parse_mode='html', reply_markup=slider())


@dp.callback_query_handler(lambda c: c.data.split('-')[0] in ('plus', 'minus'))
async def change_quantity(call: types.CallbackQuery):
    data = call.data.split('-')
    try:
        if data[0] == 'plus' and int(data[1]) < 60:
            local_storage[-1] = int(data[1]) + 1
            await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           caption='<b>Виберіть кількість килимів:</b>', parse_mode='html',
                                           reply_markup=slider(int(data[1]) + 1))
        elif data[0] == 'minus' and int(data[1]) > 1:
            local_storage[-1] = int(data[1]) - 1
            await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           caption='<b>Виберіть кількість килимів:</b>', parse_mode='html',
                                           reply_markup=slider(int(data[1]) - 1))
    except IndexError:
        await bot.send_message(call.message.chat.id, '<b>Виникла проблема, будь ласка почніть з початку</b>',
                               parse_mode='html', reply_markup=main_menu)


@dp.callback_query_handler(lambda c: c.data == 'add-to-cart')
async def add_to_cart(call: types.CallbackQuery):
    add_product(call.from_user.id, *local_storage)
    local_storage.clear()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    with open(os.path.abspath('src/success.png'), 'rb') as file:
        await bot.send_photo(call.message.chat.id, file,
                             '<b>Товар успішно доданий до кошику(кошик знаходиться у профілі)</b>',
                             parse_mode='html', reply_markup=main_menu)


@dp.callback_query_handler(lambda c: c.data.split('-')[0] == 'delete')
async def delete_item(call: types.CallbackQuery):
    delete_product(int(call.data.split('-')[1]))
    with open(os.path.abspath('src/success.png'), 'rb') as file:
        await bot.edit_message_media(types.InputMedia(media=file, caption='Успішно видалено!'),
                                     call.message.chat.id, call.message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
