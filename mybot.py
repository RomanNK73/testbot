import telebot
from groq import Groq

client = Groq(api_key="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")
bot = telebot.TeleBot("6900169476:AAFVoE53s6xPBBFE9jy_w5cnxxqMTh_cV3g")
messages = []
stop_flag = False

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
    if message.text == 'exit':
        stop_flag = True    
        print()
        
while not stop_flag:
    bot.polling(none_stop=True, interval=0, timeout=0)
