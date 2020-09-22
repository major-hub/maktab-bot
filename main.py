from logging import getLogger
from telegram import Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters

from config import *
from pupil import *
from admin import *
from registration import *
from my_logger import debug_requests

logger = getLogger(__name__)


def do_start(update: Update, context):
    user = update.effective_user
    if user.id in admin_ids():
        update.message.reply_text(
            text="Assalomu alaykum! Men sizning yordamchingizman. O'quvchilarning test berish va "
                 "ularning baholari haqida sizga ma'lumot beraman. "
                 "Batafsil ma'lumot uchun /help ni bosing",
            reply_markup=ReplyKeyboardRemove()
        )
    elif not check_person(user_id=user.id):
        update.message.reply_text(
            text="Assalomu alaykum !\nBu bot masofaviy o'qishda o'quvchi va o'qituvchi o'rtasidagi "
                 "savol-javob bilan bilim almashish va o'quvchini baholash uchun xizmat qiladi. "
                 "Buning uchun avval ro'yhatdan o'ting\n\n"
                 "Ro'yhatdan o'tish uchun /login ni bosing",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        update.message.reply_text("Siz ro'yhatdan o'tgansiz. Batafsil ma'lumot uchun /help ni bosing",
                                  reply_markup=ReplyKeyboardRemove())


def do_help1(update: Update, context):
    user = update.effective_user
    if user.id in admin_ids():
        update.message.reply_text(
            text="Sizga quyidagi imkoniyatlar bo'yicha yordam beraman",
            reply_markup=help_buttons(),
        )
    elif check_person(user_id=user.id):
        update.message.reply_text(
            text="Xurmatli o'quvchi! Test topshirishga tayyormisiz ?\n\n"
                 "#diqqat Bu bot orqali o'qtuvchingiz sizni baholaydi va sizga ma'lumot yuboradi",
            reply_markup=pupil_help_buttons()
        )
    else:
        update.message.reply_text(
            "Iltimos, avval ro'yhatdan o'ting!\n\n"
            "Ro'yhatdan o'tish uchun /login ni bosing",
            reply_markup=ReplyKeyboardRemove()
        )


def do_help2(update: Update, context):
    user = update.effective_user
    if user.id in admin_ids():
        update.message.reply_text(
            text="❗️Foydalanishda <b>Namuna</b>dagidek yozing\n"
                 "Ustozlar ro'yhatini ko'rish uchun\n"
                 "Namuna: <pre>#ustozlar</pre>\n"
                 "Sinf testlarini ko'rish uchun\n"
                 "Namuna: <pre>#testlar 7 Rus_tili</pre>\n"
                 "O'quvchini delete qilish uchun\n"
                 "Namuna: <pre>#delete_pupil Familya Ism</pre>\n"
                 "Ustozni delete qilish uchun\n"
                 "Namuna: <pre>#delete_teacher Familya Ism</pre>\n",

            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
    elif check_person(user_id=user.id):
        update.message.reply_text(
            text="Xurmatli o'quvchi! Test topshirishga tayyormisiz ?\n\n"
                 "#diqqat Bu bot orqali o'qtuvchingiz sizni baholaydi va sizga ma'lumot yuboradi",
            reply_markup=pupil_help_buttons()
        )
    else:
        update.message.reply_text(
            "Iltimos, avval ro'yhatdan o'ting!\n\n"
            "Ro'yhatdan o'tish uchun /login ni bosing",
            reply_markup=ReplyKeyboardRemove()
        )


def do_message(update: Update, context):
    user = update.effective_user
    text = update.effective_message.text
    if user.id in admin_ids():
        if text.startswith('#'):
            admin_commands(update, text)
        else:
            admin_commands2(update, text)
    elif check_person(user_id=user.id):
        user_commands(update, text)
    else:
        update.message.reply_text(
            "Iltimos, avval ro'yhatdan o'ting!\n\n"
            "Ro'yhatdan o'tish uchun /login ni bosing",
            reply_markup=ReplyKeyboardRemove()
        )


def do_cancel(update, context):
    update.message.reply_text("Ba'zi holatlarda ishlatiladi !")


def do_error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update,  context.error)


def main():
    logger.info("Bot started...")
    updater = Updater(token=TOKEN, use_context=True)
    init_db_pupils()          #
    init_db_tests()           #       instalizatsiya
    logger.info(updater.bot.get_me())
    dp = updater.dispatcher

    start_handler = CommandHandler('start', do_start)
    start_cancel = CommandHandler('cancel', do_cancel)
    help1_handler = CommandHandler('help', do_help1)
    help2_handler = CommandHandler('help2', do_help2)
    message_handler = MessageHandler(Filters.all, do_message)

    # pupil.py
    test_handler = ConversationHandler(
        entry_points=[CommandHandler('test', test)],
        states={
            TESTFAN: [CommandHandler('cancel', cancel_test), MessageHandler(Filters.text, test_fan, pass_user_data=True)],
            TEST1: [CommandHandler('cancel', cancel_test), MessageHandler(Filters.text, check1, pass_user_data=True)],
            TEST2: [CommandHandler('cancel', cancel_test), MessageHandler(Filters.text, check2, pass_user_data=True)],
            TEST3: [CommandHandler('cancel', cancel_test), MessageHandler(Filters.text, check3, pass_user_data=True)],
            TEST4: [CommandHandler('cancel', cancel_test), MessageHandler(Filters.text, check4, pass_user_data=True)],
            TEST5: [CommandHandler('cancel', cancel_test), MessageHandler(Filters.text, check5, pass_user_data=True)],
        },
        fallbacks=[CommandHandler('cancel', cancel_test)]
    )
    # admin.py
    add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            LEVEL: [CommandHandler('cancel', cancel_add), MessageHandler(Filters.text, level, pass_user_data=True)],
            ANSWER_A: [CommandHandler('cancel', cancel_add), MessageHandler(Filters.text, answerA, pass_user_data=True)],
            ANSWER_B: [CommandHandler('cancel', cancel_add), MessageHandler(Filters.text, answerB, pass_user_data=True)],
            ANSWER_C: [CommandHandler('cancel', cancel_add), MessageHandler(Filters.text, answerC, pass_user_data=True)],
            ANSWER_D: [CommandHandler('cancel', cancel_add), MessageHandler(Filters.text, answerD, pass_user_data=True)],
            ANSWERS: [CommandHandler('cancel', cancel_add), MessageHandler(Filters.text, answers_true, pass_user_data=True)],
            ADD_CHECK: [CommandHandler('cancel', cancel_add), MessageHandler(Filters.text, add_check, pass_user_data=True)],
        },
        fallbacks=[CommandHandler('cancel', cancel_add)]
    )
    # registration.py
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('login', callback=log_in)],
        states={
            TEACHER: [CommandHandler('cancel', cancel_log_in),
                      MessageHandler(Filters.text, teacher_check, pass_user_data=True)],
            FAN: [CommandHandler('cancel', cancel_log_in),
                      MessageHandler(Filters.text, teacher_fan, pass_user_data=True)],
            KLASS: [CommandHandler('cancel', cancel_log_in), MessageHandler(Filters.text, klass, pass_user_data=True)],
            SURNAME: [CommandHandler('cancel', cancel_log_in), MessageHandler(Filters.text, last_name, pass_user_data=True)],
            NAME: [CommandHandler('cancel', cancel_log_in), MessageHandler(Filters.text, first_name, pass_user_data=True)],
            NUMBER: [CommandHandler('cancel', cancel_log_in), MessageHandler(Filters.all, nomer, pass_user_data=True)],
        },
        fallbacks=[CommandHandler('cancel', cancel_log_in)]
    )

    dp.add_handler(start_handler)
    dp.add_handler(help1_handler)
    dp.add_handler(help2_handler)
    dp.add_handler(test_handler)
    dp.add_handler(add_handler)
    dp.add_handler(registration_handler)
    dp.add_error_handler(do_error)
    dp.add_handler(start_cancel)
    dp.add_handler(message_handler)

    updater.start_polling()
    updater.idle()
    logger.info("Finish")


if __name__ == '__main__':
    main()