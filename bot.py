print("BOT STARTING...")
from flask import Flask
from threading import Thread
import os

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8775952227:AAEcxoBPstbiI296-3-Dwd-fvpuQXW9z0E4"
ADMIN_ID = 497424696
GROUP_ID = -1003901678768  # umumiy guruh — barcha anonim murojaatlar


def _env_group(name, default=None):
    value = os.environ.get(name)
    return int(value) if value else default


PSYCHOLOGIST_GROUP_ID = _env_group("PSYCHOLOGIST_GROUP_ID", -1004401375212)
INSPECTOR_GROUP_ID = _env_group("INSPECTOR_GROUP_ID", -1004396095050)
STUDENT_COUNCIL_GROUP_ID = _env_group("STUDENT_COUNCIL_GROUP_ID")
YOUTH_OFFICE_GROUP_ID = _env_group("YOUTH_OFFICE_GROUP_ID", -1004377862023)
YOUTH_STAFF_GROUPS = {
    "tillaxodjayeva": _env_group("YOUTH_TILLAXODJAYEVA_GROUP_ID"),
    "raxmatullayev": _env_group("YOUTH_RAXMATULLAYEV_GROUP_ID"),
    "ernazarova": _env_group("YOUTH_ERNAZAROVA_GROUP_ID"),
}

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot ishlayapti!"

user_messages = {}
user_message_targets = {}
user_priority = {}
user_priority_target = {}
user_contact_target = {}
user_lang = {}
counter = 1

PSYCHOLOGIST_PHOTO_PATH = os.path.join(os.path.dirname(__file__), "psychologist.png")
INSPECTOR_PHOTO_PATH = os.path.join(os.path.dirname(__file__), "inspector.png")
YOUTH_PHOTO_DIR = os.path.dirname(os.path.abspath(__file__))

YOUTH_OFFICE_STAFF = {
    "tillaxodjayeva": {
        "name": "Tillaxodjayeva Sayyora Qobiljonovna",
        "photo": os.path.join(YOUTH_PHOTO_DIR, "youth_tillaxodjayeva.png"),
        "position_uz": "5 tashabbus bo'yicha",
        "position_ru": "по 5 инициативам",
        "prompt_uz": "Tillaxodjayeva Sayyora Qobiljonovnaga murojaatingizni yozing.",
        "prompt_ru": "Напишите ваше обращение Tillaxodjayeva Sayyora Qobiljonovna.",
        "admin": "5 tashabbus",
    },
    "raxmatullayev": {
        "name": "Raxmatullayev Abdulaziz Ismatulla o'g'li",
        "photo": os.path.join(YOUTH_PHOTO_DIR, "youth_raxmatullayev.png"),
        "position_uz": "sport masalalari bo'yicha",
        "position_ru": "по спортивным вопросам",
        "prompt_uz": "Raxmatullayev Abdulaziz Ismatulla o'g'liga murojaatingizni yozing.",
        "prompt_ru": "Напишите ваше обращение Raxmatullayev Abdulaziz Ismatulla o'g'li.",
        "admin": "Sport masalalari",
    },
    "ernazarova": {
        "name": "Ernazarova Feruza G'ofurovna",
        "photo": os.path.join(YOUTH_PHOTO_DIR, "youth_ernazarova.png"),
        "position_uz": "TTJ hamda ijara bo'yicha",
        "position_ru": "по общежитию и аренде",
        "prompt_uz": "Ernazarova Feruza G'ofurovnaga murojaatingizni yozing.",
        "prompt_ru": "Напишите ваше обращение Ernazarova Feruza G'ofurovna.",
        "admin": "TTJ va ijara",
    },
}

BUTTONS = {
    "psychologist": {"uz": "Psixolog", "ru": "Психолог"},
    "inspector": {"uz": "Inspektor", "ru": "Инспектор"},
    "student_council": {"uz": "Talabalar Kengashi", "ru": "Студенческий совет"},
    "youth_office": {"uz": "Yoshlar ishlari ofisi", "ru": "Офис по делам молодежи"},
}

CONTACT_TARGETS = {
    "psychologist": {
        "uz": "psixologga",
        "ru": "психологу",
        "admin": "Psixolog",
        "reply_uz": "Psixolog javobi",
        "reply_ru": "Ответ психолога",
    },
    "inspector": {
        "uz": "inspektorga",
        "ru": "инспектору",
        "admin": "Inspektor",
        "reply_uz": "Inspektor javobi",
        "reply_ru": "Ответ инспектора",
    },
    "student_council": {
        "uz": "Talabalar Kengashiga",
        "ru": "Студенческому совету",
        "admin": "Talabalar Kengashi",
        "reply_uz": "Talabalar Kengashi javobi",
        "reply_ru": "Ответ Студенческого совета",
    },
}
for _key, _staff in YOUTH_OFFICE_STAFF.items():
    CONTACT_TARGETS[f"youth_{_key}"] = {
        "uz": _staff["name"],
        "ru": _staff["name"],
        "admin": _staff["admin"],
        "reply_uz": f"{_staff['name']} javobi",
        "reply_ru": f"Ответ {_staff['name']}",
        "group_id": YOUTH_STAFF_GROUPS.get(_key) or YOUTH_OFFICE_GROUP_ID,
    }

CONTACT_TARGETS["psychologist"]["group_id"] = PSYCHOLOGIST_GROUP_ID
CONTACT_TARGETS["inspector"]["group_id"] = INSPECTOR_GROUP_ID
CONTACT_TARGETS["student_council"]["group_id"] = STUDENT_COUNCIL_GROUP_ID

psychologist_texts = {
    "uz": (
        "🧠<b>Psixolog</b>\n\n"
        "<b>Nargiza Ma’murovna Norova</b>\n"
        "Oliy toifali psixolog\n\n"
        "💯Murojaatchilarning shaxsiga oid ma’lumotlar sir saqlanadi!\n\n"
        "⏰<b>Ish vaqti:</b> 9:00-17:00\n\n"
        "🗓 <b>Qabul kunlari:</b>\n"
        "Seshanba     🕥 10:30-16:00\n"
        "Payshanba    🕙 10:00-16:00\n"
        "Juma         🕥 10:30-16:00\n\n"
        
        "📍<b>Manzil: «F» (TTJ) Bino, 1-qavat, 115-xona.</b>"
    ),
    "ru": (
        "🧠<b>Психолог</b>\n\n"
        "<b>Наргиза Мамуровна Норова</b>\n"
        "Психолог высшей категории\n\n"
        "💯Личные данные обратившихся сохраняются в тайне!\n\n"
        "⏰<b>Время работы:</b> 9:00-17:00\n\n"
        "🗓 <b>Дни приема:</b>\n"
        "Вторник      🕥 10:30-16:00\n"
        "Четверг      🕙 10:00-16:00\n"
        "Пятница      🕥 10:30-16:00\n\n"
        
        "📍<b>Адрес: здание «F» (Общежитие), 1-й этаж, кабинет 115.</b>"
    )
}
inspector_texts = {
    "uz": (
        "👮<b>Inspektor bilan aloqa</b>\n\n"
        "<b>Boymatov Shaxzod Inom o‘g‘li</b>\n"
        "Katta leytenant · Profilaktika katta inspektori\n\n"
        "Universitet faoliyati, ichki tartib-qoidalar yoki talabalik hayotiga oid "
        "masalalar yuzasidan murojaat qilishingiz mumkin.\n\n"
        "🔒Murojaatlaringiz maxfiyligi ta'minlanadi va belgilangan tartibda ko‘rib chiqiladi.\n\n"
        "🤝Sizning taklif va murojaatlaringiz universitet muhitini yanada takomillashtirishga xizmat qiladi.\n\n"
        "📍<b>Manzil:</b> "
    ),
    "ru": (
        "👮 <b>Связь с инспектором</b>\n\n"
        "<b>Бойматов Шахзод Ином Угли</b>\n"
        "Старший лейтенант · Старший инспектор профилактики\n\n"
        "Вы можете обратиться по вопросам деятельности университета, внутренних правил "
        "или студенческой жизни.\n\n"
        "🔒Конфиденциальность ваших обращений обеспечивается, они рассматриваются в установленном порядке.\n\n"
        "🤝Ваши предложения и обращения помогают улучшать университетскую среду.\n\n"
        "📍<b>Адрес:</b>"
    )
}

def btn(key, lang):
    return BUTTONS[key][lang]


def is_button(message, key):
    return message.text in (BUTTONS[key]["uz"], BUTTONS[key]["ru"])


def main_menu(lang="uz"):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    markup.add(
        KeyboardButton(btn("psychologist", lang)),
        KeyboardButton(btn("inspector", lang))
    )
    markup.add(
        KeyboardButton(btn("student_council", lang)),
        KeyboardButton(btn("youth_office", lang))
    )
    return markup


def contact_markup(target, lang):
    markup = InlineKeyboardMarkup()
    if target == "psychologist":
        text = "Связаться с психологом" if lang == "ru" else "Psixolog bilan bog‘lanish"
    else:
        text = "Связаться с инспектором" if lang == "ru" else "Inspektor bilan bog‘lanish"
    markup.add(InlineKeyboardButton(text, callback_data=f"contact_{target}"))
    return markup


def write_markup(lang):
    markup = InlineKeyboardMarkup()
    text = "Написать" if lang == "ru" else "Yozish"
    markup.add(InlineKeyboardButton(text, callback_data="write_message"))
    return markup


BOT_USERNAME = None


def get_bot_username():
    global BOT_USERNAME
    if BOT_USERNAME is None:
        BOT_USERNAME = bot.get_me().username
    return BOT_USERNAME


def youth_office_text(lang="uz"):
    bot_username = get_bot_username()
    lines = []
    for i, (key, staff) in enumerate(YOUTH_OFFICE_STAFF.items(), 1):
        position = staff["position_ru"] if lang == "ru" else staff["position_uz"]
        name = staff["name"]
        link = f"https://t.me/{bot_username}?start=youth_{key}"
        lines.append(f'{i}. <a href="{link}"><b>{name}</b> — {position}</a>')
    return "\n".join(lines)


def prompt_youth_staff(user_id, staff_key):
    lang = user_lang.get(user_id, "uz")
    staff = YOUTH_OFFICE_STAFF[staff_key]
    user_contact_target[user_id] = f"youth_{staff_key}"
    prompt = staff["prompt_ru"] if lang == "ru" else staff["prompt_uz"]
    caption = f"<b>{prompt}</b>"
    photo_path = staff["photo"]

    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            bot.send_photo(
                user_id,
                photo,
                caption=caption,
                parse_mode="HTML",
                reply_markup=main_menu(lang)
            )
    else:
        bot.send_message(
            user_id,
            caption,
            parse_mode="HTML",
            reply_markup=main_menu(lang)
        )


def contact_prompt(target, lang):
    if lang == "ru":
        return f"<b>Отправьте свое обращение {CONTACT_TARGETS[target]['ru']}.</b>"
    return f"<b>{CONTACT_TARGETS[target]['uz'].capitalize()} murojaatingizni yuboring.</b>"


def target_admin_line(target):
    if not target:
        return ""
    return f"\n🎯 <b>Yo‘nalish:</b> {CONTACT_TARGETS[target]['admin']}"


def reply_header(target, lang="uz"):
    if target and target in CONTACT_TARGETS:
        label = CONTACT_TARGETS[target]["reply_ru" if lang == "ru" else "reply_uz"]
    elif lang == "ru":
        label = "Ответ администратора"
    else:
        label = "Admin javobi"
    return f"📩 <b>{label}:</b>"


def get_reply_group_ids(target):
    if target and target in CONTACT_TARGETS:
        specific = CONTACT_TARGETS[target].get("group_id")
        if specific and specific != ADMIN_ID:
            return [specific]
    return []


def get_monitored_group_ids():
    group_ids = set()
    for target in CONTACT_TARGETS.values():
        group_id = target.get("group_id")
        if group_id:
            group_ids.add(group_id)
    return group_ids


def register_appeal(message_id, user_id, target):
    user_messages[message_id] = user_id
    user_message_targets[message_id] = target


def send_user_reply(user_id, target, reply_text):
    lang = user_lang.get(user_id, "uz")
    header = reply_header(target, lang)
    bot.send_message(
        user_id,
        f"{header}\n\n{reply_text}",
        parse_mode="HTML",
        reply_markup=main_menu(lang)
    )


def send_anon_to_group(message, group_id, info_text, content_suffix=""):
    if message.text:
        return bot.send_message(
            group_id,
            info_text + content_suffix,
            parse_mode="HTML"
        )
    if message.photo:
        return bot.send_photo(
            group_id,
            message.photo[-1].file_id,
            caption=info_text,
            parse_mode="HTML"
        )
    if message.video:
        return bot.send_video(
            group_id,
            message.video.file_id,
            caption=info_text,
            parse_mode="HTML"
        )
    if message.audio:
        return bot.send_audio(
            group_id,
            message.audio.file_id,
            caption=info_text,
            parse_mode="HTML"
        )
    if message.document:
        return bot.send_document(
            group_id,
            message.document.file_id,
            caption=info_text,
            parse_mode="HTML"
        )
    if message.voice:
        return bot.send_voice(
            group_id,
            message.voice.file_id,
            caption=info_text,
            parse_mode="HTML"
        )
    return None


def send_anon_to_groups(message, info_anon, info_archive, user_id, target, content_suffix=""):
    for group_id in get_reply_group_ids(target):
        sent = send_anon_to_group(message, group_id, info_anon, content_suffix)
        if sent:
            register_appeal(sent.message_id, user_id, target)

    if GROUP_ID and GROUP_ID != ADMIN_ID:
        send_anon_to_group(message, GROUP_ID, info_archive, content_suffix)


def forward_appeal(message, info_full, info_anon, info_archive, user_id, target):
    sent_admin = None

    if message.text:
        content_suffix = f"\n\n<pre>{message.text}</pre>"
        sent_admin = bot.send_message(
            ADMIN_ID,
            info_full + content_suffix,
            parse_mode="HTML"
        )
        send_anon_to_groups(message, info_anon, info_archive, user_id, target, content_suffix)

    elif message.photo:
        sent_admin = bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=info_full,
            parse_mode="HTML"
        )
        send_anon_to_groups(message, info_anon, info_archive, user_id, target)

    elif message.video:
        sent_admin = bot.send_video(
            ADMIN_ID,
            message.video.file_id,
            caption=info_full,
            parse_mode="HTML"
        )
        send_anon_to_groups(message, info_anon, info_archive, user_id, target)

    elif message.audio:
        sent_admin = bot.send_audio(
            ADMIN_ID,
            message.audio.file_id,
            caption=info_full,
            parse_mode="HTML"
        )
        send_anon_to_groups(message, info_anon, info_archive, user_id, target)

    elif message.document:
        sent_admin = bot.send_document(
            ADMIN_ID,
            message.document.file_id,
            caption=info_full,
            parse_mode="HTML"
        )
        send_anon_to_groups(message, info_anon, info_archive, user_id, target)

    elif message.voice:
        sent_admin = bot.send_voice(
            ADMIN_ID,
            message.voice.file_id,
            caption=info_full,
            parse_mode="HTML"
        )
        send_anon_to_groups(message, info_anon, info_archive, user_id, target)

    if sent_admin:
        register_appeal(sent_admin.message_id, user_id, target)

    return sent_admin

texts = {
    "uz": {
        "start": "<b>Assalomu alaykum!</b>\n\n📩 Murojaatingizni yozib qoldiring.",
        "recipient_prompt": "<b>Assalomu alaykum!</b>\n\nKimga murojaat yo'llamoqchisiz:",
        "help": "ℹ️ <b>Yordam</b>\n\n"
                "Ushbu bot orqali anonim tarzda yuborishingiz mumkin:\n"
                "• takliflar 💡\n"
                "• murojaatlar 📝\n"
                "• shikoyatlar ⚠️\n"
                "• e’tirozlar 📢\n\n"
                "Bot quyidagilarni qabul qiladi:\n\n"
                "• 📝 Matnli xabarlar\n"
                "• 🖼 Foto\n"
                "• 🎥 Video\n"
                "• 🎤 Ovozli xabarlar\n"
                "📩 Xabaringizni yoki faylni yuboring.\n\n"
                "🔒 Sizning shaxsingiz sir saqlanadi",
        "about": "📌<b>Bot haqida</b>\n\n"
                 "Mazkur bot <a href='https://t.me/uwedsc'>Talabalar Kengashining</a> "
                 "rasmiy anonim murojaatlar boti hisoblanadi.\n\n"
                 "<blockquote>📩<b>Ushbu bot orqali siz murojaatlaringizni anonim tarzda yo‘llashingiz mumkin.</b></blockquote>"
    },
    "ru": {
        "start": "<b>Здравствуйте!</b>\n\n📩 Отправьте ваше обращение.",
        "recipient_prompt": "<b>Assalomu alaykum!</b>\n\nКому вы хотите направить обращение:",
        "help": "ℹ️ <b>Помощь</b>\n\n"
                "Через этого бота вы можете анонимно отправить:\n"
                "• предложения 💡\n"
                "• обращения 📝\n"
                "• жалобы ⚠️\n"
                "• возражения 📢\n\n"
                "Бот принимает:\n\n"
                "• 📝 Текстовые сообщения\n"
                "• 🖼 Фото\n"
                "• 🎥 Видео\n"
                "• 🎤 Голосовые сообщения\n"
                "📩 Отправьте сообщение или файл.\n\n"
                "🔒 Ваша личность останется анонимной",
        "about": "📌<b>О боте</b>\n\n"
                 "Этот бот является официальным анонимным ботом обращений "
                 "<a href='https://t.me/uwedsc'>Студенческого совета</a>.\n\n"
                 "<blockquote>📩<b>Вы можете отправлять обращения анонимно.</b></blockquote>"
        
    }
}
# 🌐 /language — tilni tanlash
@bot.message_handler(commands=['language'])
def change_language(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
    )

    bot.send_message(
        message.chat.id,
        "🌐<b>Tilni tanlang / Выберите язык:</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )


# 🌐 /start — tilni tanlash
@bot.message_handler(commands=['start'])
def start(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1 and parts[1].startswith("youth_"):
        staff_key = parts[1].replace("youth_", "", 1)
        if staff_key in YOUTH_OFFICE_STAFF:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            prompt_youth_staff(message.from_user.id, staff_key)
            return

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="start_lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="start_lang_ru")
    )

    bot.send_message(
        message.chat.id,
        "🌐<b>Tilni tanlang / Выберите язык:</b>",
        reply_markup=markup,
        parse_mode="HTML"
    )


# 🌐 TILNI SAQLASH (bitta universal handler)
@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_") or call.data.startswith("start_lang_"))
def set_language(call):
    lang = call.data.split("_")[-1]
    user_lang[call.from_user.id] = lang

    # 🔥 startdan kelgan
    if call.data.startswith("start_"):
        bot.send_message(
            call.from_user.id,
            texts[lang]["help"],
            parse_mode="HTML",
            reply_markup=write_markup(lang)
        )
    else:
        # 🔥 /language dan kelgan
        if lang == "ru":
            text = "✅<b>Язык изменён</b>"
        else:
            text = "✅<b>Til o‘zgartirildi</b>"

        bot.send_message(call.from_user.id, text, reply_markup=main_menu(lang))


@bot.callback_query_handler(func=lambda call: call.data == "write_message")
def write_message_handler(call):
    lang = user_lang.get(call.from_user.id, "uz")
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.from_user.id,
        texts[lang]["recipient_prompt"],
        parse_mode="HTML",
        reply_markup=main_menu(lang)
    )


# ℹ️ HELP
@bot.message_handler(commands=['help'])
def help_command(message):
    lang = user_lang.get(message.from_user.id, "uz")

    bot.send_message(
        message.chat.id,
        texts[lang]["help"],
        parse_mode="HTML",
        reply_markup=main_menu(lang)
    )

# 📌 ABOUT
@bot.message_handler(commands=['about'])
def about_command(message):
    lang = user_lang.get(message.from_user.id, "uz")

    bot.send_message(
        message.chat.id,
        texts[lang]["about"],
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=main_menu(lang)
    )

# 🧠 PSYCHOLOGIST
def send_psychologist_info(chat_id, user_id):
    lang = user_lang.get(user_id, "uz")

    if os.path.exists(PSYCHOLOGIST_PHOTO_PATH):
        with open(PSYCHOLOGIST_PHOTO_PATH, "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=psychologist_texts[lang],
                parse_mode="HTML",
                reply_markup=contact_markup("psychologist", lang)
            )
    else:
        bot.send_message(
            chat_id,
            psychologist_texts[lang],
            parse_mode="HTML",
            reply_markup=contact_markup("psychologist", lang)
        )



@bot.message_handler(
    content_types=['text'],
    func=lambda message: message.chat.type == 'private'
    and is_button(message, "psychologist")
)
def psychologist_old_button(message):
    user_contact_target.pop(message.from_user.id, None)

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass

    send_psychologist_info(message.chat.id, message.from_user.id)


def send_inspector_info(chat_id, user_id):
    lang = user_lang.get(user_id, "uz")

    if os.path.exists(INSPECTOR_PHOTO_PATH):
        with open(INSPECTOR_PHOTO_PATH, "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=inspector_texts[lang],
                parse_mode="HTML",
                reply_markup=contact_markup("inspector", lang)
            )
    else:
        bot.send_message(
            chat_id,
            inspector_texts[lang],
            parse_mode="HTML",
            reply_markup=contact_markup("inspector", lang)
        )


@bot.message_handler(
    content_types=['text'],
    func=lambda message: message.chat.type == 'private'
    and is_button(message, "inspector")
)
def inspector_button(message):
    user_contact_target.pop(message.from_user.id, None)

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass

    send_inspector_info(message.chat.id, message.from_user.id)


@bot.message_handler(
    content_types=['text'],
    func=lambda message: message.chat.type == 'private'
    and is_button(message, "student_council")
)
def student_council_button(message):
    lang = user_lang.get(message.from_user.id, "uz")
    user_contact_target[message.from_user.id] = "student_council"

    bot.send_message(
        message.chat.id,
        contact_prompt("student_council", lang),
        parse_mode="HTML",
        reply_markup=main_menu(lang)
    )


@bot.message_handler(
    content_types=['text'],
    func=lambda message: message.chat.type == 'private'
    and is_button(message, "youth_office")
)
def youth_office_button(message):
    lang = user_lang.get(message.from_user.id, "uz")
    user_contact_target.pop(message.from_user.id, None)

    bot.send_message(
        message.chat.id,
        youth_office_text(lang),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=main_menu(lang)
    )


# 📩 CONTACT REQUEST
@bot.callback_query_handler(func=lambda call: call.data in ["contact_psychologist", "contact_inspector"])
def start_contact_request(call):
    target = call.data.replace("contact_", "")
    lang = user_lang.get(call.from_user.id, "uz")
    user_contact_target[call.from_user.id] = target

    bot.answer_callback_query(call.id)
    bot.send_message(
        call.from_user.id,
        contact_prompt(target, lang),
        parse_mode="HTML",
        reply_markup=main_menu(lang)
    )

# 📩 USER yozadi → PRIORITY TANLAYDI
MENU_BUTTONS = set()
for _labels in BUTTONS.values():
    MENU_BUTTONS.add(_labels["uz"])
    MENU_BUTTONS.add(_labels["ru"])


@bot.message_handler(
    content_types=['text', 'photo', 'video', 'audio', 'document', 'voice'],
    func=lambda message: message.chat.type == 'private'
    and message.from_user.id != ADMIN_ID
    and not (message.text and message.text.startswith('/'))
    and not (message.text and message.text in MENU_BUTTONS)
)
def forward_message(message):
    lang = user_lang.get(message.from_user.id, "uz")
    target = user_contact_target.pop(message.from_user.id, None)

    # 🔘 BUTTON TEXTLAR
    if lang == "ru":
        btn1 = "🚨 Срочно"
        btn2 = "📩 Обычное обращение"
        if target:
            text = f"<b>Выберите приоритет обращения {CONTACT_TARGETS[target]['ru']}:</b>"
        else:
            text = "<b>Выберите приоритет обращения:</b>"
    else:
        btn1 = "🚨 Shoshilinch"
        btn2 = "📩 Oddiy murojaat"
        if target:
            text = f"<b>{CONTACT_TARGETS[target]['uz'].capitalize()} murojaatingiz ustuvorligini tanlang:</b>"
        else:
            text = "<b>Murojaatingiz ustuvorligini tanlang:</b>"

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(btn1, callback_data="high"),
        InlineKeyboardButton(btn2, callback_data="normal")
    )

    user_priority[message.from_user.id] = message
    user_priority_target[message.from_user.id] = target

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup,
        parse_mode="HTML"
    )

# 🔥 PRIORITY TANLANGANDA
@bot.callback_query_handler(func=lambda call: call.data in ["high", "normal"])
def handle_priority(call):
    global counter

    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass

    message = user_priority.get(call.from_user.id)
    if not message:
        bot.answer_callback_query(call.id, "Xatolik!")
        return

    user = message.from_user
    target = user_priority_target.get(call.from_user.id)

    priority = "🚨 SHOSHILINCH" if call.data == "high" else "📩 Oddiy murojaat"

    username = f"@{user.username}" if user.username else "Yo‘q"
    link = f"https://t.me/{user.username}" if user.username else "Yo‘q"

    info_full = (
        f"📩 <b>Murojaat №{counter}</b>\n\n"
        f"{priority}" + target_admin_line(target) + "\n\n"
        f"👤 <b>Ism:</b> {user.first_name}\n"
        f"🔗 <b>Username:</b> {username}\n"
        f"🌐 <b>Profil:</b> {link}\n"
        f"🆔 <b>ID:</b> {user.id}"
    )

    info_anon = (
        f"📩 <b>Anonim murojaat №{counter}</b>\n\n"
        f"{priority}" + target_admin_line(target) + "\n\n"
        "❗ Javob berish uchun shu xabarga reply qiling\n"
        "<i>Для ответа — reply на это сообщение</i>"
    )

    info_archive = (
        f"📩 <b>Anonim murojaat №{counter}</b>\n\n"
        f"{priority}" + target_admin_line(target) + "\n\n"
        "📁 <i>Umumiy arxiv</i>"
    )

    sent = forward_appeal(message, info_full, info_anon, info_archive, user.id, target)
    if not sent:
        bot.answer_callback_query(call.id, "Xatolik!")
        return

    counter += 1

   # 🌐 tilni aniqlaymiz
    lang = user_lang.get(call.from_user.id, "uz")

# 🔘 BUTTON

    if lang == "ru":
        btn_text = "Студенческий совет УМЭД"
        text = "<b>Ваше обращение отправлено! Скоро ответим.</b>"
    else:
        btn_text = "Talabalar Kengashi"
        text = "<b>Murojaatingiz yuborildi! Tez orada javob beramiz.</b>"

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            btn_text,
            url="https://t.me/uwedsc"
        )
    )

    bot.send_message(
        call.from_user.id,
        text,
        reply_markup=markup,
        parse_mode="HTML"
    )

# 🔥 XATONI OLDINI OLISH
    if call.from_user.id in user_priority:
        del user_priority[call.from_user.id]
    if call.from_user.id in user_priority_target:
        del user_priority_target[call.from_user.id]
    
    # ... boshqa funksiyalar (start, help, forward_message, handle_priority)

# 🔁 ADMIN VA GURUH JAVOBI
@bot.message_handler(commands=['groupid'])
def group_id_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(
        message.chat.id,
        f"🆔 <b>Chat ID:</b> <code>{message.chat.id}</code>",
        parse_mode="HTML"
    )


@bot.message_handler(
    func=lambda message: message.chat.id == ADMIN_ID
    and message.reply_to_message
    and message.text
)
def admin_reply(message):
    replied = message.reply_to_message
    user_id = user_messages.get(replied.message_id)

    if not user_id:
        bot.send_message(ADMIN_ID, "❗ Bu xabarga javob topilmadi")
        return

    target = user_message_targets.get(replied.message_id)
    send_user_reply(user_id, target, message.text)


@bot.message_handler(
    func=lambda message: message.chat.type in ["group", "supergroup"]
    and message.chat.id in get_monitored_group_ids()
    and message.reply_to_message
    and message.text
    and message.reply_to_message.from_user
    and message.reply_to_message.from_user.is_bot
)
def group_reply(message):
    replied = message.reply_to_message
    user_id = user_messages.get(replied.message_id)

    if not user_id:
        return

    target = user_message_targets.get(replied.message_id)
    send_user_reply(user_id, target, message.text)

if __name__ == "__main__":
    print("BOT STARTING...")

    def run_web():
        port = int(os.environ.get("PORT", 10000))
        app.run(host="0.0.0.0", port=port)

    Thread(target=run_web).start()

    bot.infinity_polling()

