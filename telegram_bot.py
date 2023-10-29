import json
import logging

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)

from main import aggregate_salaries

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.message.text)
    answer = await aggregate_salaries(data.get("dt_from"), data.get("dt_upto"), data.get("group_type"))
    await update.message.reply_text(answer)


def main() -> None:
    application = (
        Application.builder()
        .token("6926863371:AAEP8Fy3A0LDDbuhzlrt8Y6R8clILs1cZ64")
        .build()
    )
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
