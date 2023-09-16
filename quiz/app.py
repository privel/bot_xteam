
import logging
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import configparser
from a_state import quiz,answering
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

__connection = None
config = configparser.ConfigParser()
config.read("setting.ini")


API_TOKEN = config["Bot"]["bot_token"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('data.db')
    return __connection


	
def update_first(user_id, user_name, tetx):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO work (user_id, user_name, q1) VALUES (?, ?, ?)', (user_id, user_name, tetx))
    conn.commit() 

def update_second(user_id, tetx):
    conn = get_connection()
    c = conn.cursor()
    #c.execute('INSERT INTO work (q2) VALUES (?)', (tetx,))
    c.execute('UPDATE work SET q2=(?) WHERE user_id=(?)', (tetx,user_id,))
    conn.commit() 

def update_third(user_id, tetx):
    conn = get_connection()
    c = conn.cursor()
    #c.execute('INSERT INTO work (q3) VALUES (?)', (tetx,))
    c.execute('UPDATE work SET q3=(?) WHERE user_id=(?)', (tetx,user_id,))
    conn.commit() 
def find_worker(user_id):
	conn = get_connection()
	c = conn.cursor()
	c.execute('SELECT * FROM work WHERE user_id=(?)', (user_id,))
	s = c.fetchone()
	return(s[0])

def opros_workera(user_id):
	conn = get_connection()
	c = conn.cursor()
	c.execute("SELECT * FROM work WHERE user_id=(?)",(user_id))
	s = c.fetchone()
	return([s[0],s[1],s[2],s[3],s[4],s[5]])

def opros_workera2(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM work WHERE user_id = (?)", (user_id,))
    return c.fetchone()



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	
    
	#await message.reply('Выберите вариант пополнения баланса',reply_markup=markup)
	print(message.chat.id)
	await message.reply("🧠 Есть ли у Вас опыт ?\n Если да, то скажите какой?")
	await quiz.q1.set()

@dp.message_handler(commands=['/chat_id'])
async def send_id(message: types.Message):
	await message.reply(f"chat id = <code>{message.chat.id}</code>")



@dp.message_handler(state=quiz.q1)
async def qwewqe(message: types.Message, state: FSMContext):
	data = await state.get_data()
	update_first(message.from_user.id, message.from_user.username, message.text)
	
	await message.reply("💁‍♀️Сколько Вы готовы уделять времени своей работе?")
	await state.finish()
	await quiz.q2.set()

@dp.message_handler(state=quiz.q2)
async def sqm(message: types.Message, state: FSMContext):
	data2 = await state.get_data()
	await message.reply("Отлично,пожалуйста скажите от куда вы узнали о нас ?")
	update_second(message.from_user.id, message.text)
	await state.finish()
	await quiz.q3.set()


@dp.message_handler(state=quiz.q3)
async def ssq(message:types.Message, state: FSMContext):
	u_id = message.from_user.id
	markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✔Принять', callback_data='aprov')
            ]
        ]
    )
	data3 = await state.get_data()
	update_third(message.from_user.id, message.text)
	await message.reply("✅ Заявка успешно отправлена ожидайте ответа")
	await bot.send_message(chat_id=-1001967468942,text=f"Пользователь <code>{message.from_user.id}</code> @{message.from_user.username} \n Ответы воркера \n 🧠 Есть ли у Вас опыт ? Если да, то скажите какой? \n Ответ: {opros_workera2(message.from_user.id)[2]} \n 💁‍♀️Сколько Вы готовы уделять времени своей работе? \n Ответ {opros_workera2(message.from_user.id)[3]} \n Отлично,пожалуйста скажите от куда вы узнали о нас ? \n Ответ: {opros_workera2(message.from_user.id)[4]}", parse_mode='HTML', reply_markup=markup)
	await state.finish()


@dp.callback_query_handler(text='aprov')
async def qwewqe(call: types.CallbackQuery):
	
	await call.message.answer('Введите id воркера \n пример /778282373')
	
	await answering.ans.set()
	


@dp.message_handler(state=answering.ans)
async def qweas(message:types.Message, state: FSMContext):
	data4 = await state.get_data()
	
	try:
		await bot.send_message(chat_id=int(message.text[1:]),text="👩🏻‍💻 Чат воркеров: https://t.me/+k-B02DWUWsRkMzE6\n\n 🦹🏼‍♀️ Тс: SteallSexy\n\n ✅ Вся информация находиться в закрепленном сообщении в чате воркеров")
		
	except Exception as e:
		await message.answer(f'<b>❌ Некорректный ввод Exception</b> {e}')
	await state.finish()
	# await state.finish()


# @dp.message_handler()
# async def echo(message: types.Message):
#     await bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)