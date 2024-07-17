from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random

API_TOKEN = '7487132330:AAGso3DBAQ7Cj4Z4de0xuszhGCwbbeEEIlo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

questions = [
    {"question": "Столица Франции?", "answer": "Париж", "options": ["Берлин", "Мадрид", "Париж", "Рим"]},
    {"question": "2 + 2?", "answer": "4", "options": ["3", "4", "5", "6"]},
    {"question": "Самая большая планета Солнечной системы?", "answer": "Юпитер",
     "options": ["Земля", "Марс", "Юпитер", "Сатурн"]},
    {"question": "Какое самое глубокое озеро в мире?", "answer": "Байкал",
     "options": ["Байкал", "Титикака", "Виктория", "Онтарио"]},
    {"question": "Кто написал роман 'Война и мир'?", "answer": "Толстой",
     "options": ["Достоевский", "Толстой", "Пушкин", "Гоголь"]},
    {"question": "Сколько минут в одном часе?", "answer": "60", "options": ["30", "45", "60", "90"]},
    {"question": "Как называется крупнейший океан на Земле?", "answer": "Тихий",
     "options": ["Атлантический", "Индийский", "Северный Ледовитый", "Тихий"]},
    {"question": "Сколько континентов на Земле?", "answer": "7", "options": ["5", "6", "7", "8"]},
    {"question": "Какой элемент таблицы Менделеева обозначается символом 'O'?", "answer": "Кислород",
     "options": ["Водород", "Кислород", "Азот", "Углерод"]},
    {"question": "Кто был первым президентом США?", "answer": "Джордж Вашингтон",
     "options": ["Авраам Линкольн", "Джордж Вашингтон", "Томас Джефферсон", "Бенджамин Франклин"]},
    {"question": "Столица Японии?", "answer": "Токио", "options": ["Пекин", "Сеул", "Токио", "Киото"]},
    {"question": "В каком году состоялся первый полет человека в космос?", "answer": "1961",
     "options": ["1957", "1961", "1969", "1972"]},
    {"question": "Какая страна является родиной пиццы?", "answer": "Италия",
     "options": ["Франция", "Италия", "Испания", "Греция"]},
    {"question": "Сколько дней в високосном году?", "answer": "366", "options": ["364", "365", "366", "367"]},
    {"question": "Как называется самая маленькая кость в человеческом теле?", "answer": "Стремечко",
     "options": ["Молоточек", "Ключица", "Стремечко", "Пяточная кость"]},
    {"question": "Кто написал симфонию №9 'Ода к радости'?", "answer": "Бетховен",
     "options": ["Моцарт", "Бетховен", "Бах", "Чайковский"]},
    {"question": "Какое химическое соединение имеет формулу H2O?", "answer": "Вода",
     "options": ["Вода", "Метан", "Кислород", "Водород"]},
    {"question": "Какая планета ближе всего к Солнцу?", "answer": "Меркурий",
     "options": ["Венера", "Земля", "Марс", "Меркурий"]},
    {"question": "Кто автор картины 'Мона Лиза'?", "answer": "Леонардо да Винчи",
     "options": ["Пабло Пикассо", "Винсент Ван Гог", "Леонардо да Винчи", "Микеланджело"]},
    {"question": "Какая самая длинная река в мире?", "answer": "Нил",
     "options": ["Амазонка", "Конго", "Миссисипи", "Нил"]},
    {"question": "Сколько часов в сутках?", "answer": "24", "options": ["12", "24", "36", "48"]},
    {"question": "Как называется крупнейшая пустыня в мире?", "answer": "Сахара",
     "options": ["Гоби", "Калахари", "Сахара", "Антарктическая"]},
    {"question": "Кто изобрел лампочку?", "answer": "Томас Эдисон",
     "options": ["Александр Белл", "Томас Эдисон", "Никола Тесла", "Гульельмо Маркони"]},
    {"question": "Столица Германии?", "answer": "Берлин", "options": ["Мюнхен", "Гамбург", "Берлин", "Франкфурт"]},
    {"question": "В каком году распался Советский Союз?", "answer": "1991", "options": ["1989", "1990", "1991", "1992"]}
]

current_question = {}
score = 0
remaining_questions = []


@dp.message_handler(commands=['start'])
async def start_quiz(message: types.Message):
    global current_question, score, remaining_questions
    score = 0
    remaining_questions = questions.copy()
    current_question = random.choice(remaining_questions)

    # Создание клавиатуры с вариантами ответов
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in current_question["options"]:
        markup.add(KeyboardButton(option))

    await message.answer(current_question['question'], reply_markup=markup)


@dp.message_handler()
async def check_answer(message: types.Message):
    global current_question, score, remaining_questions
    if message.text.lower() == current_question['answer'].lower():
        score += 1
        await message.answer(f"Правильно! Ваши очки: {score}")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {current_question['answer']}")

    # Переход к следующему вопросу или завершение викторины
    remaining_questions.remove(current_question)
    if remaining_questions:
        current_question = random.choice(remaining_questions)

        # Создание клавиатуры с вариантами ответов
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for option in current_question["options"]:
            markup.add(KeyboardButton(option))

        await message.answer(current_question['question'], reply_markup=markup)
    else:
        await message.answer(f"Викторина завершена! Ваши очки: {score}")
        # Удаление клавиатуры после завершения викторины
        await message.answer("Спасибо за участие!", reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
