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
 
#Тело бота
#A dict that can be used to keep any data in. For each update from the same user it will be the same dict.
def main():
    mybot = Updater(settings.API, request_kwargs = settings.PROXY, use_context=True)    
    
    logging.info('Bot start')
    
    # This class dispatches all kinds of updates to its registered handlers.
    dp = mybot.dispatcher
    
    # Важно! Ставьте CommandHandler выше MessageHandler, тк он перехватит команды
    # The case if the user is already in chat group, use the command '/adm'
    dp.add_handler(CommandHandler("adm", want_adm, pass_user_data=True))
    
    # Chat text message 
#    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_chat, pass_user_data=True))

    
    # Starts polling updates from Telegram.
    mybot.start_polling()
    # Blocks until one of the signals are received and stops the updater.
    mybot.idle()


def want_adm(update, context):
    key = update.message.from_user.first_name
    value = update.message.from_user.id
    context.user_data[key] = value
    
    if context.user_data:
        logging.info("The User: %s want to play ADM, but He/She is already in", context.user_data)
        update.message.reply_text("Hello, {}. I remember that you want me to send ADM:)". format(context.user_data))
    else:
        logging.info("The User: %s with User_id: %s want to play ADM", key, value)
    
    context_dict(context.user_data)
    

def context_dict(dict):
    print(dict)
    
    
def talk_chat(update, context):
    if context.user_data:
        logging.info("The User: %s was already wrote smth", context.user_data)
        update.message.reply_text("Hello, {}. We are familiar:)". format(context.user_data))
    else:
        key = update.message.from_user.first_name
        value = update.message.from_user.id
        context.user_data[key] = value
        logging.info("The User: %s is the first in here", context.user_data)
        update.message.reply_text("Hello, {}. You are newbie!". format(context.user_data))


def talk_to_me(bot, update, user_data):
    button_adm = KeyboardButton('Want ADM!')
    button_leave = KeyboardButton('Want to Leave!')
    member_kb = ReplyKeyboardMarkup([
                                    [button_adm],[button_leave]
                                    ], resize_keyboard=True
                                    )
    update.message.reply_text('Hello everyones! Please, choose!', reply_markup=member_kb)
#    if update.message.chat.type == 'group':
#        if update.message.chat.title == 'Santa-Clause':
#            print("We are in Santa-Claus Group!")
           #     logging.info("The User: %s with User_id: %s was added to the Chat_id: %s,", update.message.from_user.first_name,  
            #                                                                                update.message.from_user.id, update.message.chat.id)
            #    new_chat_member = message.new_chat_participant.first_name 
            #    print(new_chat_member)
            #    chat_members = bot.get_chat_members_count(update.message.chat.id)
            #    print (chat_members)
                
            #All types are defined in types.py. They are all completely in line with the Telegram API's definition of the types, 
            #except for the Message's from field, which is renamed to from_user (because from is a Python reserved token)
#            user_text = "Hello {}! You wrote: {}".format(update.message.from_user.first_name, update.message.text)
 #           logging.info("User: %s, Chat_id: %s, User_id: %s, Message: %s", update.message.from_user.first_name, update.message.chat.id, 
 #                                                                                       update.message.from_user.id, update.message.text)          
 #   else:
 #       user_text = "Hello {}! You wrote: {}".format(update.message.chat.first_name, update.message.text)
 #       logging.info("User: %s, Chat_id: %s, Message: %s", update.message.chat.first_name, update.message.chat.id, update.message.text)
 #   print(update.message)
#    update.message.reply_text(user_text)   
 #   try:
 #       bot.send_message(update.message.from_user.id, "You wrote smth?")
 #   except(Unauthorized):
 #       print("Santa-Claus bot was blocked by the user: %s %s" %(update.message.from_user.first_name, update.message.from_user.last_name))
        
    

def user_dict(key, val, remove=False):
    members = {}
    list = []
    if remove==False:
        members[key] = val      
        list.append(members)
#        if key not in members.keys():
#            list[key] = val
    elif remove==True:
        try:
            del members[key]
        except KeyError:
            print('Key is not in members!')
    print (list)



# Два подчеркивания (__) - системная переменная Питона
# Эта конструкция позволяет импортировать функции как методы в других файлах
# Если файл вызвали напрямую, выполняй функцию main()
if __name__ == "__main__":
    main()
  

