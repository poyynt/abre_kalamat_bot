from aiogram import Bot, Dispatcher, executor, types
import json
import twitter_with_twint

HELP_STRING = """
برای ساختن ابرکلمات از توییتر از این دستور استفاده کن:
`/twitter <profile> [mask]`
که `mask` اختباریه و میتونه یکی از:
"iran", "telegram", "twitter" 
باشه
لطفا صبور باش، ممکنه ساختن ابرکلماتت چند دقیقه طول بکشه
"""

config = json.load(open("config.json"))

bot = Bot(token = config["token"])
dp = Dispatcher(bot)

@dp.message_handler(commands = ["start", "help"])
async def help(message: types.Message):
	await message.reply(HELP_STRING, parse_mode = types.ParseMode.MARKDOWN)

@dp.message_handler(commands = ["twitter"])
async def twitter(message: types.Message):
	msg = message.text.split()
	if len(msg) == 1:
		pass #error
	idish = msg[1]
	if len(msg) == 2:
		mask = "twitter"
	else:
		mask = msg[2]
	twitter_with_twint.make(idish, mask)
	with open(f"out/{idish}.png", "rb") as photo:
		await message.reply_photo(photo)
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates = True)
