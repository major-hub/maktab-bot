import random
from telegram import ReplyKeyboardMarkup, Update

from db_pupils import get_admin_ids

TOKEN = "1334674877:AAEKKVc4iyN1bTbAlXMCMJrGCBkdiK1j6_8"  # online_maktab43_bot

# TOKEN = "1107674551:AAGQ7AAmVemS1rfZG0TyuSzoGWyWkHbx0Lw"  # online_maktab25_bot
# ADMIN_IDS = [764297703, 621383789]

ANSWS = ["A", "B", "C", "D"]
klasses = ['5A', '5B', '6A', '6B', '6D', '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B', '11A', '11B']
klasslar = ['5', '6', '7', '8', '9', '10', '11']
fanlar = ["Rus_tili", "Matematika", "Ona_tili", "Ingliz_tili", "Jismoniy_tarbiya",
          "Tarix", "Kimyo", "Fizika", "Biologiya", "Informatika", "Geografiya", "Texnologiya", "Milliy_istiqlol_goyasi"]


TEACHER, FAN, KLASS, SURNAME, NAME, NUMBER = range(6)
TESTFAN, TEST1, TEST2, TEST3, TEST4, TEST5 = range(6)
LEVEL, ANSWER_A, ANSWER_B, ANSWER_C, ANSWER_D, ANSWERS, ADD_CHECK = range(7)

sinf_for_add_test = {
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    '10': 'ten',
    '11': 'eleven'
}
show_test_buttons = ['5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf']


def admin_ids():
    res = []
    for (i,) in get_admin_ids():
        res.append(i)
    return res


def help_buttons():
    return ReplyKeyboardMarkup(
                [
                    ["👨‍🎓O'quvchilar ro'yhati"],  # sinf tanlanadi
                    ["✏️Test qo'shish", "📖Testlarni ko'rish"],  # sinf leveli tanlanadi
                    ["📄Bugunlik natijalar", "👨‍🏫Sinf test natijalari"],  # sinf tanlanadi
                    ["🔄Baholarni yangilash"],
                    ["✍️Xabar yuborish", "☎️Telefon nomer"]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )


def pupil_help_buttons():
    return ReplyKeyboardMarkup(
        [
            ["📝 Test topshirish"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def start_buttons():
    return ReplyKeyboardMarkup(
        [
            ["👨‍🏫 Ustoz", "👨‍🎓 O'quvchi"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def fanlar_buttons():
    return ReplyKeyboardMarkup(
        [
            ["Rus_tili", "Matematika"],
            ["Ona_tili", "Informatika"],
            ["Ingliz_tili", "Tarix"],
            ["Jismoniy_tarbiya", "Kimyo"],
            ["Biologiya", "Texnologiya"],
            ["Geografiya", "Fizika"],
            ["Milliy_istiqlol_goyasi"],
            ['◀️Orqaga']
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def show_test_button():
    return ReplyKeyboardMarkup(
        [
            ['5-sinf', '6-sinf', '7-sinf'],
            ['8-sinf', '9-sinf', '10-sinf'],
            ['◀️Orqaga', '11-sinf']
        ],
        resize_keyboard=True,
    )


def error(update, context):
    update.message.reply_text("Xatolik yuz berdi. Namunani /help dan ko'ring")

# ----------------------------------- Key Javoblar   ----------------------------- #


def answers():
    return ReplyKeyboardMarkup(
        [
            ['A', 'B'],
            ['C', 'D']
        ],
        resize_keyboard=True
    )
# ----------------------------------- O'quvchilar sinflari  ----------------------------- #


def pupils():
    return ReplyKeyboardMarkup(
        [
            ['5A', '5B', '6A', '6B', '6D'],
            ['7A', '7B', '8A', '8B', '9A'],
            ['9B', '10A', '10B', '11A', '11B'],
            ['◀️Orqaga']
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def klasses_add_test():
    return ReplyKeyboardMarkup(
        [
            ['5', '6', '7', '8', '9'],
            ['◀️Orqaga', '10', '11']
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def gen_answers(gen: list):
    res = []
    while len(res) != 4:
        index = random.randint(0, 17) % 4
        if gen[index] not in res:
            res.append(gen[index])
    return res


def generate_answers(answ: list):
    res = []
    while len(res) != 5:
        value = random.choice(answ)
        if value not in res:
            res.append(value)
    return res
