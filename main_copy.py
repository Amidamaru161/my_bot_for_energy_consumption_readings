

from myfunc import *
import telebot 
from telebot import types
from threading import *

def readmqtt():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
def startbot():
    bot.polling(none_stop=True)
    
t1=Thread(target=readmqtt)
t2=Thread(target=startbot)
bot=telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💡 Узнать последнии показания ")
    btn2 = types.KeyboardButton("📈 Посмотреть график")
    btn3 = types.KeyboardButton("💾 Получить файл базы данных")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для дипломной работы".format(message.from_user), reply_markup=markup)
    


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "💡 Узнать последнии показания"):
        db=sqlite3.connect('bbg.db')
        with db:
            c=db.cursor()
            c.execute("SELECT * FROM data")
            rows=c.fetchall()
        array_data=rows[-1]
        bot.send_message(message.chat.id, text=f"ID:{array_data[0]},Общее потребление:{array_data[1]},Дата:{array_data[5]})")
        db.close()
    elif(message.text == "📈 Посмотреть график"):
        plotting()
        img = open('saved_figure-100dpi.PNG', 'rb')
        bot.send_photo(message.chat.id, img)
    elif(message.text == "💾 Получить файл базы данных"):
        file=open('bbg.db','rb')
        bot.send_document(message.chat.id,file)
if __name__=='__main__':
    t1.start()
    t2.start()
    
    