import datetime
from os import environ
from os.path import join, dirname
import telegram
from dotenv import load_dotenv
from models import get_session, get_last_cotizaciones
from utils import format_cotizaciones_for_telegram
from logger_factory import get_logger

logger = get_logger("channel")

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

TOKEN = environ.get("TOKEN", None)
CHANNEL = environ.get("CHANNEL", None)
OWNER = environ.get("OWNER", None)


def send_cotizaciones(bot):
    now = datetime.datetime.now()
    session = get_session()
    cotizaciones = get_last_cotizaciones(now, session)
    text = format_cotizaciones_for_telegram(cotizaciones)
    if text:
        bot.sendMessage(chat_id=CHANNEL,
                        text=text,
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        logger.warning("No hubo cotizaciones para el día de hoy")


if __name__ == '__main__':
    bot = telegram.Bot(token=TOKEN)
    send_cotizaciones(bot)
