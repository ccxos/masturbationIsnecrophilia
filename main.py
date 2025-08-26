import telebot
import requests
import re

BOT_TOKEN = "6361025046:AAGJipp5umiDUZ1xJaUmuDckyLX1RW9PsIU"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me a TikTok username and I will return the profile picture.")

def fetch_from_api(username):
    url = f"https://www.tikwm.com/api/user/info?unique_id={username}"
    r = requests.get(url, timeout=10).json()
    if r.get("code") == 0 and "author" in r["data"] and "avatar" in r["data"]["author"]:
        return r["data"]["author"]["avatar"]
    return None

def scrape_avatar(username):
    profile_url = f"https://www.tiktok.com/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(profile_url, headers=headers, timeout=10)
    if r.status_code != 200:
        return None
    m = re.search(r'"avatarLarger":"([^"]+)"', r.text)
    if m:
        return m.group(1).encode('utf-8').decode('unicode_escape')
    return None

@bot.message_handler(func=lambda m: True)
def fetch_avatar(message):
    username = message.text.strip().lstrip("@")

    avatar_url = fetch_from_api(username)
    if not avatar_url:
        avatar_url = scrape_avatar(username)

    if avatar_url:
        bot.send_photo(message.chat.id, avatar_url)
    else:
        bot.reply_to(message, "Could not fetch avatar. Maybe the username is invalid or the API doesn't support it.")

print("Bot is running...")
bot.infinity_polling()
