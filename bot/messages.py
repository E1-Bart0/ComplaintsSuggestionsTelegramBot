from telegram import InlineKeyboardButton

SUGGESTION_HEADER = "😍 НОВОЕ ПРЕДЛОЖЕНИЕ 😍"
COMPLAINT_HEADER = "🤬 НОВАЯ ЖАЛОБА 🤬"
ANONYMOUS_MSG_HEADER = "😎 НОВОЕ АНОНИМНОЕ СООБЩЕНИЕ 😎"
NEW_PASSWORD_HEADER = "👀 Новый пароль для Суперпользователь 👀"  # noqa: S105


def combine_header_and_msg(header, message):
    return f"**{header}**\n\n{message.text}"


def start_message(user_name: str) -> str:
    return (
        f"💌 Привет, {user_name}! 💌\n\n"
        "Я БОТ,\nСозданный для Анонимный Жалоб И Предложений\n"
        "Просто напиши мне, а Я передам Ваше сообщение от Своего имени тем, кто может что-то изменить.\n"
        "Спасибо!!!\n\n"
        "Для справки по командам напиши /help"
    )


def help_message() -> str:
    return (
        "🤗 Справка 🤗\n\n"
        "Жалобы и предложения могут видеть только Суперпользователи SU.\n\n"
        "📌Справка по командам\n"
        "- /start - Добавляет пользователя в БД;\n"
        "- /del - Удаляет пользователя из БД;\n"
        "- /help - Выводит это сообщение. Справка;\n"
        "- /su <password> - Стать SU для просмотра всех Жалоб и Предложений;\n"
        "- /new_su_password <new_password> - Изменить пароль для SU, только активные SU могут менять пароль;\n"
        "\n Спасибо за внимание!"
    )


def became_su_message() -> str:
    return (
        "🦸 Теперь Вы Суперпользователь 🦸\n\n"
        "Вы можете видеть все жалобы и предложения.\nПожалуйста. Наслаждайтесь🥂"
    )


def password_validation_message(password: str) -> str:
    return (
        "🦀Вы ввели неправильный пароль.🦀\n\n"
        f"`{password}` не подходит.\n"
        "Пожалуйста. Перепроверьте пароль"
    )


def wrong_new_password_message(password: str) -> str:
    return (
        "🐡 Недопустимый пароль 🐡\n\n"
        f"`{password}` - Длинна пароля {len(password)}\n"
        "Пароль должен быть не менее 4 символов и не более 16, "
        "а также не содержать пробелы и переходы на новую строку.\n"
        "Пожалуйста, Попробуйте еще раз."
    )


def ask_about_new_password_message(password: str) -> str:
    return f"🤐 Желаете изменить Пароль для SU 🤐\n\n {password}"


def not_su_message() -> str:
    return "🪱 Только суперпользователь может менять пароль 🪱"


def on_delete_message() -> str:
    return "😤 Вы были удалены из БД 😤"


def on_failed_deleted_message() -> str:
    return "🤖 Что-то пошло не так 🤖\n\nСкорее всего Вас не было в БД"


def ask_how_to_transfer_message() -> str:
    return "Передать в группу как:"


def successful_changed_password_message(password: str) -> str:
    return f"Пароль был успешно изменен на новый:\n\n{password}"


def filed_change_password_message() -> str:
    return "🤖 Что-то пошло не так 🤖"


ON_CHANGE_PASSWORD_KEYBOARD_1 = [
    [
        InlineKeyboardButton("Да", callback_data="confirm_change_password"),
        InlineKeyboardButton("Нет", callback_data="pass"),
    ],
]

ON_COMPLAINT_SUGGESTION_KEYBOARD = [
    [
        InlineKeyboardButton("Предложение", callback_data="suggestion"),
        InlineKeyboardButton("Жалоба", callback_data="complaint"),
    ],
    [
        InlineKeyboardButton("Анонимное\nСообщение", callback_data="anonymous message"),
        InlineKeyboardButton("Отмена", callback_data="stop"),
    ],
]
ON_CHANGE_PASSWORD_KEYBOARD_2 = [
    [
        InlineKeyboardButton(
            "Проинформировать Других", callback_data="info_about_changing"
        ),
        InlineKeyboardButton("Окей", callback_data="pass"),
    ],
]
