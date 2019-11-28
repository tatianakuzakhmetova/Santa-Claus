# pip install python-telegram-bot[socks]

'''
Привет! Как я понял ты учишься писать ботов. А можешь/хочешь написать бота для розыгрыша анонимного деда мороза? 

Принимает email'ы или telegram аккаунты
По кнопке распределяет внучков так, чтобы никто не попал сам к себе, и высылает сообщение.

чуть сложнее:
Бот добавляется в чат. По некоторой команде распределяет внучнов из участников чата (главное отбросить всех ботов) 
и пишет им личное сообщение с ником его внучка.
'''


'''
2 способа внести пользователя в user_data dictionary:
    1. Если бот получает событие, по которому нового пользователя добавляют в группу
    (тут надо тогда обрабатывать событие, когда пользователя уходит из группы
    2. Если пользователь уже был добавлен в группу до того, как там появился Бот
    (в этом случае должна быть какая-то команда, которая добавляет пользователя в группу)
    * Проверка, что в словаре user_data не будет существовать 2х одинаковых пользователей (с одинаковым id)

В словарь user_data вставляем Логику подкидывания АДМ

3 способа удалить пользователя из словаря:
    1. Он уходит по доброй воле
    2. Его удаляет Администратор (например, это Спам-аккаунт)
    3. Это бот, поэтому его удаляем автоматически

'''

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
import settings
import logging

import random


# Reply keyboard, Получение геолокации и контактных данных пользователя
from telegram import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

# Создаем глобальный слопарик с Пользовательской информацией.
# Что делать, выбора нет! В политике Телеграмма - нет возможности сохранять данные от пользователя дольше,
# чем случится следующее Update-событие (пришел/покинул группу новый член, кто-то написал сообщение или послал команду)
# Пряча ключ API бота, мы гарантируем безопасность и сохранность полученных пользовательских данных. 
all_user_data = dict()
 
#Тело бота
#A dict that can be used to keep any data in. For each update from the same user it will be the same dict.
def main():
    mybot = Updater(settings.API, request_kwargs = settings.PROXY)    
    
    logging.info('Bot start')
    
    # This class dispatches all kinds of updates to its registered handlers.
    dp = mybot.dispatcher
    
    # Важно! Ставьте CommandHandler выше MessageHandler, тк он перехватит команды
    # The case if the user is already in chat group, use the command '/adm'
    dp.add_handler(CommandHandler("adm", want_adm, pass_user_data=True))
    dp.add_handler(CommandHandler("stop", stop, pass_user_data=True))
    
    # Chat text message 
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    # Starts polling updates from Telegram.
    mybot.start_polling()
    # Blocks until one of the signals are received and stops the updater.
    mybot.idle()


def talk_to_me(bot, update, user_data):
    if update.message.chat.type == 'group':
        value = update.message.from_user.id
        key = update.message.from_user.first_name
        logging.info("The User: %s with User_id: %s wrote in Chat_id: %s,", value, key, update.message.chat.id)
        if value not in all_user_data.values():
            all_user_data[key] = value
            user_text = "Hey, {}! Looks like you are newbie! Have you already done /adm command?".format(key)
        else:      
            user_text = "Hi, {}! We are familiar! Are you in /adm group?".format(key)
        
        update.message.reply_text(user_text)

    
    
def want_adm(bot, update, user_data):
    key = update.message.from_user.first_name
    value = update.message.from_user.id
    
    if value not in all_user_data.values():
        all_user_data[key] = value
        logging.info("The User: %s is the first in all_user_data dict", key)
    else:
        logging.info("The User: %s is already in all_user_data dict", key)
  
    print (all_user_data)
    
    #Check Group chat member count. If some of them hadn't type /adm command, ask them to choose smth
    chat_members = bot.get_chat_members_count(update.message.chat.id)
    print(chat_members)
    #One of chat_member is the Santa-Claus bot
    if (chat_members-1) > len(all_user_data):
        bot.send_message(update.message.chat.id, "Who didn't choose /adm command yet?")
    elif (chat_members-1) == len(all_user_data):
        create_adm_dict()
   

def stop(bot, update, user_data):
    all_user_data.clear()
    print(all_user_data)


def create_adm_dict():
    #Random choice for ADM
    #Working with all_user_data dictionary with {User_Name: User_ID}
    adm_base = {}
    nicks = []
    for nick in all_user_data.keys():
        nicks.append(nick)
        print(nicks)
    while len(adm_base) != len(nicks):
        from_msg = random.choice(nicks)
        to_msg = random.choice(nicks)
        #Verify if from_user == to_user
        if to_msg == from_msg:
            print("Wrong situation! We can't send the message to ourselves'")
            continue
        # Verify if from_useralready has the to_user
        if adm_base.get(from_msg):
            print("Ookey! This user already is ADM!")
            continue
        adm_base[from_msg] = to_msg
        
    print(adm_base)
    
    
    
#    button_adm = KeyboardButton('Want ADM!')
#    button_leave = KeyboardButton('Want to Leave!')
#    member_kb = ReplyKeyboardMarkup([
#                                    [button_adm],[button_leave]
#                                    ], resize_keyboard=True
#                                    )
#    update.message.reply_text('Hello everyones! Please, choose!', reply_markup=member_kb)

 #   try:
 #       bot.send_message(update.message.from_user.id, "You wrote smth?")
 #   except(Unauthorized):
 #       print("Santa-Claus bot was blocked by the user: %s %s" %(update.message.from_user.first_name, update.message.from_user.last_name))
        





# Два подчеркивания (__) - системная переменная Питона
# Эта конструкция позволяет импортировать функции как методы в других файлах
# Если файл вызвали напрямую, выполняй функцию main()
if __name__ == "__main__":
    main()
  

