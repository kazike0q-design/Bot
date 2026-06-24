from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

# URL de la imagen de portada
START_IMAGE_URL = "https://tu-imagen-aqui.jpg"


START_TEXT = """
╔══════════════════════════════════════════════════════════╗
                         ✨🌟 MissiaM 🌟✨
╚══════════════════════════════════════════════════════════╝

Hace siglos, el continente AeGedom cayó en manos de la corrupción y traición,
como una flor marchita bajo la sombra de la codicia. 🌑

Los Imperios fueron destruidos, Reyes olvidados y Dioses silenciados;
pues todo imperio es como el dedo que señala la luna, y no la luna misma. 🌙

Y aun así... las razas continúan luchando por sobrevivir,
ignorando que la batalla es ya la paz cuando el corazón deja de temblar. ❤️

Tu historia comienza ahora, oh viajero,
pues el maestro dice que el camino de mil liós comienza con un solo paso. 🧘🌄

═══════════════════════════════════════════════════════════
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✨ Comenzar", callback_data="start_game")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=START_IMAGE_URL,
        caption=START_TEXT,
        reply_markup=reply_markup
    )


async def start_game_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    gender_text = """
╔══════════════════════════════════════════════════════════╗
                         ✨🌟 MissiaM 🌟✨
╚══════════════════════════════════════════════════════════╝

¡Oh! ✨ Por favor, disculpa mi emoción, ¡soy Veyra! 🧝‍♀️
Los espíritus ancestrales me han encomendado la hermosa tarea
de guiarte en este viaje lleno de aventuras y desafíos... 💫

😊 Se lleva una mano a las mejillas, algo apenada, y sonríe con dulzura.

Qué descuidada soy, ¡si apenas nos conocemos! 🌟
Antes de avanzar, me daría mucha ilusión saber más de ti.
¿Te identificas como hombre o mujer? 👤
Para el pueblo de las hadas, esas distinciones no existen en nuestro mundo,
por lo que siempre nos da mucha curiosidad y respeto descubrir
cómo se sienten los caminantes como tú. 🧚

Progreso : ●○○○○○○○○○ 10%

═══════════════════════════════════════════════════════════
"""

    keyboard = [
        [
            InlineKeyboardButton("♂️ Hombre", callback_data="gender_male"),
            InlineKeyboardButton("♀️ Mujer", callback_data="gender_female")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(
        caption=gender_text,
        reply_markup=reply_markup
    )


async def select_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    gender = query.data

    if gender == "gender_male":
        context.user_data["gender"] = "Hombre"
    else:
        context.user_data["gender"] = "Mujer"

    race_text = """
╔══════════════════════════════════════════════════════════╗
                         ✨🌟 MissiaM 🌟✨
╚══════════════════════════════════════════════════════════╝

¡Oh, maravilloso! Entonces perteneces a esa hermosa mitad
que trae vida y continuidad al mundo 💖✨.
Es realmente interesante cómo se dividen los caminantes... 🧝‍♀️🌙

😊 Te observa con ojos brillantes ✨, ladeando la cabeza con una sonrisa curiosa.

Dime, buen viajero... 🌍 En este rincón del mundo conviven muchísimas
razas distintas, y muchas de ellas comparten tu misma forma de ser.
Para poder guiarte mejor por sus senderos 🌄,
¿me dirías a qué raza perteneces?
Mi corazón tiene mucha intriga por conocer tus raíces 🌳💫.

Progreso : ●●●○○○○○○○ 30%

═══════════════════════════════════════════════════════════
"""

    keyboard = [
        [InlineKeyboardButton("👤 Humanos", callback_data="race_human")],
        [InlineKeyboardButton("🧝 Elfos", callback_data="race_elf")],
        [InlineKeyboardButton("🧔 Enanos", callback_data="race_dwarf")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(
        caption=race_text,
        reply_markup=reply_markup
    )


def register_start_handlers(app):
    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(
            start_game_callback,
            pattern="^start_game$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            select_gender,
            pattern="^gender_(male|female)$"
        )
    )
