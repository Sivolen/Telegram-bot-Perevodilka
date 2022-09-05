from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from recasepunc.recasepunc import WordpieceTokenizer
from pathlib import Path
from modules.translate import translate, converter_wav

from settings import TM_TOKEN

# Set FMS storage
storage = MemoryStorage()


# Set bot parameters
bot = Bot(token=TM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Perevodilka!\nI'm translate your voice massages.")


@dp.message_handler(content_types=["audio"])
async def echo(message: types.Message):
    """
    This handler will be called when user sends audio file and starts the process of converting to text
    :param message: Audio
    :return: None
    """
    cache_folder = Path("cache")
    if not cache_folder.is_dir():
        cache_folder.mkdir()
    file_id = message.audio.file_id  # Get file id
    file = await bot.get_file(file_id)  # Get file path
    await bot.download_file(
        file.file_path, destination=f"cache/{message.audio.file_name}"
    )
    # print(open(f"cache/{message.audio.file_name}", "rb").read)
    text = converter_wav(message.audio.file_name)
    text_file = Path(f"cache/{message.audio.file_name}")
    await message.answer(f"Google {text}")
    text1 = translate(message.audio.file_name)
    await message.answer(f"Vosk {text1}")
    # print(f"Google {text}")
    # print(f"Vosk {text1}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

