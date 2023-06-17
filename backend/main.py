import json

import openai
from openai.error import InvalidRequestError, RateLimitError

from datetime import datetime
from config import API_TOKEN



openai.api_key = API_TOKEN



class MessageHandler:


    def __init__(self, user_id: str) -> None:
        self.user_id = user_id


    def _get_dialog_history(self) -> list:
        with open('backend\data.json') as f:
            data = json.load(f)
        if self.user_id in data:
            messages = []
            for i in data[self.user_id]:
                messages.append(i[0])
                messages.append(i[1])
            return messages
        return []


    def _save_data(self, messages: dict, answer: dict) -> None:
        with open('backend\data.json') as f:
            data = json.load(f)
        if self.user_id in data:
            data[self.user_id].append((messages, answer, {"date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}))
        else:
            data[self.user_id] = [(messages, answer, {"date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")})]
        with open('backend\data.json', 'w') as f:
            json.dump(data, f)


    def question(self, text: str) -> str:
        """
        Главная функция, задает вопрос ChatGPT, и получает ответ от нее
        """
        messages = self._get_dialog_history()
        messages.append({'role': 'user', 'content': text})
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                temperature=0.5,
                max_tokens=1000
            )
        except RateLimitError:
            return 'Превышено количество запросов в минуту! Попробуйте позже'
        except InvalidRequestError:
            return 'Превышено количество допустимых токенов! Попробуйте укоротить свой запрос'
        response = response.choices[0].message
        self._save_data(messages[0], response)
        return response.content



def clear_dialog(user_id: str) -> None:
    with open('backend\data.json') as f:
        data = json.load(f)
    del data[user_id]
    with open('backend\data.json', 'w') as f:
        json.dump(data, f)
