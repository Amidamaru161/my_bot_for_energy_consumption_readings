import time
import datetime
import matplotlib.pyplot as plt 
import sqlite3
from paho.mqtt import client as mqtt_client
import random

broker = "m6.wqtt.ru"
port = 11252
topic = "/datchik"
topic1 = "receive/123"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'u_DIWHF1'
password = 'povIvsFt'
TOKEN='5357368336:AAErqK9xbUeM4G4y5IdQudLIzRmqtmxZpII'

def plot (x,y):
    
    plt.figure(figsize=(15, 15))
    plt.plot(x, y, 'o-r', alpha=0.7, label="first", lw=5, mec='b', mew=0, ms=10)
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.savefig('saved_figure-100dpi.png', dpi = 100) 

def create_data(string_data):
  db=sqlite3.connect('bbg.db')
  cursor=db.cursor()   
  choose_str=str(string_data)#Преобразование в нужный тип данных 
  data_list=choose_str.split(",")#Создание массива с разделителем через запятую
  ac = datetime.datetime.now().replace(microsecond=0)
  #EpochSeconds=time.mktime(ac.timetuple())+7200#UTC ВРЕМЯ для калининграда     
  data_list.append(ac)
  sql_request='INSERT INTO data(id,voltage,ampere,power,cosfi,date) VALUES(?,?,?,?,?,?)'
  cursor.execute(sql_request,data_list)#Запись данных в БД РАБОТАЕТ !!!!!!
  db.commit()
  db.close()

def plotting():
  db=sqlite3.connect('bbg.db')
  with db:
      
      c=db.cursor()
      c.execute('SELECT voltage FROM data ')
      voltage_array=c.fetchall()
      c.execute('SELECT date FROM data ')
      date_array=c.fetchall()
  voltage_array2=[x for l in voltage_array for x in l]#преобразование [[1],[2]]=[1,2]
  date_array2=[x for l in date_array for x in l]
  date_time=[datetime.datetime.fromtimestamp(x) for x in date_array2 ]# по идее работает верно 
  str_date_time=[str(x) for x in date_time]  
      
  plot(str_date_time, voltage_array2)
  db.close()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Подключено к брокеру !")
        else:
            print("Ошибка соединеня  %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    
    def on_message(client, userdata, msg):
        message_test=msg.payload.decode()#Получаемое сообщение 
        create_data(message_test)
        print(f"Получено `{message_test}` от `{msg.topic}`")
    client.subscribe(topic)
    client.on_message = on_message
    
