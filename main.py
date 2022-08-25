from aiogram import Bot, Dispatcher, types, executor
import logging
import requests
from bs4 import BeautifulSoup as b

#BOT
logging.basicConfig(level=logging.INFO)
TOKEN = 'BOT TOKEN'
bot = Bot(token=TOKEN)
dp=Dispatcher(bot)

#Commands
@dp.message_handler(commands= ['start'])
async def startwork(message: types.Message):
    await bot.send_message(message.from_user.id, "Hello! I am test bot!")

@dp.message_handler(content_types=['text'])
async def messagefromuser(message: types.Message):
    if message.text == "Show me prices":
        URL = "https://kz.e-katalog.com/ek-list.php?search_=Приставки"
        r = requests.get(URL)
        soup = b(r.text, "html.parser")
        all_links = soup.find_all('a', class_="model-short-title no-u")
        for link in all_links:
            # Object page
            URL = "https://kz.e-katalog.com" + link['href']
            r = requests.get(URL)
            soup = b(r.text, "html.parser")

            name = soup.find("div", class_="fix-menu-name")
            pr = name.find('a').text
            name.find("a").extract()
            name = name.text

            await bot.send_message(message.from_user.id, name + " " + pr)
#polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





