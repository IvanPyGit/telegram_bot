from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename = "mylog.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

# from config import TOKEN

TOKEN = '5144649363:AAFVXcUKNCVuwWoB5784xylPX_i4D2pCrP0'
#пользуемся LongPolling для теста, потом перепишем под Webhook
bot = Bot(token = TOKEN) #инициализируем бота
dp = Dispatcher(bot) #инициализируем диспетчер


# айограм ассинхронная библиотека, когда в потоке появляется пауза - исполняем что-то другое
# @dp.message_handler() #сюда попадает декоратор, обозначает событие когда нам кто-то пишет
# async def echo_send(message : types.Message): #через : аннотация типа для параметра
#     await message.answer(message.text) #простое смс
# await message.reply(message.text) #отвечаем на сообщение пользователя текстом
# await bot.send_message(message.from_user.id, message.text) #в лс, только если пользователь уже общался с ботом



async def on_startup(_):
	print('Бот вышел в онлайн')

'''******************************КЛИЕНТСКАЯ ЧАСТЬ*******************************************'''
@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
	try: #обработка ошибок - не удалось отправить сообщение
		await bot.send_message(message.from_user.id, 'Приятного аппетита')
		await message.delete() #удаляем сообщение
	except: # не указали ошибку
		await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Pizza_SheefBot')
# отвечаем на сообщение

@dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message : types.Message):
	await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')

@dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message : types.Message):
	await bot.send_message(message.from_user.id, 'ул. Колбасная 15')


# @dp.message_handler(commands=['Меню'])
# async def pizza_menu_command(message : types.Message):
# 	for ret in cur.execute('SELECT * FROM menu').fetchall():
# 	   await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
'''*******************************АДМИНСКАЯ ЧАСТЬ*******************************************'''

'''*********************************ОБЩАЯ ЧАСТЬ*********************************************'''

@dp.message_handler()
async def echo_send(message : types.Message):
	if message.text == 'Привет':
		await message.answer('И тебе привет!')
	# await message.reply(message.text)
	# await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
# ипропускать обновления, чтобы когда бот вне сети после активации его не заваливало сообщениями и он на них не отвечал