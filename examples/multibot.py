import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.command import Command, CommandObject
from aiogram.types import BotCommand, BotCommandScopeDefault, User
from aiogram.utils.token import TokenValidationError

logger = logging.getLogger(__name__)

TOKENS = [
    "TOKEN1",
    "TOKEN2",
]
ADMIN_ID = 123456789


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="add_bot",
            description="add bot, usage '/add_bot 123456789:qwertyuiopasdfgh'",
        ),
        BotCommand(
            command="stop_bot",
            description="stop bot, usage '/stop_bot 123456789'",
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def on_startup(bot: Bot):
    await set_commands(bot)
    await bot.send_message(chat_id=ADMIN_ID, text="Bot started!")


async def on_shutdown(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text="Bot shutdown!")


async def add_bot(message: types.Message, command: CommandObject, dp: Dispatcher):
    if command.args:
        try:
            bot = Bot(command.args)
            user: User = await bot.me()
            asyncio.create_task(dp.start_bot_polling(bot=bot, dp=dp))
            await message.answer(f"New bot started: @{user.username}")
        except TokenValidationError as err:
            await message.answer(f"{str(err)}")
    else:
        await message.answer("Please provide token")


async def stop_bot(message: types.Message, command: CommandObject, dp: Dispatcher):
    if command.args:
        try:
            dp.stop_bot_polling(int(command.args))
        except (ValueError, KeyError) as err:
            await message.answer(f"{str(err)}")
    else:
        await message.answer("Please provide bot id")


async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bots = [Bot(token) for token in TOKENS]
    dp = Dispatcher(isolate_events=True)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.register(add_bot, Command(commands="add_bot"))
    dp.message.register(stop_bot, Command(commands="stop_bot"))

    dp.message.register(echo)

    for bot in bots:
        await bot.get_updates(offset=-1)
    await dp.start_polling(*bots, dp=dp)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Exit")
