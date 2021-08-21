import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = "BOT TOKEN"
dp = Dispatcher()

logger = logging.getLogger(__name__)


@dp.message(commands={"start"})
async def command_start_handler(message: Message, event_update) -> None:
    times = 1_000_000
    event = event_update

    print(f"Call times: {times}")
    start = datetime.now()
    for _ in range(times):
        event.event_last_cached
    print("Update type last     Cached", datetime.now() - start)

    start2 = datetime.now()
    for _ in range(times):
        event.event_last
    print("Update type last     Uncached", datetime.now() - start2)

    print("--------------------------------------------------------")

    start = datetime.now()
    for _ in range(times):
        event.event_first_cached
    print("Update type first    Cached", datetime.now() - start)

    start2 = datetime.now()
    for _ in range(times):
        event.event_first
    print("Update type first    Uncached", datetime.now() - start2)

    print("--------------------------------------------------------")

    start = datetime.now()
    for _ in range(times):
        event.message.content_type_last_cached
    print("Message type last    Cached", datetime.now() - start)

    start2 = datetime.now()
    for _ in range(times):
        event.message.content_type_last
    print("Message type last    Uncached", datetime.now() - start2)

    print("--------------------------------------------------------")

    start = datetime.now()
    for _ in range(times):
        event.message.content_type_first_cached
    print("Message type first   Cached", datetime.now() - start)

    start2 = datetime.now()
    for _ in range(times):
        event.message.content_type_first
    print("Message type first   Uncached", datetime.now() - start2)


def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
