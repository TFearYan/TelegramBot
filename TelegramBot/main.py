import telebot
from telebot import types

bot = telebot.TeleBot('5433971032:AAF_tv31AoNj89KT8ZG8Eq_-dVbnaijS3v0')
description = ''
price = 0
user_description = False
adress = ''


@bot.message_handler(content_types=['text'])
def beginning(message):
    if message.text != 'Меню' and message.text != 'Сделать заказ':
        hello_user = 'Здравствуй , '
        if message.from_user.last_name is None:
            hello_user += f'{message.from_user.first_name}'
        else:
            hello_user += f'{message.from_user.first_name}{message.from_user.last_name}'
        bot.send_message(chat_id=message.chat.id, text=hello_user)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton('Меню')
    order_b = types.KeyboardButton('Сделать заказ')
    keyboard.add(menu_button, order_b)
    bot.send_message(chat_id=message.chat.id, text='Пожалуйста,выберите действие и нажите на кнопку!',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, choose)


def choose(message):
    if message.text == 'Меню':
        products(message)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes = types.KeyboardButton('Да')
        no = types.KeyboardButton('Нет')
        keyboard.add(yes, no)
        bot.send_message(chat_id=message.chat.id, text='Хотите сделать заказ?!',
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, agree)
    elif message.text == 'Сделать заказ':
        products(message, order=True)
    else:
        bot.send_message(chat_id=message.chat.id, text='Пожалуйста,нажите на кнопку!')


def agree(message):
    if message.text == 'Нет':
        delete = types.ReplyKeyboardRemove()
        bot.send_message(chat_id=message.chat.id, text='До свидания',
                         reply_markup=delete)
    elif message.text == 'Да':
        delete = types.ReplyKeyboardRemove()
        bot.send_message(chat_id=message.chat.id, text='Пожалуйста,выберите продукт!',
                         reply_markup=delete)
        products(message, order=True)


def products(message, order=False):
    adresses = ['Photos of pizza/Margarita.jpg', 'Photos of pizza/Mozzarella.jpg', 'Photos of pizza/Rancho.png']
    messages = ['Mаргарита 1000 р \nСостав:...', 'Mоцарелла 1200 р \nСостав:...', 'Ранчо 1500 р \nСостав:...']
    names_inline_buttons = [['2 Кусочка пиццы (330 p)', '4 Кусочка пиццы (600 p)', 'Целая пицца (1000 p)'],
                            ['2 Кусочка пиццы (400 p)', '4 Кусочка пиццы (700 p)', 'Целая пицца (1200 p)'],
                            ['2 Кусочка пиццы (550 p)', '4 Кусочка пиццы (900 p)', 'Целая пицца (1500 p)']]
    callback_inline_buttons = {
        0: [['2 Кусочка "Маргариты"', '330'], ['4 Кусочка "Маргариты"', '600'],
            ['Пицца "Маргарита"', '1000']],
        1: [['2 Кусочка "Mоцареллы"', '400'], ['4 Кусочка "Mоцареллы"', '700'],
            ['Пицца "Mоцарелла"', '1200']],
        2: [['2 Кусочка "Ранчо"', '550'], ['4 Кусочка "Ранчо"', '900'], ['Пицца "Ранчо"', '1500']]}
    id_element = 0
    if order is False:
        for adress in adresses:
            photo = open(adress, 'rb')
            bot.send_photo(chat_id=message.chat.id, photo=photo)
            bot.send_message(chat_id=message.chat.id, text=messages[id_element])
            id_element += 1
    else:
        for adress in adresses:
            photo = open(adress, 'rb')
            delete = types.ReplyKeyboardRemove()
            bot.send_photo(chat_id=message.chat.id, photo=photo, reply_markup=delete)
            keyboard = types.InlineKeyboardMarkup()
            twoparts_button = types.InlineKeyboardButton(text=names_inline_buttons[id_element][0],
                                                         callback_data=str(callback_inline_buttons[id_element][0]))
            fourparts_button = types.InlineKeyboardButton(text=names_inline_buttons[id_element][1],
                                                          callback_data=str(callback_inline_buttons[id_element][1]))
            pizza_button = types.InlineKeyboardButton(text=names_inline_buttons[id_element][2],
                                                      callback_data=str(callback_inline_buttons[id_element][2]))
            keyboard.add(twoparts_button)
            keyboard.add(fourparts_button)
            keyboard.add(pizza_button)
            bot.send_message(chat_id=message.chat.id, text=messages[id_element], reply_markup=keyboard)
            id_element += 1
    bot.register_next_step_handler(message, after_products)


def after_products(message):
    global description
    delete = types.ReplyKeyboardRemove()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pickup_button = types.KeyboardButton('Самовывоз')
    keyboard.add(pickup_button)
    if message.text == f'Оформить заказ (Цена : {str(price)})':
        bot.send_message(chat_id=message.chat.id, text='Напишите адрес или выберите самовывоз!', reply_markup=delete)
        bot.send_message(chat_id=message.chat.id,
                         text='Адрес пишите следующим форматом:\nПоселок\nУлица\nДом\n<b><u>Адрес напишите одним сообщением!!!!</u></b>',
                         reply_markup=keyboard, parse_mode='HTML')
        bot.register_next_step_handler(message, check_order)
    elif message.text == 'Написать заказ самому':
        bot.send_message(chat_id=message.chat.id,
                         text='Напишите заказ следующим форматом\nНазвание-количество\n<b><u>Заказ напишите одним сообщением!!!!</u></b>',
                         reply_markup=delete, parse_mode='HTML')
        description = ''
        bot.register_next_step_handler(message, description_user)
        return description
    '''elif message.text == 'Убрать пункт':
            word = ''''''
            for char in range(len(description) - 1, -1, -1):
                word += description[char]
                if char == "'" and description[char] != -1:
                    break
            description -= word
            bot.send_message(chat_id=message.chat.id, text=description, reply_markup=delete)
            bot.register_next_step_handler(message, products)
            return description'''


def description_user(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pickup_button = types.KeyboardButton('Самовывоз')
    keyboard.add(pickup_button)
    global description, user_description
    if message.text != '':
        description = message.text
        bot.send_message(chat_id=message.chat.id,
                         text='Адрес пишите следующим форматом:\nПоселок\nУлица\nДом\n<b><u>Адрес напишите одним сообщением!!!!</u></b>',
                         reply_markup=keyboard, parse_mode='HTML')
        user_description = True
        bot.register_next_step_handler(message, check_order)


def check_order(message):
    global user_description, adress, description, price
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    delete = types.ReplyKeyboardRemove()
    yes_button = types.KeyboardButton('Да')
    no_button = types.KeyboardButton('Нет')
    adress = message.text
    keyboard.add(yes_button, no_button)
    bot.send_message(chat_id=message.chat.id, text=f'Адрес оформлен!\n{adress}', reply_markup=delete)
    if user_description is False:
        bot.send_message(chat_id=message.chat.id, text=f'{description}\nЦена: {str(price)}\nАдрес: {adress}',
                         reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text=f'{description}\nАдрес: {adress}',
                         reply_markup=keyboard)
    bot.send_message(chat_id=message.chat.id, text='Заказ верен?')
    bot.register_next_step_handler(message, wait_order)
    return adress, description, price


def wait_order(message):
    delete = types.ReplyKeyboardRemove()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_button = types.KeyboardButton('Изменить заказ')
    cancelorder_button = types.KeyboardButton('Отменить заказ')
    keyboard.add(change_button, cancelorder_button)
    global description, price
    if message.text == 'Да':
        bot.send_message(chat_id=message.chat.id,
                         text='Заказ отправлен на готовку!\nКак только заказ приготовиться вам придет сообщение!',
                         reply_markup=delete)
        bot.send_message(chat_id=1076070842,
                         text=f'{description}\nЦена: {price}\n{adress}\n<a href="tg://user?id={message.from_user.id}">Чат с пользователем</a>',
                         parse_mode='HTML')
    elif message.text == 'Нет':
        bot.send_message(chat_id=message.chat.id, text='Выберите действие!', reply_markup=keyboard)
        bot.register_next_step_handler(message, change_order2)
    description = ''
    price = 0
    return description, price


def change_order2(message):
    delete = types.ReplyKeyboardRemove()
    adresses = ['Photos of pizza/Margarita.jpg', 'Photos of pizza/Mozzarella.jpg', 'Photos of pizza/Rancho.png']
    messages = ['Mаргарита 1000 р \nСостав:...', 'Mоцарелла 1200 р \nСостав:...', 'Ранчо 1500 р \nСостав:...']
    names_inline_buttons = [['2 Кусочка пиццы \n(330 p)', '4 Кусочка пиццы \n(600 p)', 'Целая пицца \n(1000 p)'],
                            ['2 Кусочка пиццы \n(400 p)', '4 Кусочка пиццы \n(700 p)', 'Целая пицца \n(1200 p)'],
                            ['2 Кусочка пиццы \n(550 p)', '4 Кусочка пиццы \n(900 p)', 'Целая пицца \n(1500 p)']]
    callback_inline_buttons = {
        0: [['2 Кусочка "Маргариты"', '330'], ['4 Кусочка "Маргариты"', '600'],
            ['Пицца "Маргарита"', '1000']],
        1: [['2 Кусочка "Mоцареллы"', '400'], ['4 Кусочка "Mоцареллы"', '700'],
            ['Пицца "Mоцарелла"', '1200']],
        2: [['2 Кусочка "Ранчо"', '550'], ['4 Кусочка "Ранчо"', '900'], ['Пицца "Ранчо"', '1500']]}
    id_element = 0
    if message.text == 'Изменить заказ':
        for adress in adresses:
            photo = open(adress, 'rb')
            delete = types.ReplyKeyboardRemove()
            bot.send_photo(chat_id=message.chat.id, photo=photo, reply_markup=delete)
            keyboard = types.InlineKeyboardMarkup()
            twoparts_button = types.InlineKeyboardButton(text=names_inline_buttons[id_element][0],
                                                         callback_data=str(callback_inline_buttons[id_element][0]))
            fourparts_button = types.InlineKeyboardButton(text=names_inline_buttons[id_element][1],
                                                          callback_data=str(callback_inline_buttons[id_element][1]))
            pizza_button = types.InlineKeyboardButton(text=names_inline_buttons[id_element][2],
                                                      callback_data=str(callback_inline_buttons[id_element][2]))
            keyboard.add(twoparts_button)
            keyboard.add(fourparts_button)
            keyboard.add(pizza_button)
            bot.send_message(chat_id=message.chat.id, text=messages[id_element], reply_markup=keyboard)
            id_element += 1
        bot.send_message(message.chat.id, text='Выберите еду!', reply_markup=delete)
        bot.register_next_step_handler(message, after_products)
    elif message.text == 'Отменить заказ':
        bot.send_message(chat_id=message.chat.id, text='До свидания!', reply_markup=delete)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global description, price
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    price += int(call.data[call.data.find(',') + 3: -2])
    description += call.data[1:call.data.find(',')] + '\n'
    ready_button = types.KeyboardButton(f'Оформить заказ (Цена : {str(price)})')
    user_button = types.KeyboardButton('Написать заказ самому')
    keyboard.add(user_button)
    keyboard.add(ready_button)
    bot.send_message(chat_id=call.message.chat.id, text=description, reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=call.id)
    return description, price


bot.polling(none_stop=True)
