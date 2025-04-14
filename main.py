import logging
import re
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel

# Укажите данные вашего аккаунта
API_ID = 20909352  # Ваш API ID, полученный с https://my.telegram.org
API_HASH = "a3be2584a77447cfc0c7d1595076e9dc"  # Ваш API Hash, полученный с https://my.telegram.org

# Настройка ID для групп
SOURCE_GROUP_ID = -1002459101321  # ID исходной группы
DESTINATION_GROUP_ID = -1002680292174  # ID целевой группы

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Словарь для слов и соответствующих ID топиков
WORD_TO_TOPIC_ID = {
    "B-Day Candle": 227,
    "Desk Calendar": 224,
    "Homemade Cake": 221,
    "Sakura Flower": 218,
    "Lol Pop": 215,
    "Spy Agaric": 212,
    "Eternal Candle": 209,
    "Witch Hat": 206,
    "Scared Cat": 203,
    "Voodoo Doll": 200,
    "Flying Broom": 197,
    "Crystall Ball": 194,
    "Skull Flower": 191,
    "Trapped Heart": 188,
    "Mad Pumpkin": 185,
    "Sharp Tongue": 182,
    "Ion Gem": 179,
    "Evil Eye": 176,
    "Hex Pot": 173,
    "Hypno Lollipop": 170,
    "Kissed Frog": 167,
    "Electric Skull": 164,
    "Magic Potion": 161,
    "Record Player": 158,
    "Vintage Cigar": 155,
    "Berry Box": 152,
    "Eternal Rose": 149,
    "Mini Oscar": 146,
    "Perfume Bottle": 143,
    "Love Candle": 140,
    "Durov's Cap": 137,
    "Hanging Star": 134,
    "Jelly Bunny": 131,
    "Spiced Wine": 127,
    "Plush Pepe": 124,
    "Precious Peach": 121,
    "Astral Shard": 118,
    "Genie Lamp": 115,
    "Signet Ring": 112,
    "Swiss Watch": 109,
    "Bunny Muffin": 106,
    "Star Notepad": 103,
    "Jester Hat": 100,
    "Sleigh Bell": 97,
    "Snow Mittens": 94,
    "Snow Globe": 91,
    "Santa Hat": 88,
    "Winter Wreath": 85,
    "Ginger Cookie": 82,
    "Jingle Bells": 79,
    "Party Sparkler": 76,
    "Cookie Heart": 73,
    "Candy Cane": 69,
    "Tama Gadget": 66,
    "Lunar Snake": 63,
    "Loot Bag": 60,
    "Diamond Ring": 57,
    "Toy Bear": 54,
    "Love Potion": 51,
    "Top Hat": 48,
    "Neko Helmet": 45
}

# Инициализация клиента Telegram
client = TelegramClient("user_account", API_ID, API_HASH)


@client.on(events.NewMessage)
async def handle_messages(event):
    """
    Обрабатывает сообщения из исходной группы и пересылает их в соответствующий топик целевой группы.
    """
    try:
        # Проверяем, что сообщение пришло из исходной группы
        if event.chat_id == SOURCE_GROUP_ID:
            # Проверяем наличие ключевых слов в сообщении
            for word, topic_id in WORD_TO_TOPIC_ID.items():
                if word in event.message.message:
                    # Логируем найденное слово и ID топика
                    logging.info(f"Найдено слово: '{word}', пересылаем в топик ID: {topic_id}")

                    # Пересылаем сообщение в соответствующий топик
                    await client.send_message(
                        entity=PeerChannel(DESTINATION_GROUP_ID),
                        message=event.message.message,
                        reply_to=topic_id  # Используем reply_to для указания топика
                    )
                    logging.info(f"Сообщение успешно переслано в топик ID: {topic_id}")
                    return  # Выходим из цикла после пересылки, чтобы не отправлять дубли
            logging.warning("Слово для пересылки не найдено в сообщении.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


async def main():
    logging.info("Запуск клиента Telegram...")
    async with client:
        await client.run_until_disconnected()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())