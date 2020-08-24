import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import messages
from sqlite3 import connect
import os.path
from Classes import Article, User
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.sqlite3")
db = connect(db_path, check_same_thread=False)
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id':random.randint(512, 2486141648)})


# API-ключ созданный ранее
token = "b182998a3aab72a77ed8bacd7c20cf9bc9fc61874e18d03d2dbb230af0f5c220a7ba250a125bcbbe4b07f"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
users_sendingsZapros = []
# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request : str = event.text
            thisUserIsSending = [None, None, None, None]
            for user in users_sendingsZapros:
                if user[0] == event.user_id:
                    thisUserIsSending = [event.user_id, user[1]]

            try:
                if request == "помощь":
                    write_msg(event.user_id, messages.help)
                if request == "отправить запрос":
                    if thisUserIsSending == False:
                        users_sendingsZapros.append([event.user_id, 0])
                        write_msg(event.user_id, "Введите имя запроса:")
                if thisUserIsSending[0] and thisUserIsSending[1] == 0:
                    thisUserIsSending.append(request)
                    write_msg(event.user_id, "Введите описание запроса:")
                    thisUserIsSending[1] = 1
                if thisUserIsSending[0] and thisUserIsSending[1] == 1:
                    thisUserIsSending.append(request)
                    write_msg(event.user_id, "Чтобы сохранить запрос напишите да чтобы не отправлять напишите что-то другое:")
                    thisUserIsSending[1] == 2
                if thisUserIsSending[0] and thisUserIsSending[1] == 2:
                    if request.lower() == "Да":
                        write_msg(event.user_id, "Запрос отправлен")
                        art = Article()
                        usr = User()
                        art.newArticle(thisUserIsSending[1], thisUserIsSending[2], database=db, cursor=db.cursor(), user=usr)
                        thisUserIsSending = []
            except IndexError:
                print ("Error: IndexError")