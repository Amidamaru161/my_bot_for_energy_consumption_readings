

from myfunc import *

import telebot 
from telebot import types

client = connect_mqtt()
subscribe(client)

bot=telebot.TeleBot(TOKEN)

#@bot.message_handler(commands=['start'])#Запуск брокера 
#def connect (message):
   # msg="Подключено к брокеру"
    #bot.send_message(message.chat.id,str(msg),parse_mode='html')
    #client.loop_forever()
 
 
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💡 Узнать последнии показания ")
    btn2 = types.KeyboardButton("📈 Посмотреть график")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для дипломной работы".format(message.from_user), reply_markup=markup)
    client.loop_forever()
#@bot.message_handler(commands=['publish'])
#def get_data(message):
    #publish(client)


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "💡 Узнать последнии показания"):
        db=sqlite3.connect('bbg.db')
        with db:
            c=db.cursor()
            c.execute("SELECT * FROM data")
            rows=c.fetchall()
        bot.send_message(message.chat.id, text=f"Показания {rows[-1]}!)")
        db.close()
    elif(message.text == "📈 Посмотреть график"):
        img = open('saved_figure-100dpi.PNG', 'rb')
        bot.send_photo(message.chat.id, img)
        

#@bot.message_handler(commands=['test'])
#def return_data(message):
 #   db=sqlite3.connect('bbg.db')
    
 #   with db:
  #      c=db.cursor()
   #     c.execute("SELECT * FROM data")
        #rows=c.fetchall()
   # msg=f'Показания {rows[-1]}'
   # bot.send_message(message.chat.id,str(msg),parse_mode='html')
    #db.commit()
  #  db.close()

bot.polling(none_stop=True)