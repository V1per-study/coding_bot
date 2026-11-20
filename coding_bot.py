import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ================== ТОКЕН ==================
BOT_TOKEN = "9105342860:AAEgNAGwPcOBwII4mGOOGIjLsxLGQbOKwcY"  # від @BotFather
# ===========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ---------- Стани ----------
class UserState(StatesGroup):
    choosing_level = State()
    choosing_topic = State()


# ---------- Дані (теми по рівнях) ----------
TOPICS = {
    "beginner": {
        "variables": "📦 Змінні (Variables)\n\nЗмінна — це ім'я, під яким зберігається значення.\n\nПриклад:\n```python\nname = \"V1per\"\nage = 20\nis_student = True\n```\n\nТипи даних: str, int, float, bool",
        
        "conditions": "🔀 Умови (if/else)\n\nДозволяють виконувати код залежно від умови.\n\n```python\nage = 18\nif age >= 18:\n    print(\"Дорослий\")\nelse:\n    print(\"Неповнолітній\")\n```",
        
        "loops": "🔁 Цикли (for / while)\n\nfor — коли знаєш скільки разів:\n```python\nfor i in range(5):\n    print(i)\n```\n\nwhile — поки умова True:\n```python\ncount = 0\nwhile count < 3:\n    print(count)\n    count += 1\n```",
        
        "functions": "⚙️ Функції\n\nФункція — блок коду, який можна викликати багато разів.\n\n```python\ndef greet(name):\n    return f\"Привіт, {name}!\"\n\nprint(greet(\"V1per\"))\n```"
    },
    
    "intermediate": {
        "lists": "📋 Списки (Lists)\n\n```python\nnumbers = [1, 2, 3, 4]\nnumbers.append(5)\nprint(numbers[0])  # 1\n```\n\nМетоди: append, pop, remove, sort, len()",
        
        "dicts": "🗂️ Словники (Dictionaries)\n\n```python\nuser = {\n    \"name\": \"V1per\",\n    \"age\": 20,\n    \"skills\": [\"Python\", \"aiogram\"]\n}\nprint(user[\"name\"])\n```",
        
        "oop_basic": "🏗️ ООП (основи)\n\n```python\nclass Bot:\n    def __init__(self, name):\n        self.name = name\n\n    def start(self):\n        print(f\"{self.name} запущений\")\n\nmy_bot = Bot(\"V1perBot\")\nmy_bot.start()\n```",
        
        "exceptions": "⚠️ Обробка помилок\n\n```python\ntry:\n    number = int(input(\"Введи число: \"))\nexcept ValueError:\n    print(\"Це не число!\")\n```"
    },
    
    "advanced": {
        "decorators": "🎀 Декоратори\n\n```python\ndef logger(func):\n    def wrapper(*args, **kwargs):\n        print(f\"Викликаю {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@logger\ndef hello():\n    print(\"Привіт\")\n```",
        
        "async": "⚡ Асинхронність (async/await)\n\n```python\nimport asyncio\n\nasync def fetch_data():\n    await asyncio.sleep(1)\n    return \"Дані отримано\"\n\nasync def main():\n    result = await fetch_data()\n    print(result)\n\nasyncio.run(main())\n```",
        
        "generators": "🔄 Генератори\n\n```python\ndef countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor num in countdown(5):\n    print(num)\n```",
        
        "context_managers": "📂 Context Managers (with)\n\n```python\nwith open(\"file.txt\", \"r\") as f:\n    content = f.read()\n# файл автоматично закриється\n```"
    }
}


LEVEL_NAMES = {
    "beginner": "🟢 Початківець",
    "intermediate": "🟡 Середній",
    "advanced": "🔴 Продвинутий"
}


# ---------- Клавіатури ----------
def get_level_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🟢 Початківець", callback_data="level_beginner")
    builder.button(text="🟡 Середній", callback_data="level_intermediate")
    builder.button(text="🔴 Продвинутий", callback_data="level_advanced")
    builder.adjust(1)
    return builder.as_markup()


def get_topics_keyboard(level: str):
    builder = InlineKeyboardBuilder()
    
    topic_names = {
        "beginner": {
            "variables": "📦 Змінні",
            "conditions": "🔀 Умови",
            "loops": "🔁 Цикли",
            "functions": "⚙️ Функції"
        },
        "intermediate": {
            "lists": "📋 Списки",
            "dicts": "🗂️ Словники",
            "oop_basic": "🏗️ ООП",
            "exceptions": "⚠️ Помилки"
        },
        "advanced": {
            "decorators": "🎀 Декоратори",
            "async": "⚡ Async/Await",
            "generators": "🔄 Генератори",
            "context_managers": "📂 Context Managers"
        }
    }
    
    for key, name in topic_names[level].items():
        builder.button(text=name, callback_data=f"topic_{level}_{key}")
    
    builder.button(text="⬅️ Змінити рівень", callback_data="back_to_levels")
    builder.adjust(2)
    return builder.as_markup()


def get_back_to_topics_keyboard(level: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ До тем", callback_data=f"back_topics_{level}")
    return builder.as_markup()


# ---------- Хендлери ----------
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привіт! Я бот, який пояснює основи програмування.\n\n"
        "Спочатку вибери свій рівень:",
        reply_markup=get_level_keyboard()
    )
    await state.set_state(UserState.choosing_level)


@dp.callback_query(F.data.startswith("level_"))
async def choose_level(callback: CallbackQuery, state: FSMContext):
    level = callback.data.split("_")[1]
    await state.update_data(level=level)
    
    await callback.message.edit_text(
        f"Ти вибрав рівень: <b>{LEVEL_NAMES[level]}</b>\n\n"
        "Обери тему, про яку хочеш дізнатися:",
        reply_markup=get_topics_keyboard(level),
        parse_mode="HTML"
    )
    await state.set_state(UserState.choosing_topic)
    await callback.answer()


@dp.callback_query(F.data.startswith("topic_"))
async def show_topic(callback: CallbackQuery, state: FSMContext):
    _, level, topic_key = callback.data.split("_", 2)
    
    text = TOPICS[level][topic_key]
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_topics_keyboard(level),
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(F.data == "back_to_levels")
async def back_to_levels(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вибери свій рівень:",
        reply_markup=get_level_keyboard()
    )
    await state.set_state(UserState.choosing_level)
    await callback.answer()


@dp.callback_query(F.data.startswith("back_topics_"))
async def back_to_topics(callback: CallbackQuery, state: FSMContext):
    level = callback.data.split("_")[2]
    
    await callback.message.edit_text(
        f"Рівень: <b>{LEVEL_NAMES[level]}</b>\n\nОбери тему:",
        reply_markup=get_topics_keyboard(level),
        parse_mode="HTML"
    )
    await callback.answer()


# ---------- Запуск ----------
async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())