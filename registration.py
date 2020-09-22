from config import *
from telegram import ParseMode, Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ConversationHandler

from db_pupils import *


def log_in(update: Update, context):
    update.message.reply_text("Tanlang !", reply_markup=start_buttons())
    return TEACHER


def teacher_check(update: Update, context):
    user = update.effective_user

    text = update.effective_message.text
    if text == "👨‍🏫 Ustoz":
        if user.id in admin_ids():
            update.message.reply_text("Siz ro'yhatdan o'tgansiz.\n"
                                      "Batafsil /help da",
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        else:
            update.message.reply_text("Marhamat, Parolni kiriting",
                                      reply_markup=ReplyKeyboardRemove())
            return FAN
    elif text == "👨‍🎓 O'quvchi":
        if not check_person(user_id=user.id):
            update.message.reply_text(
                text="Familya va ismingiz <b>Jurnal</b> bilan bir xil bo'lsin",
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardRemove()
            )
            update.message.reply_text(
                text="<b>Sinfingizni</b> tanlang:",
                parse_mode=ParseMode.HTML,
                reply_markup=pupils(),
            )
            return KLASS
        else:
            update.message.reply_text("Siz ro'yhatdan o'tgansiz.\n"
                                      "Batafsil /help da",
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
    else:
        update.message.reply_text("Iltimos, quyidagilardan birini tanlang!",
                                  reply_markup=start_buttons())
        return TEACHER


def teacher_fan(update: Update, context):
    text = update.effective_message.text
    if text == "43":
        update.message.reply_text(
            "Qaysi fandan dars berasiz ?",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["Rus_tili", "Matematika"],
                    ["Ona_tili", "Informatika"],
                    ["Ingliz_tili", "Tarix"],
                    ["Jismoniy_tarbiya", "Kimyo"],
                    ["Biologiya", "Texnologiya"],
                    ["Geografiya", "Fizika"],
                    ["Milliy_istiqlol_goyasi"]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        return KLASS
    else:
        update.message.reply_text(
            "Iltimos, to'g'risini tanlang !",
            reply_markup=start_buttons()
        )
        return TEACHER


def klass(update: Update, context):
    text = update.effective_message.text
    if text in klasses or text in fanlar:

        context.user_data[0] = text
        update.message.reply_text(
            text="<b>Familyangizni</b> kiriting, e'tibor bilan",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove(),
        )
        return SURNAME
    else:
        update.message.reply_text(
            text="Iltimos, quyidagilardan birini tanlang!",
        )
        return KLASS


def last_name(update: Update, context):
    text = update.effective_message.text
    if text:
        context.user_data[1] = text
        update.message.reply_text(
            text="<b>Ismingizni</b> kiriting, e'tibor bilan",
            parse_mode=ParseMode.HTML,
        )
        return NAME
    else:
        update.message.reply_text(
            text="Iltimos, faqat familyangizni kiriting",
            parse_mode=ParseMode.HTML,
        )
        return SURNAME


def first_name(update: Update, context):
    text = update.effective_message.text
    if text:
        context.user_data[2] = text
        update.message.reply_text(
            text="Iltimos, <b>telefon</b> tugmasini bosing",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("📞 telefon", request_contact=True)]],
                                             resize_keyboard=True)
        )
        return NUMBER
    else:
        update.message.reply_text(
            text="Iltimos, faqat ismingizni kiriting",
            parse_mode=ParseMode.HTML,
        )
        return NAME


#nomer
def nomer(update: Update, context):
    user = update.effective_user
    text = update.effective_message.contact.phone_number
    context.user_data[3] = text

    if context.user_data.get(0) in klasses:
        add_pupil(sana=dt.datetime.now().date(), user_id=user.id, klass=context.user_data.get(0),
                  last_name=context.user_data.get(1), first_name=context.user_data.get(2), nomer=context.user_data[3])

    elif context.user_data.get(0) in fanlar:
        add_admin(admin_id=user.id, last_name=context.user_data.get(1), first_name=context.user_data.get(2),
                  fan=context.user_data.get(0), nomer=context.user_data[3])
    else:
        update.message.reply_text(
            text="Iltimos, <b>telefon</b> tugmasini bosing va ruxsat berish qiling",
            parse_mode=ParseMode.HTML,
        )
        return NUMBER
    update.message.reply_text(
        text="Tashakkur!\nSiz ro'yhatdan muvofaqqiyatli o'tdingiz\n\nBatafsil /help da",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def cancel_log_in(update: Update, context):
    update.message.reply_text("Avval ro'yhatdan o'ting", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
