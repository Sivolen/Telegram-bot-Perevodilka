from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import File
# from recasepunc.recasepunc import WordpieceTokenizer
from pathlib import Path
from modules.translate import translate_vosk, translate_sr

from settings import TM_TOKEN

# Set FMS storage
storage = MemoryStorage()


# Set bot parameters
bot = Bot(token=TM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(LoggingMiddleware())


async def handle_file(file: File, file_name: str) -> None:
    Path(f"cache").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"cache/{file_name}")


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
    print(message)

    audio = await bot.get_file(message.audio.file_id)  # Get file path
    await handle_file(file=audio, file_name=f"{message.audio.file_name}")

    google_text = translate_sr(message.audio.file_name)
    await message.answer(f"Google {google_text}")
    vosk_text = translate_vosk(message.audio.file_name)
    await message.answer(f"Vosk {vosk_text}")
    # Delete source file
    Path(f"cache/{message.audio.file_name}").unlink()

    # print(f"Google {text}")
    # print(f"Vosk {text1}")


@dp.message_handler(content_types=["voice"])
async def echo(message: types.Message):
    print(message)
    voice = await message.voice.get_file()
    await handle_file(file=voice, file_name=f"{voice.file_id}.ogg")
    google_text = translate_sr(f"{voice.file_id}.ogg")
    await message.answer(f"Google {google_text}")
    vosk_text = translate_vosk(f"{voice.file_id}.ogg")
    await message.answer(f"Vosk {vosk_text}")
    print(message)
    # Delete source file
    Path(f"cache/{voice.file_id}.ogg").unlink()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
