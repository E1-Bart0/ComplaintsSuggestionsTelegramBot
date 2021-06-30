from typing import Sequence

from telegram import InlineKeyboardButton

from db.models import User

SUGGESTION_HEADER = "😍 НОВОЕ ПРЕДЛОЖЕНИЕ 😍"
COMPLAINT_HEADER = "🤬 НОВАЯ ЖАЛОБА 🤬"
ANONYMOUS_MSG_HEADER = "😎 НОВОЕ АНОНИМНОЕ СООБЩЕНИЕ 😎"
NEW_PASSWORD_HEADER = "👀 Новый пароль для Суперпользователей 👀"  # noqa: S105
ALL_USERS_HEADER = "Список всех пользователей"
ALL_SU_HEADER = "Список всех суперпользователей"
ALL_ADMIN_HEADER = "Список всех администраторов"


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


def help_message_for_admin() -> str:
    return (
        "📌Справка по командам администратора\n"
        "- /all - Посмотреть всех пользователей;\n"
        "- /all_su - Посмотреть всех Суперпользователей;\n"
        "- /all_admin - Посмотреть всех Администраторов;\n"
        "- /add_su - Добавить Суперпользователя;\n"
        "- /remove_su - Удалить Суперпользователя;\n"
        "- /add_admin - Добавить Администратора;\n"
        "- /remove_admin - Удалить Администратора;\n"
    )


def help_message(user: User) -> str:
    additional_text = help_message_for_admin() if user.is_admin else ""
    return (
        "🤗 Справка 🤗\n\n"
        "Жалобы и предложения могут видеть только Суперпользователи SU.\n\n"
        "📌Справка по командам\n\n"
        "- /start - Добавляет пользователя в БД;\n"
        "- /del - Удаляет пользователя из БД;\n"
        "- /help - Выводит это сообщение. Справка;\n"
        "- /su <password> - Стать SU для просмотра всех Жалоб и Предложений;\n"
        "📌Справка по командам суперпользователя\n"
        "- /new_su_password <new_password> - Изменить пароль для SU, только активные SU могут менять пароль;\n"
        f"{additional_text}"
        "\n Спасибо за внимание!"
    )


def became_su_message() -> str:
    return (
        "🦸 Теперь Вы Суперпользователь 🦸\n\n"
        "Вы можете видеть все жалобы и предложения.\nПожалуйста. Наслаждайтесь🥂"
    )


def became_non_su_message() -> str:
    return "🦸 Теперь Вы Не Суперпользователь 🦸\n\n"


def became_admin_message() -> str:
    return (
        "🦸 Теперь Вы Администратор 🦸\n\n"
        "Вы можете использовать скрытые команды.\n"
        "Для просмотра команд введите /help"
    )


def became_non_admin_message() -> str:
    return "🦸 Теперь Вы Не Администратор 🦸\n\n"


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


def filed_message() -> str:
    return "🤖 Что-то пошло не так 🤖"


def get_all_members_message(members: Sequence[User], header: str) -> str:
    all_members = (
        f"{member.full_name}"
        f'{" =SU= " if member.is_superuser else ""}'
        f'{" *Admin* " if member.is_admin else ""}'
        for member in members
    )
    all_members_str = "\n".join(all_members)
    return f"{header}\n\nИмя пользователя\n{all_members_str}"


def get_username(member: User) -> str:
    return f"{member.full_name}"


def not_members_message():
    return "Нет пользователей"


def user_became_su_message(user: User):
    return f"{user.full_name} Теперь Суперпользователь"


def add_to_su_message():
    return "Кого хотите Добавить в Суперпользователи"


def remove_from_su_message():
    return "Кого хотите Удалить из Суперпользователей"


def add_to_admin_message():
    return "Кого хотите Добавить в Администраторы"


def remove_from_admin_message():
    return "Кого хотите Удалить из Администраторов"


def user_became_not_su_message(user: User):
    return f"{user.full_name} Больше Не Суперпользователь"


def user_became_admin_message(user: User):
    return f"{user.full_name} Теперь Администратор"


def user_became_not_admin_message(user: User):
    return f"{user.full_name} Больше Не Администратор"


def you_send_suggestion_message():
    return "Ваше Предложение отправлено"


def you_send_complaint_message():
    return "Ваша Жалоба отправлена"


def you_send_anonymous_message():
    return "Ваше Анонимное сообщение отправлено"


def you_success_send_message():
    return "Сообщение было отправлено"


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
