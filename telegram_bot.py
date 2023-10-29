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
    if update.message and update.message.text:
        nonBreakSpace = "\xa0"
        json_data = update.message.text.replace(nonBreakSpace, " ")
        data = json.loads(json_data)
        dt_from = data.get("dt_from")
        dt_upto = data.get("dt_upto")
        group_type = data.get("group_type")
        answer = await aggregate_salaries(dt_from, dt_upto, group_type)
        await update.message.reply_text(answer)
    else:
        print("Empty Data")


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
