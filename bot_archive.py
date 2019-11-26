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

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')
 
#Тело бота
def main():
    mybot = Updater(settings.API, request_kwargs = settings.PROXY)    
    
    logging.info('Bot start')
    
    # This class dispatches all kinds of updates to its registered handlers.
    dp = mybot.dispatcher
    
    # Важно! Ставьте CommandHandler выше MessageHandler, тк он перехватит команды
    # The case if the user is already in chat group, use the command '/adm'
#    dp.add_handler(CommandHandler("adm", want_adm, pass_user_data=True))
    
    # Chat text message 
#    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    # New member was added after Santa-Claus bot was added
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_member, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, add_member, pass_user_data=True))

#    dp.add_handler(MessageHandler(Filters.status_update, update_member, pass_user_data=True))

    
    # Starts polling updates from Telegram.
    mybot.start_polling()
    # Blocks until one of the signals are received and stops the updater.
    mybot.idle()


# user_data - это словарь
def want_adm(bot, update, user_data):
    print("User send me a command /adm")    
    user_data[update.message.from_user.first_name] = update.message.from_user.id
    print(user_data)

def talk_to_me(bot, update, user_data):
    if update.message.chat.type == 'group':
        if update.message.chat.title == 'Santa-Clause':
            print("We are in Santa-Claus Group!")
           #     logging.info("The User: %s with User_id: %s was added to the Chat_id: %s,", update.message.from_user.first_name,  
            #                                                                                update.message.from_user.id, update.message.chat.id)
            #    new_chat_member = message.new_chat_participant.first_name 
            #    print(new_chat_member)
            #    chat_members = bot.get_chat_members_count(update.message.chat.id)
            #    print (chat_members)
                
            #All types are defined in types.py. They are all completely in line with the Telegram API's definition of the types, 
            #except for the Message's from field, which is renamed to from_user (because from is a Python reserved token)
            user_text = "Hello {}! You wrote: {}".format(update.message.from_user.first_name, update.message.text)
            logging.info("User: %s, Chat_id: %s, User_id: %s, Message: %s", update.message.from_user.first_name, update.message.chat.id, 
                                                                                        update.message.from_user.id, update.message.text)          
    else:
        user_text = "Hello {}! You wrote: {}".format(update.message.chat.first_name, update.message.text)
        logging.info("User: %s, Chat_id: %s, Message: %s", update.message.chat.first_name, update.message.chat.id, update.message.text)
    print(update.message)
#    update.message.reply_text(user_text)   
    try:
        bot.send_message(update.message.from_user.id, "You wrote smth?")
    except(Unauthorized):
        print("Santa-Claus bot was blocked by the user: %s %s" %(update.message.from_user.first_name, update.message.from_user.last_name))
        

def add_member(bot, update, user_data):
    print("We are inside add_member func!")
    print(update.message.new_chat_members[0])
    logging.info("The User: %s with User_id: %s in Chat_id: %s was added to the group", update.message.new_chat_members[0].first_name,  
                                                                        update.message.new_chat_members[0].id, update.message.chat.id)
    key = update.message.new_chat_members[0].first_name 
    val = update.message.new_chat_members[0].id
#    user_dict(key, val)
    bot.send_message(val, "Hello, %s! You wrote smth?" % (key))
    

    
def left_member(bot, update, user_data):
    print("We are inside left_member func!")
    print(update.message.left_chat_member)
    logging.info("The User: %s with User_id: %s in Chat_id: %s was removed from the group", update.message.left_chat_member.first_name,  
                                                                            update.message.left_chat_member.id, update.message.chat.id)
    key = update.message.left_chat_member.first_name
    val = update.message.left_chat_member.id
    user_dict(key, val, remove=True)    

    
def update_member(bot, update, user_data):
    print(update.message)
    print(update.message.left_chat_member)
    print(update.message.new_chat_members[0])
    
#    member_kicked = bot.kick_chat_member(update.message.chat.id, update.message.new_chat_members[0].id)
#    print(member_kicked)
    

def user_dict(key, val, remove=False):
    members = {}
    if remove==False:
        if key not in members.keys():
            members[key] = val
    elif remove==True:
        try:
            del members[key]
        except KeyError:
            print('Key is not in members!')
    print(members)


# Два подчеркивания (__) - системная переменная Питона
# Эта конструкция позволяет импортировать функции как методы в других файлах
# Если файл вызвали напрямую, выполняй функцию main()
if __name__ == "__main__":
    main()

