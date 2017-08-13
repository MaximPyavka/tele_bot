import requests
import datetime



token = "353018784:AAGWKfvmUShKnxGuB0xyLL0bZBj5i9RsMxk"

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates_json(self, offset=None, timeout=100):
        params = {'timeout': timeout, 'offset': offset}
        method = "getUpdates"
        response = requests.get(self.api_url+method, data=params)
        return response.json()['result']

    def get_last_update(self):
        get_result = self.get_updates_json()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

    def get_chat_id(self):
        chat_id = self.get_last_update['message']['chat']['id']
        return chat_id

    def send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        method = "sendMessage"
        response = requests.post(self.api_url+method, data=params)
        return response

mr_bot = BotHandler(token)
greetings = ('hello', 'здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()

def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        updates = mr_bot.get_updates_json(new_offset)

        if updates:

            last_update = mr_bot.get_last_update()

            last_update_id = last_update['update_id']
            print(last_update_id)
            last_chat_text = last_update['message']['text']
            print(last_chat_text)
            last_chat_id = last_update['message']['chat']['id']
            print(last_chat_id)
            last_chat_name = last_update['message']['chat']['first_name']
            print(last_chat_name)
            print(now.day)
            print(today)

            if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
                mr_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                mr_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                mr_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
                today += 1

            new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()



