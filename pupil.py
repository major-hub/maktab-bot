from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from db_pupils import *
from db_tests import *
from config import *


def submit(ball: int):
    if ball == 5:
        return "a'lo darajada"
    elif ball == 4:
        return "muvofaqqiyatli"
    elif ball == 3:
        return "qoniqarli"
    elif ball == 2:
        return "qoniqarsiz"
    elif ball == 1:
        return "juda qoniqarsiz"
    elif ball == 0:
        return "mutlaq 0 darajada"
    else:
        return "Xatolik yuz berdi"


# savol  qaytaradi
def question(update: Update, context, number: int):  # number question soni
    number -= 1
    true_answ = ''
    test = context.user_data[1][number]
    test = test.split('##')
    answ = test[1].split('\n')
    savol = str(number+1) + '. ' + test[0] + '\n'
    for i in answ:
        if i.startswith('*'):
            savol += i[1:] + '\n'
            true_answ += i[1]
        else:
            savol += i + '\n'
    context.user_data[11] = true_answ    # togri javob, user_data[11]
    update.message.reply_text(
        text=savol,
        reply_markup=answers()
    )


def test(update: Update, context):
    user = update.effective_user
    if user.id in admin_ids():
        update.message.reply_text(
            text="🚷 Test o'quvchilar uchun."
                 "\n\nTestlarni ko'rish uchun batafsil /help da",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    elif not check_person(user_id=user.id):
        update.message.reply_text(
            text="Iltimos, oldin ro'yhatdan o'ting.\n"
                 "Ro'yhatdan o'tish uchun /login ni bosing",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "⚡️ Qaysi fandan test topshirmoqchisiz ?",
            reply_markup=fanlar_buttons()
        )
        return TESTFAN


def test_fan(update: Update, context):
    text = update.effective_message.text
    user = update.effective_user
    context.user_data[0] = text   # fan
    if text in fanlar:
        if check_submit_test(user_id=user.id, fan=text):
            update.message.reply_text(
                f"Siz {text} fanidan test topshirgansiz! "
                "Ustozingiz baholaguncha kuting\n\n"
                "Boshqa fanning testiga urinib ko'ring",
                reply_markup=fanlar_buttons()
            )
            return TESTFAN
        else:
            try:
                klass = sinf_for_add_test.get(get_klass(user_id=user.id))
                test = []
                for savol, javob in get_tests(klass=klass, fan=text):
                    test.append(savol + "##" + javob)
                test = generate_answers(test)
                context.user_data[1] = test   # testlar [savol##javob]
                question(update, context, 1)
                return TEST1
            except Exception:
                update.message.reply_text(
                    text="⚠️ Hali testlar kiritilmagan",
                    reply_markup=fanlar_buttons()
                )
                return TESTFAN
    else:
        update.message.reply_text(
            "Iltimos, fanlardan birini tanlang !",
            reply_markup=fanlar_buttons()
        )
        return TESTFAN


def check1(update: Update, context):
    text = update.effective_message.text
    if text in ANSWS:
        if text == context.user_data[11]:
            context.user_data[10] = 1      # ball
            update.message.reply_text("Javobingiz tog'ri")
        else:
            context.user_data[10] = 0
            tr_answ = context.user_data[11]
            update.message.reply_text(f"Afsuski, javobingiz notog'ri\nTo'g'ri javob {tr_answ}")
        question(update, context, 2)
        return TEST2
    else:
        update.message.reply_text("Iltimos, variantlardan birini tanlang")
        question(update, context, 1)
        return TEST1


def check2(update: Update, context):
    text = update.effective_message.text
    if text in ANSWS:
        if text == context.user_data[11]:
            context.user_data[10] += 1
            update.message.reply_text("Javobingiz tog'ri")
        else:
            tr_answ = context.user_data[11]
            update.message.reply_text(f"Afsuski, javobingiz notog'ri\nTo'g'ri javob {tr_answ}")
        question(update, context, 3)
        return TEST3
    else:
        update.message.reply_text("Iltimos, variantlardan birini tanlang")
        question(update, context, 2)
        return TEST2


def check3(update: Update, context):
    text = update.effective_message.text
    if text in ANSWS:
        if text == context.user_data[11]:
            context.user_data[10] += 1
            update.message.reply_text("Javobingiz tog'ri")
        else:
            tr_answ = context.user_data[11]
            update.message.reply_text(f"Afsuski, javobingiz notog'ri\nTo'g'ri javob {tr_answ}")
        question(update, context, 4)
        return TEST4
    else:
        update.message.reply_text("Iltimos, variantlardan birini tanlang")
        question(update, context, 3)
        return TEST3


def check4(update: Update, context):
    text = update.effective_message.text
    if text in ANSWS:
        if text == context.user_data[11]:
            context.user_data[10] += 1
            update.message.reply_text("Javobingiz tog'ri")
        else:
            tr_answ = context.user_data[11]
            update.message.reply_text(f"Afsuski, javobingiz notog'ri\nTo'g'ri javob {tr_answ}")
        question(update, context, 5)
        return TEST5
    else:
        update.message.reply_text("Iltimos, variantlardan birini tanlang")
        question(update, context, 4)
        return TEST4


def check5(update: Update, context):
    user = update.effective_user
    text = update.effective_message.text
    if text in ANSWS:
        if text == context.user_data[11]:
            context.user_data[10] += 1
            update.message.reply_text("Javobingiz tog'ri")
        else:
            tr_answ = context.user_data[11]
            update.message.reply_text(f"Afsuski, javobingiz notog'ri\nTo'g'ri javob {tr_answ}")
        update.message.reply_text(
            text=f"Tabriklaymiz, siz testlarni {submit(context.user_data[10])} topshirdingiz\nSizda to'g'ri javoblar soni {context.user_data[10]} ta",
            reply_markup=ReplyKeyboardRemove(),
        )
        if context.user_data[10] == 0:
            context.user_data[10] = -1
        rating(user_id=user.id, fan=context.user_data[0], ball=context.user_data[10])
        update.message.reply_text(
            text="Javobingiz ustozingizga yetkaziladi\n\n<b>Keyingi testga yaxshi tayyorlaning</b>",
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END
    else:
        update.message.reply_text("Iltimos, variantlardan birini tanlang")
        question(update, context, 5)
        return TEST5


def cancel_test(update: Update, context):
    user = update.effective_user
    update.message.reply_text("Siz testni to'xtatdingiz!\n"
                              "Endi, bu fandan ertaga qaytadan urinib ko'ring",
                              reply_markup=ReplyKeyboardRemove())
    rating(user_id=user.id, fan=context.user_data[0], ball=-1)
    return ConversationHandler.END


# O'quvchilarning barcha kamandalari
def user_commands(update: Update, text: str):
    if text == "📝 Test topshirish":
        update.message.reply_text(
            "Test topshirish uchun /test ni bosing!"
        )
    elif text == '◀️Orqaga':
        update.message.reply_text(
            text="Xurmatli o'quvchi! Test topshirishga tayyormisiz ?\n\n"
                 "#diqqat Bu bot orqali o'qtuvchingiz sizni baholaydi va sizga ma'lumot yuboradi",
            reply_markup=pupil_help_buttons()
        )
    else:
        update.message.reply_text(
            "Bu faqat test ishlash va ustozingiz yuborgan ma'lumotlardan foydalanish uchun",
            reply_markup=pupil_help_buttons()
        )