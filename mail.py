import requests
import random
import string
from multiprocessing import Pool

def get_domains():
    response = requests.get('https://api.mail.tm/domains')
    if response.status_code == 200:
        return [domain['domain'] for domain in response.json()['hydra:member']]
    else:
        print(f"ドメインの取得に失敗しました: {response.content}")
        return None

def send_to_discord(email, password):
    webhook_url = "discordwebhookurl"
    data = {
        "content": f"アカウントが正常に作成されました！メール: {email}, パスワード: {password}",
        "username": "メールアドレスジェネレーターさん"
    }
    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Discordへの送信に失敗しました: {err}")
    else:
        print("Discordへの通知が成功しました。")

def create_account(domain):
    api_url = "https://api.mail.tm/accounts"
    local_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"{local_part}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    account_data = {"address": email, "password": password}
    response = requests.post(api_url, json=account_data)
    if response.status_code == 201:
        print(f"アカウントが作成されました！メール: {email}, パスワード: {password}")
        send_to_discord(email, password)
    else:
        print(f"アカウントの作成に失敗しました: {response.content}")

def create_accounts_in_parallel(domains):
    with Pool(50) as p: 
        p.map(create_account, domains * 500)

if __name__ == "__main__":
    domains = get_domains()
    if domains:
        create_accounts_in_parallel(domains)