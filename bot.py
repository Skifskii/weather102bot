import bot_config
from aiogram import Bot, Dispatcher, executor, types
import datetime
import requests

#weatherbot

bot = Bot(token=bot_config.telegram_token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Напиши название города!")


@dp.message_handler(commands="info")
async def start(message: types.Message):
    await message.answer("Weather102Bot\n\nРазработчик - sskifskii")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={bot_config.open_weather_token}&units=metric')
        data = response.json()

        code_to_smile = {
            "Clear": "\U00002600 Ясно",
            "Clouds": "\U00002601 Облачно",
            "Rain": "\U00002614 Дождь",
            "Drizzle": "\U00002614 Дождь",
            "Thunderstorm": "\U000026A1 Гроза",
            "Snow": "\U0001F328 Снег",
            "Mist": "\U0001F32B Туман"
        }

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = ""

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(
                f"Погода в городе: {city}\n"
                f"\n"
                f"{wd}\n"
                f"🌡Температура: {cur_weather}C°\n"
                f"💧Влажность: {humidity}%\n"
                f"♨Давление: {pressure} мм.рт.ст\n"
                f"💨Ветер: {wind} м/с\n"
                f"🌅Восход солнца: {sunrise}\n"
                f"🌇Закат солнца: {sunset}\n"
                f"\n"
                f"Хорошего дня!\n"
                )

    except:
        await message.reply('Некоректное название города')



if __name__ == '__main__':
    executor.start_polling(dp)



