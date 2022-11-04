import dataclasses
import config
import logging
from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import MessageHandler, Filters
from models import ReceiptInfo, ReceiptResult
from receipts_api import request_receipt_details
import spread_sheet
from util import save_in_json


TMP_IMG_FILE = "./last_qr_photo.jpg"
DATA_PATH = "./data"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Send photos of your receipts here")


def photo_handler(update, context):
    """ handles receipt with qr code """
    newFile = update.message.effective_attachment[-1].get_file()
    newFile.download(TMP_IMG_FILE)
    try:
        receipt_result = get_details(TMP_IMG_FILE)
        if (receipt_result.is_ok):
            persist_receipt(receipt_result.receipt)
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="✅ Qr saved!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Failed to process Qr with error: " + receipt_result.errror_msg)
    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Failed to process Qr with error: " + str(e))


def get_details(path: str) -> ReceiptResult:
    with open(path, "rb") as f:
        return request_receipt_details(f)


def persist_receipt(receipt_info: ReceiptInfo):
    goods = list(map(lambda o: o.__dict__, receipt_info.goods))
    metadata_values = list(dataclasses.asdict(receipt_info.metadata).values())
    save_in_json(DATA_PATH, goods)
    rows = [metadata_values + list(good.values()) for good in goods]
    spread_sheet.add_rows(rows)


def main():
    updater = Updater(token=config.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    updater.start_polling()


if __name__ == '__main__':
    main()
