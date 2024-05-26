import telebot
from telebot import types

from groq import Groq

client = Groq(api_key="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")
bot = telebot.TeleBot("6900169476:AAFVoE53s6xPBBFE9jy_w5cnxxqMTh_cV3g")
messages = []
stop_flag = False
    
@ bot.message_handler(commands=['test'])
def test(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("На сайт rbc", url = "https://www.rbc.ru"))
    bot.send_message(message.chat.id, message, reply_markup=markup)
    
@ bot.message_handler(commands=['stop'])
def stopbot(message):
    #markup = types.InlineKeyboardMarkup()
    #markup.add(types.InlineKeyboardButton("На сайт rbc", url = "https://www.rbc.ru"))
    #bot.send_message(message.chat.id, message)

    forget(message)
    global stop_flag  # Объявляем stop_flag как глобальную переменную
    bot.reply_to(message, "Бот остановлен")
    stop_flag = True
    bot.stop_polling()


@ bot.message_handler(commands=['forget'])
def forget(message):
    global messages
    messages=[]
    bot.reply_to(message, "Беседа забыта")
    

@ bot.message_handler(commands=['help'])
def helpfunc(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop = types.KeyboardButton("/stop")
    forget = types.KeyboardButton("/forget")
    test = types.KeyboardButton("/test")
    help1 = types.KeyboardButton("/help")

    
    markup.add(forget,stop,test,help1)
    #bot.send_message(message.chat.id, "Помощь", reply_markup=markup)
    bot.send_message(chat_id=message.chat.id, text="Выберите команду:", reply_markup=markup)
    
@ bot.message_handler(content_types=['text'])
def get_text_messages(message):
    #print(type(message))
    print(f"user ({ message.from_user.username }): {message.text}")
    #print(f"user: {message}")
    global messages
    messages.append({"role": 'user', "content": message.text})
    if len(messages) > 20:
        messages = messages[-20:]
    response = client.chat.completions.create(model='llama3-70b-8192', messages=messages, temperature=0)
    bot.send_message(message.from_user.id, response.choices[0].message.content)
    messages.append({"role": 'assistant', "content": response.choices[0].message.content})
    print(f"answer: {response.choices[0].message.content}")    
        
    
    
# можно так, без цикла, через stop_polling() но keyinterrupt не будет работать
#     bot.polling(none_stop=True, interval=0, timeout=0)
    
while not stop_flag:
    try:
        bot.polling(none_stop=False, interval=0, timeout=0)
    except Exception as e:
        print(e)
        time.sleep(15)    
    
