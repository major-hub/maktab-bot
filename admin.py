import random
from datetime import datetime
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from config import *
from db_pupils import *
from db_tests import *


def get_datetime():
    return datetime.now().date()


# add test
def add(update: Update, context):
    user = update.effective_user
    if user.id in admin_ids():
        update.message.reply_text("Nechanchi sinf uchun savol kiritmoqchisiz",
                                  reply_markup=klasses_add_test())
        return LEVEL
    else:
        update.message.reply_text("🚷 Bu Ustozlar uchun")
        return ConversationHandler.END


def level(update: Update, context):
    text = update.effective_message.text
    if text == "Hamma sinfga" or text in klasslar:
        if text != "Hamma sinfga":
            context.user_data[0] = sinf_for_add_test[text]   # sinfi 5, 6, 7, ...
        else:
            context.user_data[0] = text
        update.message.reply_text(
            "⚠️Diqqat!\n"
            "Avval savolni keyin to'g'ri javob variantini va qolgan 3 ta variantni kiriting\n\n"
            "#diqqat Agar biror joyda xatolik yuz bersa, /cancel ni bosing",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )
        update.message.reply_text("❓ Savolni kiriting")
        return ANSWER_A
    else:
        update.message.reply_text("Sinfni tanlang")
        return LEVEL


def answerA(update: Update, context):
    text = update.effective_message.text
    if len(text) > 4:
        context.user_data[1] = text   # savol
        update.message.reply_text("✍️Savolning javobini, ya'ni to'g'ri variantni kiriting")
        return ANSWER_B
    else:
        update.message.reply_text("❌ Xatolik, savol uzunroq bolishi kerak. A javobni qayta kiriting")
        return ANSWER_A


def answerB(update: Update, context):
    text = update.effective_message.text
    context.user_data[2] = text   # true answer
    update.message.reply_text("✍️Qolgan 3ta variantlarni kiriting\n\nVariant №1")
    return ANSWER_C


def answerC(update: Update, context):
    text = update.effective_message.text
    context.user_data[3] = text  # variant 1
    update.message.reply_text("✍️Variant №2")
    return ANSWER_D


def answerD(update: Update, context):
    text = update.effective_message.text
    context.user_data[4] = text  # variant 2
    update.message.reply_text("✍️Variant №3")
    return ANSWERS


def answers_true(update: Update, context):
    text = update.effective_message.text
    context.user_data[5] = text  # variant 3
    javoblar = []
    for i in range(2, 6):
        javoblar.append(context.user_data[i])
    javoblar = gen_answers(javoblar)
    answ = ""
    variantlar = ["A) ", "B) ", "C) ", "D) "]
    for i in range(len(javoblar)):
        if javoblar[i] == context.user_data[2]:
            answ += "*"
        answ += variantlar[i] + javoblar[i] + '\n'
    test_javoblar = 'Savol: ' + context.user_data[1] + '\n' + answ
    context.user_data[6] = answ.strip()
    update.message.reply_text(f"❗️Tekshiring, to'g'rimi❓\n\n{test_javoblar}",
                              reply_markup=ReplyKeyboardMarkup([["👍Ha", "👎 Yo'q"]], resize_keyboard=True, one_time_keyboard=True))
    return ADD_CHECK


def add_check(update: Update, context):
    user = update.effective_user
    text = update.effective_message.text
    if text == "👍Ha":
        sinf = context.user_data[0]
        test = context.user_data[1]
        answ = context.user_data[6]
        fan = get_admin_fan(admin_id=user.id)
        add_test(sinf=sinf, test=test, answer=answ, fan=fan)
        update.message.reply_text("Test muvofaqqiyatli qo'shildi. Yana test qo'shish uchun /add ni bosing\n\n"
                                  "Testlarni ko'rish uchun batafsil /help da",
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        update.message.reply_text("❗️Unda qaytadan kiriting\n"
                                  "Nechanchi sinf uchun savol kiritmoqchisiz",
                                  reply_markup=klasses_add_test()
                                  )
        return LEVEL


def cancel_add(update: Update, context):
    update.message.reply_text("Siz testni to'xtatdingiz!\nQayta kiritish uchun /add ni bosing",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# ---------------END


def date_results(update, date):
    try:
        user = update.effective_user
        fan = get_admin_fan(admin_id=user.id)
        balls = [f"{sinf} {familya} {ism} {baho}" for sinf, familya, ism, baho in get_date_ball(fan=fan, date=date)]
        text = '\n'.join(balls)
        if len(text) == 0: text = "Ma'lumot topilmadi"
        update.message.reply_text(
            text=f"<pre>{text}</pre>",
            parse_mode=ParseMode.HTML,
            reply_markup=help_buttons()
        )
    except Exception:
        update.message.reply_text(
            text="<pre>Ma'lumot topilmadi</pre>\n\n",
            parse_mode=ParseMode.HTML,
            reply_markup=help_buttons()
        )


def klass_results(update, klass):
    try:
        user = update.effective_user
        fan = get_admin_fan(admin_id=user.id)
        balls = [f"{sana} {familya} {ism} {baho}" for sana, familya, ism, baho in get_klass_ball(fan=fan, klass=klass)]
        text = '\n'.join(balls)
        if len(text) == 0: text = "Ma'lumot topilmadi"
        update.message.reply_text(
            text=f"<pre>{text}</pre>\n\n"
                 "#diqqat Test natijalarini Jurnalizga qo'ygandan keyin 🔄Baholarni yangilash bosing."
                 " Shunda o'quvchi yana qayta test topshira oladi!",
            parse_mode=ParseMode.HTML,
            reply_markup=help_buttons()
        )
    except Exception:
        update.message.reply_text(
            text="<pre>Ma'lumot topilmadi</pre>\n\n",
            parse_mode=ParseMode.HTML,
            reply_markup=help_buttons()
        )


def send_messages_to_all_pupils(update, klass, text: str):
    for (user_id,) in get_all_pupil_ids(klass=klass):
        try:
            update.message.bot.send_message(chat_id=user_id,
                                            text=text,
                                            reply_markup=ReplyKeyboardRemove())  # 764297703
        except Exception:
            continue
    update.message.reply_text(f"Xabar {klass} sinfiga yuborildi!", reply_markup=help_buttons())


def show_pupils(update: Update, klass: str):
    try:
        royhat = [f"{familya} {ism}" for familya, ism in get_pupils(klass=klass, )]
        text = '\n'.join(royhat)
        if len(text) == 0: text = "Ma'lumot topilmadi"
        update.message.reply_text(
            text=f"<pre>{text}</pre>",
            parse_mode=ParseMode.HTML,
            reply_markup=help_buttons()
        )
    except Exception:
        update.message.reply_text(
            text="<pre>Ma'lumot topilmadi</pre>\n\n",
            parse_mode=ParseMode.HTML,
            reply_markup=help_buttons()
        )


def show_tests(update: Update, klass: str):
    user = update.effective_user
    test = ""
    fan = get_admin_fan(admin_id=user.id)
    i = 1
    try:
        for savol, javob in get_tests(klass=klass, fan=fan):
            javoblar = javob.split('\n')
            test += f'{i}-savol: ' + savol + '\n' + javoblar[0] + '\n' + javoblar[1] + '\n' + javoblar[2] + '\n' + javoblar[3] +'\n\n'
            i += 1
        update.message.reply_text(
            text=test,
            replpy_markup=ReplyKeyboardRemove()
        )
    except Exception:
        update.message.reply_text(
            text="⚠️ Hali testlar kiritilmagan",
            reply_markup=help_buttons()
        )

#supper admin uchun
def show_tests_admin(update: Update, klass: str, fan):
    if fan in fanlar:
        test = ""
        i = 1
        try:
            for savol, javob in get_tests(klass=klass, fan=fan):
                javoblar = javob.split('\n')
                test += f'{i}-savol: ' + savol + '\n' + javoblar[0] + '\n' + javoblar[1] + '\n' + javoblar[2] + '\n' + javoblar[3] +'\n\n'
                i += 1
            update.message.reply_text(
                text=test,
                replpy_markup=ReplyKeyboardRemove()
            )
        except Exception:
            update.message.reply_text(
                text="⚠️ Hali testlar kiritilmagan",
                reply_markup=help_buttons()
            )
    else:
        update.message.reply_text("Xatolik! Bunday fan mavjud emas")


# commands   [ natija, tozalash, xabar, testlar ]  opitniylar uchun
def admin_commands(update: Update, text: str):
    user = update.effective_user
    text = text.strip()
    if text == '#ustozlar':
        ustozi = ''
        for lname, fname, fan in get_ustozlar():
            ustoz = f"<pre>{lname} {fname} {fan}</pre>"
            ustozi += ustoz + '\n'
        update.message.reply_text(
            text=ustozi,
            parse_mode=ParseMode.HTML
        )
    elif text.find('#ustoz') == 0:
        if len(text.split(' ')) == 3:
            update.message.reply_text(
                f"{get_teacher_number(last_name=text.split(' ')[1], first_name=text.split(' ')[2])}",
            )
        else:
            update.message.reply_text(
                "Iltimos, namunadagidek kiriting !\n"
                "👨‍🏫 O'qituvchining nomeri olish uchun\n"
                "<u>Namuna:</u> <pre>#ustoz Kimsanov Kimsan</pre>\n"
                "👨‍🎓 O'quvchining nomeri olish uchun\n"
                "<u>Namuna:</u> <pre>#nomer 7A Kimsanov Kimsan</pre>",
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardRemove()
            )
    elif text.find('#testlar') == 0:
        if len(text.split(' ')) == 3:
            sinf = sinf_for_add_test[text.split(' ')[1]]     # 7, 8, 9....
            show_tests_admin(update, sinf, text.split(' ')[2])
        else:
            update.message.reply_text("Namunadek bo'lmadi. Namuna /help2 da")
    elif text.find('#xabar') == 0:
        if '#xabar' == text.split(' ')[0] and text.split(' ')[1][:2] in klasses:
            send_messages_to_all_pupils(update, text.split(' ')[1][:2], text)
        else:
            for klass in klasses:
                send_messages_to_all_pupils(update, klass, text)
    elif text.find('#nomer') == 0:
        if len(text.split(' ')) == 4 and len(text.split(' ')[1]) in (2, 3):
            update.message.reply_text(
                f"{get_pupil_number(klass=text.split(' ')[1], last_name=text.split(' ')[2], first_name=text.split(' ')[3])}",
            )
    elif text.find('#delete_pupil') == 0:
        xabr = delete_user(last_name=text.split(' ')[1], first_name=text.split(' ')[2])  # bazani qaytadan boshlash
        update.message.reply_text(xabr)
    elif text.find('#delete_teacher') == 0:
        xabr = delete_teacher(last_name=text.split(' ')[1], first_name=text.split(' ')[2])  # bazani qaytadan boshlash
        update.message.reply_text(xabr)
    else:
        update.message.reply_text("❌ Xatolik yuz berdi. Namunani /help dan ko'ring")


#opitniy adminlar uchun
def admin_commands2(update: Update, text: str):
    user = update.effective_user
    if text == '◀️Orqaga':
        update.message.reply_text(
            text="Sizga quyidagi tugmalar bo'yicha yordam beraman",
            reply_markup=help_buttons(),
        )
    elif text == "📄Bugunlik natijalar":
        date_results(update, get_datetime())
    #
    elif text == "👨‍🎓O'quvchilar ro'yhati":
        set_either(admin_id=user.id, force='list')
        update.message.reply_text(
            text="Qaysi sinfning ro'yhatini ko'rmoqchisiz",
            reply_markup=pupils(),
        )
    elif text == "👨‍🏫Sinf test natijalari":
        set_either(admin_id=user.id, force='result')
        update.message.reply_text(
            text="Qaysi sinfning test natijalarini ko'rmoqchisiz",
            reply_markup=pupils(),
        )
    elif text == "🔄Baholarni yangilash":
        set_either(admin_id=user.id, force='refresh')
        update.message.reply_text(
            text="Qaysi sinfning baholarini yangilamoqchi ya'ni tozalamoqchisiz",
            reply_markup=pupils(),
        )

    #
    elif text in klasses:
        if get_either(admin_id=user.id) == 'list':
            show_pupils(update, text)
        elif get_either(admin_id=user.id) == 'result':
            klass_results(update, text)
        elif get_either(admin_id=user.id) == 'refresh':
            fan = get_admin_fan(admin_id=user.id)
            if clear_one(fan=fan, klass=text):
                update.message.reply_text(
                    "Baholar muvofaqqiyatli tozalandi.",
                    reply_markup=help_buttons()
                )
            else:
                update.message.reply_text(
                    text="<pre>Ma'lumot topilmadi</pre>\n\n",
                    parse_mode=ParseMode.HTML,
                    reply_markup=help_buttons()
                )
        else:
            update.message.reply_text(
                "❌ Xatolik yuz berdi. Iltimos, sinflardan birini tanlang",
                reply_markup=pupils(),
            )
    #
    elif text == "✍️Xabar yuborish":
        update.message.reply_text(
            text="Xabarni quyidagi namunadek yozing\n"
                 "Biror sinfga yubormoqchi bo'lsayiz\n"
                 "<u>Namuna</u>: <pre>#xabar 7A `sizning xabariz`</pre>\n"
                 "Agar hamma sinflarga yubormoqchi bo'lsayiz\n"
                 "<u>Namuna</u>: <pre>#xabar `sizning xabariz`</pre>",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove(),
        )
    elif text == "✏️Test qo'shish":
        update.message.reply_text(
            text="Test qo'shish uchun /add ni bosing",
            reply_markup=ReplyKeyboardMarkup([['◀️Orqaga']], resize_keyboard=True)
        )
    elif text == "☎️Telefon nomer":
        update.message.reply_text(
            text="Telefon nomerni olish uchun quyidagi namunadek yozing\n\n"
                 "👨‍🏫 O'qituvchining nomeri olish uchun\n"
                 "<u>Namuna:</u> <pre>#ustoz Palonchiyev Pistonchi</pre>\n"
                 "👨‍🎓 O'quvchining nomeri olish uchun\n"
                 "<u>Namuna:</u> <pre>#nomer 7A Palonchiyev Pistonchi</pre>\n"
                 "Sinf 8A, 9B, ... ixtiyoriy!",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove(),
        )
    elif text == "📖Testlarni ko'rish":
        update.message.reply_text("Qaysi sinfning testlarini ko'rmoqchisiz",
                                  reply_markup=show_test_button())
    elif text in show_test_buttons:
        sinf = sinf_for_add_test[text.split('-')[0]]
        show_tests(update, sinf)

    else:
        update.message.reply_text("❌ Xatolik yuz berdi. Namunani /help dan ko'ring")