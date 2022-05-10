# -*- coding: utf-8 -*-
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          ConversationHandler, Filters, MessageHandler)
import json
import random

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

FIRST, SECOND, THIRD = range(3)

ONE, TWO, THREE = range(3)

with open("nft.json", encoding="utf8") as f, open("ducks.json",
                                                  encoding="utf8") as f1:
    nf_lst = json.load(f)["test"]
    du_lst = json.load(f1)["test"]


def start(update, context):
    context.user_data["nft"] = 0
    context.user_data["ducks"] = 0
    context.user_data["hi"] = 0
    context.user_data["index_of_del_mess"] = 0
    context.user_data["index_of_del_mess1"] = 0
    context.user_data["du_lst"] = du_lst[::]
    random.shuffle(context.user_data["du_lst"])

    keyboard = [
        [InlineKeyboardButton("NFT", callback_data=str(ONE))],
        [InlineKeyboardButton("Ducks", callback_data=str(TWO))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data["index_of_del_mess"] = update.message.reply_text(
        text="Привет, путка!(нет, я не обзываюсь, это просто путник + утка)\nЯ утка бот, люблю расширять свой уткозор интересными статьями и играми, могу рассказать о двух темах моего проекта, а именно про техгнологию NFT и уток!",
        reply_markup=reply_markup
    )

    return FIRST


def NFT(update, context):
    query = update.callback_query
    query.answer()

    if context.user_data["nft"] < 3:
        keyboard = [
            [
                InlineKeyboardButton("Продолжаем!", callback_data=str(ONE))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text=nf_lst[context.user_data["nft"]]["title"] + "\n" +
                 nf_lst[context.user_data["nft"]][
                     "inf"], reply_markup=reply_markup)
    else:
        keyboard = [
            [InlineKeyboardButton("Нет, на этом закончим",
                                  callback_data=str(THREE))],
            [InlineKeyboardButton("Конечно, сыграем в уточек!",
                                  callback_data=str(TWO))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text=nf_lst[context.user_data["nft"]]["title"] + "\n" +
                 nf_lst[context.user_data["nft"]][
                     "inf"], reply_markup=reply_markup)

    context.user_data["nft"] += 1

    return FIRST


def ducks(update, context):
    query = update.callback_query
    query.answer()

    if context.user_data["hi"] == 0:
        query.edit_message_text(
            text="А вы знали, что утки — одни из самых популярных птиц в домашнем хозяйстве, их одомашнили ещё древние египтяне? Знали, что существует около 110 видов уток? Знали, что утиное кряканье не имеет эха?! А может знали, что шейных позвонков у уток больше, чем у жирафов? А как вам тот факт, что утята действительно принимают за свою мать первое существо, которое видят, вылупившись из яйца? А ведь они ещё и очень бесстрашные, знали? \nИ это не все факты о них, всем уток, дорогие друзья! Давайте проверим ваши знания в области утковедения! Я пришлю Вам фотографии уток, а вы попробуете угадать её породу.",
            reply_markup=None)
        context.user_data["hi"] += 1

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Раз")

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Два")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Три!")

    lenn = len(context.user_data["du_lst"][context.user_data["ducks"]]["photo"])

    png = open(f'data/{context.user_data["du_lst"][context.user_data["ducks"]]["photo"][random.randint(0, lenn - 1)]}', 'rb')

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=png)

    return SECOND


def response(update, context):
    if update.message.s.capitalize() not in \
            context.user_data["du_lst"][context.user_data["ducks"]]["name"]:
        update.message.reply_text(
            f"Не угадали, порода этой утки - {context.user_data['du_lst'][context.user_data['ducks']]['name'][0]}")
    else:
        update.message.reply_text("Вы угадали!")

    keyboard = [
        [InlineKeyboardButton("Следующая утка!", callback_data=str(ONE))],
        [InlineKeyboardButton("Надоели эти утки!", callback_data=str(TWO))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.user_data['ducks'] == len(context.user_data["du_lst"]) - 1:
        update.message.reply_text(
            context.user_data["du_lst"][context.user_data["ducks"]][
                "inf"] + "\nКстати, если настоящую такую утку вы позволить себе не можете, то всегда можно купить DFT с ней и наслаждаться, скорее покупайте! " +
            context.user_data["du_lst"][context.user_data["ducks"]]["http"],
            reply_markup=None)
        update.message.reply_text(
            "Ой-ой, у меня кончились утки...чтож...Надеюсь теперь твои познания в утковедении стали больше, а твой уткозор стал шире! Удачи тебе, путка!")
        context.user_data.clear()
        return ConversationHandler.END

    else:
        update.message.reply_text(
            context.user_data["du_lst"][context.user_data["ducks"]][
                "inf"] + "\nКстати, если настоящую такую утку вы позволить себе не можете, то всегда можно купить DFT с ней и наслаждаться, скорее покупайте! " +
            context.user_data["du_lst"][context.user_data["ducks"]]["http"],
            reply_markup=reply_markup)

    context.user_data['ducks'] += 1

    return THIRD


def end(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Ты всё же решил покинуть нас...Ну ладно, до скорых уток!")

    context.user_data.clear()

    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater("5304149909:AAFGfjUxf_REttXlOf9-A1URE0knXaE2RcU",
                      use_context=True)

    dispatcher = updater.dispatcher
    jq = updater.job_queue

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(NFT, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(ducks, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(THREE) + '$'),
            ],
            SECOND: [
                MessageHandler(Filters.text & ~Filters.command, response),
            ],
            THIRD: [CallbackQueryHandler(ducks, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(end, pattern='^' + str(TWO) + '$')]

        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
