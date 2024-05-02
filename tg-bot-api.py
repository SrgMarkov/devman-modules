import os

from flask import Flask, request
import httpx
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

tg_bot_token = os.getenv('TG_BOT_TOKEN')
tunnel_url = os.getenv('NGROK_TUNNEL_URL')

URL = f'https://api.telegram.org/bot{tg_bot_token}/'


def set_webhook():
    info_response = httpx.get(f'{URL}getWebhookInfo')
    if info_response.json()['result']['url'] != tunnel_url:
        httpx.post(f'{URL}setWebhook?url={tunnel_url}/bot')
        print('Вебхук установлен')


def get_updates():
    response = httpx.get(f'{URL}getUpdates')
    return response.json()


def send_message(chat_id, text):
    response = httpx.post(f'{URL}sendMessage', json={'chat_id': chat_id, 'text': text})
    return response.json()


@app.route('/bot', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tg_response = request.get_json()
        chat_id = tg_response['message']['chat']['id']
        text = tg_response['message']['text']
        send_message(chat_id, text)
    return 'BOT is running'


if __name__ == '__main__':
    set_webhook()
    app.run(port=8080)
